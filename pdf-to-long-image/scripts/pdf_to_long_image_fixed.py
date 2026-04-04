#!/usr/bin/env python3
"""
修复版：确保文字完整的PDF转长图片
使用保守裁剪策略，确保不丢失文字内容
"""

import os
import sys
from PIL import Image
import numpy as np

def conservative_crop(image, min_margin=50):
    """
    保守裁剪：只移除确认为空白的边缘
    
    参数:
        image: PIL Image对象
        min_margin: 最小保留边距
    
    返回:
        裁剪后的图像
    """
    # 转换为灰度
    if image.mode != 'L':
        gray = image.convert('L')
    else:
        gray = image
    
    img_array = np.array(gray)
    height, width = img_array.shape
    
    # 定义空白阈值（非常严格，只移除纯白区域）
    white_threshold = 253  # 只移除几乎纯白的区域
    
    # 检测顶部空白（从顶部开始）
    top_blank = 0
    for y in range(height):
        row = img_array[y, :]
        white_pixels = np.sum(row > white_threshold)
        if white_pixels / width > 0.99:  # 99%以上为纯白
            top_blank = y + 1
        else:
            break
    
    # 检测底部空白（从底部开始）
    bottom_blank = 0
    for y in range(height-1, -1, -1):
        row = img_array[y, :]
        white_pixels = np.sum(row > white_threshold)
        if white_pixels / width > 0.99:  # 99%以上为纯白
            bottom_blank = height - y
        else:
            break
    
    # 应用裁剪，但确保最小边距
    top = max(0, top_blank - min_margin)
    bottom = min(height, height - bottom_blank + min_margin)
    
    # 确保裁剪有效
    if bottom <= top:
        return image
    
    # 裁剪
    cropped = image.crop((0, top, width, bottom))
    return cropped

def pdf_to_long_image_preserve_text(pdf_path, output_path, dpi=200):
    """
    转换为长图片，确保文字完整
    
    参数:
        pdf_path: PDF文件路径
        output_path: 输出图片路径
        dpi: 分辨率
    """
    
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("❌ 需要安装pdf2image库")
        return False
    
    print(f"📄 处理PDF：{os.path.basename(pdf_path)}")
    print(f"🔧 修复模式：保守裁剪，确保文字完整")
    print(f"🎯 分辨率：{dpi} DPI")
    
    # 转换PDF为图片 - 使用更高的渲染质量
    print("🔄 转换PDF页面（高质量渲染）...")
    try:
        # 尝试使用更好的渲染参数
        images = convert_from_path(
            pdf_path, 
            dpi=dpi,
            fmt='png',  # 使用PNG格式，质量更好
            thread_count=4,
            use_pdftocairo=True  # 使用cairo渲染器，文字处理更好
        )
    except:
        # 如果cairo不可用，回退到默认
        try:
            images = convert_from_path(pdf_path, dpi=dpi)
        except Exception as e:
            print(f"❌ PDF转换失败：{e}")
            return False
    
    print(f"✅ 转换 {len(images)} 页完成")
    
    if not images:
        print("❌ 无页面可转换")
        return False
    
    # 保守处理每一页
    processed_images = []
    
    print("🔍 保守处理页面（确保文字完整）...")
    for i, img in enumerate(images):
        original_size = img.size
        
        # 第一页：几乎不裁剪，只移除纯白边缘
        if i == 0:
            # 第一页特别小心，只移除确认为空白的边缘
            cropped_img = conservative_crop(img, min_margin=100)
        else:
            # 其他页：保守裁剪
            cropped_img = conservative_crop(img, min_margin=50)
        
        cropped_amount = original_size[1] - cropped_img.height
        
        if cropped_amount > 0:
            print(f"   第 {i+1} 页：保守裁剪 {cropped_amount}px")
        else:
            print(f"   第 {i+1} 页：未裁剪")
        
        processed_images.append(cropped_img)
    
    # 计算拼接尺寸
    total_height = sum(img.height for img in processed_images)
    max_width = max(img.width for img in processed_images)
    
    print(f"📐 拼接尺寸：{max_width} × {total_height} 像素")
    print(f"   总高度：{total_height/1000:.1f}K 像素")
    
    # 创建长图片
    print("🎨 拼接图片...")
    
    # 使用白色背景
    long_image = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    
    y_offset = 0
    for i, img in enumerate(processed_images):
        # 居中放置
        x_offset = (max_width - img.width) // 2
        long_image.paste(img, (x_offset, y_offset))
        y_offset += img.height
        
        # 在页面间添加细分割线（1像素，浅灰色）
        if i < len(processed_images) - 1:
            line_y = y_offset
            for x in range(max_width):
                if x % 20 < 10:  # 虚线
                    long_image.putpixel((x, line_y), (230, 230, 230))
            y_offset += 1
    
    # 保存为高质量PNG
    print("💾 保存长图片...")
    long_image.save(output_path, 'PNG', quality=95, optimize=True)
    
    # 验证
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    final_img = Image.open(output_path)
    final_width, final_height = final_img.size
    
    print(f"✅ 修复版长图片生成成功！")
    print(f"   📏 尺寸：{final_width} × {final_height} 像素")
    print(f"   💾 大小：{file_size:.2f} MB")
    print(f"   📍 路径：{output_path}")
    
    # 创建预览以便检查
    preview_path = output_path.replace('.png', '_preview.jpg')
    if final_height > 3000:
        # 创建缩略预览
        preview_height = 3000
        preview_width = int(final_width * (preview_height / final_height))
        preview = final_img.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        preview.save(preview_path, 'JPEG', quality=85)
        print(f"   👀 预览图：{preview_path}")
    
    return True

def verify_text_completeness(image_path, expected_text_samples):
    """
    验证文字完整性
    
    参数:
        image_path: 图片路径
        expected_text_samples: 期望出现的文字样本列表
    """
    print("\n🔎 验证文字完整性...")
    
    try:
        # 使用OCR检查文字（如果可用）
        try:
            import pytesseract
            from PIL import Image
            
            img = Image.open(image_path)
            
            # 只检查第一页区域（前1/9）
            height = img.height
            check_height = height // 9
            check_region = img.crop((0, 0, img.width, check_height))
            
            # 提取文字
            text = pytesseract.image_to_string(check_region, lang='chi_sim+eng')
            
            print("   OCR检测到的文字（前1/9区域）：")
            print("   " + "-" * 40)
            for line in text.split('\n'):
                if line.strip():
                    print(f"   | {line[:50]}{'...' if len(line) > 50 else ''}")
            print("   " + "-" * 40)
            
            # 检查关键文字
            found_count = 0
            for sample in expected_text_samples:
                if sample in text:
                    found_count += 1
                    print(f"   ✅ 找到：{sample}")
                else:
                    print(f"   ⚠️ 未找到：{sample}")
            
            print(f"   📊 关键文字匹配率：{found_count}/{len(expected_text_samples)}")
            
        except ImportError:
            print("   ℹ️  OCR不可用，跳过文字验证")
            
    except Exception as e:
        print(f"   ⚠️ 验证失败：{e}")

if __name__ == "__main__":
    project_dir = "/mnt/d/编辑部/项目/2026-04-03-人类重返月球/05_发布"
    pdf_file = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_图片已嵌入.pdf")
    
    # 输出文件
    fixed_output = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_文字完整版.png")
    
    if not os.path.exists(pdf_file):
        print(f"❌ 找不到PDF：{pdf_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔧 PDF转长图片 - 文字完整修复版")
    print("=" * 60)
    
    # 期望出现的文字样本（用于验证）
    expected_texts = [
        "2026年4月1日",
        "阿尔忒弥斯II号",
        "肯尼迪航天中心",
        "54年来人类再次向月球进发",
        "为什么54年后",
        "从插旗子到建家园",
        "梦舟和揽月",
        "国际月球科研站",
        "月球为什么重要"
    ]
    
    # 转换PDF
    success = pdf_to_long_image_preserve_text(pdf_file, fixed_output, dpi=200)
    
    if success:
        # 验证文字完整性
        verify_text_completeness(fixed_output, expected_texts)
        
        print("\n" + "=" * 60)
        print("🎉 修复版转换完成！")
        print("=" * 60)
        print("📁 生成文件：")
        print(f"   1. 📝 文字完整版：{fixed_output}")
        
        # 检查文件大小
        file_size = os.path.getsize(fixed_output) / (1024 * 1024)
        print(f"\n💡 文件信息：")
        print(f"   • 大小：{file_size:.2f} MB")
        print(f"   • 格式：PNG（无损）")
        print(f"   • 特点：保守裁剪，确保文字完整")
        
        print("\n🔧 修复措施：")
        print("   1. 使用更严格的空白检测阈值")
        print("   2. 第一页特别保护，几乎不裁剪")
        print("   3. 确保最小边距，避免裁到文字")
        print("   4. 使用高质量PNG渲染")
    else:
        print("❌ 转换失败")