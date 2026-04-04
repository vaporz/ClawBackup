#!/usr/bin/env python3
"""
优化版：将PDF转换为高质量连续拼接的长图片
改进空白检测，提供更好的拼接效果
"""

import os
import sys
from PIL import Image
import numpy as np

def analyze_page_content(image, sample_rows=10):
    """
    分析页面内容分布，智能检测空白区域
    
    参数:
        image: PIL Image对象
        sample_rows: 采样行数
    
    返回:
        (top_blank, bottom_blank): 顶部和底部的空白高度
    """
    # 转换为灰度图
    if image.mode != 'L':
        gray = image.convert('L')
    else:
        gray = image
    
    img_array = np.array(gray)
    height, width = img_array.shape
    
    # 定义空白阈值（250以上为白色）
    white_threshold = 250
    
    # 检测顶部空白
    top_blank = 0
    for row in range(0, height, height // sample_rows):
        if row >= height:
            break
        row_pixels = img_array[row, :]
        white_ratio = np.sum(row_pixels > white_threshold) / width
        
        if white_ratio > 0.95:  # 95%以上为白色
            top_blank = row
        else:
            break
    
    # 检测底部空白
    bottom_blank = 0
    for row in range(height-1, -1, -height // sample_rows):
        if row < 0:
            break
        row_pixels = img_array[row, :]
        white_ratio = np.sum(row_pixels > white_threshold) / width
        
        if white_ratio > 0.95:  # 95%以上为白色
            bottom_blank = height - row
        else:
            break
    
    return top_blank, bottom_blank

def smart_crop_page(image, remove_top=True, remove_bottom=True):
    """
    智能裁剪页面，移除不必要的空白
    
    参数:
        image: PIL Image对象
        remove_top: 是否移除顶部空白
        remove_bottom: 是否移除底部空白
    
    返回:
        裁剪后的图像
    """
    width, height = image.size
    
    # 分析页面内容
    top_blank, bottom_blank = analyze_page_content(image)
    
    # 计算裁剪区域
    top = top_blank if remove_top else 0
    bottom = height - bottom_blank if remove_bottom else height
    
    # 确保裁剪有效
    if bottom <= top:
        bottom = top + 1
    
    # 裁剪图像
    if top > 0 or bottom < height:
        cropped = image.crop((0, top, width, bottom))
        return cropped
    else:
        return image

def pdf_to_high_quality_long_image(pdf_path, output_path, dpi=200):
    """
    将PDF转换为高质量连续拼接的长图片
    
    参数:
        pdf_path: PDF文件路径
        output_path: 输出图片路径
        dpi: 转换分辨率（推荐200-300）
    """
    
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("❌ 需要安装pdf2image库")
        return False
    
    print(f"📄 处理PDF：{os.path.basename(pdf_path)}")
    print(f"🎯 高质量模式：{dpi} DPI")
    print(f"📤 输出：{output_path}")
    
    # 转换PDF为图片
    print("🔄 转换PDF页面...")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"❌ 转换失败：{e}")
        return False
    
    print(f"✅ 转换 {len(images)} 页完成")
    
    if not images:
        print("❌ 无页面可转换")
        return False
    
    # 智能处理每一页
    processed_images = []
    total_cropped = 0
    
    print("✂️  智能裁剪页面空白...")
    for i, img in enumerate(images):
        original_height = img.height
        
        # 第一页保留顶部（可能有标题），其他页移除顶部空白
        remove_top = (i > 0)
        
        # 智能裁剪
        cropped_img = smart_crop_page(img, remove_top=remove_top, remove_bottom=True)
        
        cropped_amount = original_height - cropped_img.height
        total_cropped += cropped_amount
        
        if cropped_amount > 0:
            print(f"   第 {i+1} 页：裁剪 {cropped_amount}px")
        else:
            print(f"   第 {i+1} 页：无需裁剪")
        
        processed_images.append(cropped_img)
    
    print(f"📊 总计裁剪：{total_cropped}px")
    
    # 计算拼接尺寸
    total_height = sum(img.height for img in processed_images)
    max_width = max(img.width for img in processed_images)
    
    print(f"📐 拼接尺寸：{max_width} × {total_height} 像素")
    print(f"   相当于 {total_height/1000:.1f}K 像素高度")
    
    # 创建长图片
    print("🎨 拼接图片...")
    
    # 使用RGB模式，白色背景
    long_image = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    
    y_offset = 0
    for i, img in enumerate(processed_images):
        # 居中放置
        x_offset = (max_width - img.width) // 2
        long_image.paste(img, (x_offset, y_offset))
        y_offset += img.height
        
        # 添加细分割线（可选）
        if i < len(processed_images) - 1:
            # 在页面间添加1像素灰色细线
            line_y = y_offset
            for x in range(max_width):
                if x % 10 < 5:  # 虚线效果
                    long_image.putpixel((x, line_y), (240, 240, 240))
            y_offset += 1  # 分割线高度
    
    # 保存为高质量PNG
    print("💾 保存长图片...")
    
    # 根据文件大小选择压缩级别
    estimated_size = (max_width * total_height * 3) / (1024 * 1024)  # MB
    if estimated_size > 20:  # 如果预计超过20MB，使用较高压缩
        quality = 90
        optimize = True
    else:
        quality = 95
        optimize = True
    
    long_image.save(output_path, 'PNG', quality=quality, optimize=optimize)
    
    # 验证文件
    actual_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    final_img = Image.open(output_path)
    final_width, final_height = final_img.size
    
    print(f"✅ 长图片生成成功！")
    print(f"   📏 尺寸：{final_width} × {final_height} 像素")
    print(f"   💾 大小：{actual_size:.2f} MB")
    print(f"   📍 路径：{output_path}")
    
    return True

def create_web_friendly_version(long_image_path, web_output_path, max_width=1200):
    """
    创建适合网页使用的版本
    """
    try:
        img = Image.open(long_image_path)
        original_width, original_height = img.size
        
        # 计算缩放比例
        if original_width > max_width:
            ratio = max_width / original_width
            new_width = max_width
            new_height = int(original_height * ratio)
            
            print(f"🌐 创建网页版：{new_width} × {new_height} 像素")
            web_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存为WebP格式（更小文件）
            web_img.save(web_output_path, 'WEBP', quality=85, method=6)
            
            web_size = os.path.getsize(web_output_path) / 1024  # KB
            print(f"   💾 网页版大小：{web_size:.1f} KB (WebP格式)")
            
            return True
        else:
            print("⚠️ 原图宽度已适合网页，无需缩放")
            return False
            
    except Exception as e:
        print(f"⚠️ 网页版创建失败：{e}")
        return False

if __name__ == "__main__":
    project_dir = "/mnt/d/编辑部/项目/2026-04-03-人类重返月球/05_发布"
    pdf_file = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_图片已嵌入.pdf")
    
    # 输出文件
    hq_output = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_高质量长图.png")
    web_output = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_网页版.webp")
    
    if not os.path.exists(pdf_file):
        print(f"❌ 找不到PDF：{pdf_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("📊 PDF转长图片 - 高质量优化版")
    print("=" * 60)
    
    # 转换PDF
    success = pdf_to_high_quality_long_image(pdf_file, hq_output, dpi=200)
    
    if success:
        # 创建网页版
        print("\n🌐 创建网页友好版本...")
        create_web_friendly_version(hq_output, web_output, max_width=1200)
        
        print("\n" + "=" * 60)
        print("🎉 所有转换完成！")
        print("=" * 60)
        print("📁 生成文件清单：")
        print(f"   1. 📸 高质量长图：{hq_output}")
        print(f"   2. 🌐 网页版：{web_output}")
        print(f"   3. 📄 原始PDF：{pdf_file}")
        print("\n💡 使用场景：")
        print("   • 高质量长图：打印、高清展示")
        print("   • 网页版：社交媒体、网站分享")
        print("   • 原始PDF：文档编辑、打印")
    else:
        print("❌ 转换失败")