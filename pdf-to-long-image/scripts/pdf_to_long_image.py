#!/usr/bin/env python3
"""
PDF转长图片 - 核心脚本
将PDF文档转换为连续拼接的长图片
"""

import os
import sys
import argparse
from PIL import Image
import numpy as np

try:
    from pdf2image import convert_from_path
except ImportError:
    print("❌ 需要安装pdf2image库：pip install pdf2image")
    print("   还需要系统依赖：sudo apt-get install poppler-utils")
    sys.exit(1)

def detect_page_bottom_blank(image, threshold=0.95, blank_height_ratio=0.1):
    """
    检测页面底部的空白区域
    
    参数:
        image: PIL Image对象
        threshold: 空白判断阈值（0-1）
        blank_height_ratio: 从底部开始检测的比例
    
    返回:
        空白高度（像素），如果不是空白则返回0
    """
    # 转换为灰度图
    if image.mode != 'L':
        gray = image.convert('L')
    else:
        gray = image
    
    # 转换为numpy数组
    img_array = np.array(gray)
    height, width = img_array.shape
    
    # 从底部开始检测
    start_row = int(height * (1 - blank_height_ratio))
    
    for row in range(start_row, height):
        # 检查当前行是否空白
        row_pixels = img_array[row, :]
        white_pixels = np.sum(row_pixels > 250)  # 接近白色的像素
        white_ratio = white_pixels / width
        
        if white_ratio < threshold:
            # 找到非空白行，返回空白高度
            blank_height = row - start_row
            return blank_height
    
    # 整个检测区域都是空白
    return height - start_row

def remove_bottom_blank(image, blank_height):
    """
    移除页面底部的空白区域
    
    参数:
        image: PIL Image对象
        blank_height: 要移除的空白高度（像素）
    
    返回:
        裁剪后的图像
    """
    if blank_height <= 0:
        return image
    
    width, height = image.size
    new_height = height - blank_height
    
    # 裁剪图像（移除底部空白）
    cropped = image.crop((0, 0, width, new_height))
    return cropped

def pdf_to_long_image(pdf_path, output_path, dpi=150, margin_removal=10, 
                     threshold=0.95, blank_height_ratio=0.1):
    """
    将PDF转换为连续拼接的长图片
    
    参数:
        pdf_path: PDF文件路径
        output_path: 输出图片路径
        dpi: 转换分辨率
        margin_removal: 边缘移除像素
        threshold: 空白检测阈值
        blank_height_ratio: 空白检测区域比例
    """
    
    print(f"📄 正在处理PDF文件：{os.path.basename(pdf_path)}")
    print(f"   输出文件：{output_path}")
    print(f"   分辨率：{dpi} DPI")
    print(f"   参数：阈值={threshold}, 空白检测比例={blank_height_ratio}")
    
    # 转换PDF为图片列表
    print("🔄 正在转换PDF页面为图片...")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"❌ PDF转换失败：{e}")
        return False
    
    print(f"✅ 成功转换 {len(images)} 页")
    
    if not images:
        print("❌ 没有找到可转换的页面")
        return False
    
    # 处理每一页图片
    processed_images = []
    total_blank_removed = 0
    
    for i, img in enumerate(images):
        print(f"   处理第 {i+1}/{len(images)} 页...", end="")
        
        # 检测并移除底部空白
        blank_height = detect_page_bottom_blank(img, threshold, blank_height_ratio)
        
        if blank_height > 0:
            img = remove_bottom_blank(img, blank_height)
            total_blank_removed += blank_height
            print(f" 移除空白 {blank_height}px")
        else:
            print(" 无显著空白")
        
        # 移除边缘（可选）
        if margin_removal > 0:
            width, height = img.size
            img = img.crop((margin_removal, 0, width - margin_removal, height))
        
        processed_images.append(img)
    
    print(f"📊 总共移除空白：{total_blank_removed}px")
    
    # 计算总高度和最大宽度
    total_height = sum(img.height for img in processed_images)
    max_width = max(img.width for img in processed_images)
    
    print(f"📐 拼接尺寸：宽度={max_width}px, 总高度={total_height}px")
    
    # 创建空白画布
    print("🎨 正在拼接图片...")
    long_image = Image.new('RGB', (max_width, total_height), color='white')
    
    # 拼接图片
    y_offset = 0
    for i, img in enumerate(processed_images):
        # 居中放置（如果宽度不一致）
        x_offset = (max_width - img.width) // 2
        long_image.paste(img, (x_offset, y_offset))
        y_offset += img.height
    
    # 保存长图片
    print("💾 正在保存长图片...")
    
    # 根据文件扩展名选择格式
    ext = os.path.splitext(output_path)[1].lower()
    
    if ext == '.jpg' or ext == '.jpeg':
        # JPEG格式，调整质量
        quality = 95
        long_image.save(output_path, 'JPEG', quality=quality, optimize=True)
    elif ext == '.webp':
        # WebP格式
        long_image.save(output_path, 'WEBP', quality=95, method=6)
    else:
        # 默认PNG格式
        long_image.save(output_path, 'PNG', quality=95, optimize=True)
    
    # 统计信息
    file_size = os.path.getsize(output_path) / 1024 / 1024  # MB
    print(f"✅ 长图片生成成功！")
    print(f"   文件大小：{file_size:.2f} MB")
    print(f"   最终尺寸：{long_image.width} × {long_image.height} 像素")
    print(f"   保存路径：{output_path}")
    
    return True

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='将PDF转换为连续拼接的长图片')
    parser.add_argument('input', help='输入PDF文件路径')
    parser.add_argument('output', help='输出图片路径（支持.png/.jpg/.webp）')
    parser.add_argument('--dpi', type=int, default=150, help='转换分辨率（默认150）')
    parser.add_argument('--margin', type=int, default=10, help='边缘移除像素（默认10）')
    parser.add_argument('--threshold', type=float, default=0.95, help='空白检测阈值（默认0.95）')
    parser.add_argument('--ratio', type=float, default=0.1, help='空白检测区域比例（默认0.1）')
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在：{args.input}")
        sys.exit(1)
    
    # 检查输出目录
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 执行转换
    success = pdf_to_long_image(
        args.input,
        args.output,
        dpi=args.dpi,
        margin_removal=args.margin,
        threshold=args.threshold,
        blank_height_ratio=args.ratio
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()