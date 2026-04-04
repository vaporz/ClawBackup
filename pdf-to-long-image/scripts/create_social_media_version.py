#!/usr/bin/env python3
"""
创建社交媒体优化的长图片版本
针对微信、微博等平台进行优化
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def add_social_media_header(image, title, subtitle=None):
    """
    为长图片添加社交媒体友好的页眉
    
    参数:
        image: PIL Image对象
        title: 主标题
        subtitle: 副标题（可选）
    
    返回:
        添加页眉后的图像
    """
    width, height = image.size
    
    # 创建页眉区域（高度为图片高度的10%）
    header_height = min(200, height // 10)
    
    # 创建新图像（增加页眉高度）
    new_height = height + header_height
    new_image = Image.new('RGB', (width, new_height), color=(255, 255, 255))
    
    # 粘贴原图（在页眉下方）
    new_image.paste(image, (0, header_height))
    
    # 创建绘图对象
    draw = ImageDraw.Draw(new_image)
    
    try:
        # 尝试加载字体
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", 36)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf", 24)
    except:
        # 如果字体不存在，使用默认字体
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = header_height // 4
    
    draw.text((title_x, title_y), title, fill=(0, 51, 102), font=font_large)
    
    # 绘制副标题
    if subtitle:
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = title_y + 50
        
        draw.text((subtitle_x, subtitle_y), subtitle, fill=(102, 102, 102), font=font_small)
    
    # 添加装饰线
    line_y = header_height - 5
    draw.line([(width//4, line_y), (3*width//4, line_y)], fill=(0, 102, 153), width=2)
    
    return new_image

def add_social_media_footer(image, footer_text="勘星科技 | 让每个孩子爱上航天"):
    """
    为长图片添加社交媒体友好的页脚
    
    参数:
        image: PIL Image对象
        footer_text: 页脚文字
    
    返回:
        添加页脚后的图像
    """
    width, height = image.size
    
    # 创建页脚区域（高度为100像素）
    footer_height = 100
    
    # 创建新图像（增加页脚高度）
    new_height = height + footer_height
    new_image = Image.new('RGB', (width, new_height), color=(255, 255, 255))
    
    # 粘贴原图
    new_image.paste(image, (0, 0))
    
    # 创建绘图对象
    draw = ImageDraw.Draw(new_image)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # 绘制页脚文字
    footer_bbox = draw.textbbox((0, 0), footer_text, font=font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (width - footer_width) // 2
    footer_y = height + 30
    
    draw.text((footer_x, footer_y), footer_text, fill=(102, 102, 102), font=font)
    
    # 添加二维码位置提示
    qr_text = "扫码关注 | 获取更多航天科普"
    qr_bbox = draw.textbbox((0, 0), qr_text, font=font)
    qr_width = qr_bbox[2] - qr_bbox[0]
    qr_x = (width - qr_width) // 2
    qr_y = height + 60
    
    draw.text((qr_x, qr_y), qr_text, fill=(0, 102, 153), font=font)
    
    # 添加装饰线
    line_y = height
    draw.line([(width//4, line_y), (3*width//4, line_y)], fill=(204, 204, 204), width=1)
    
    return new_image

def optimize_for_wechat(image_path, output_path):
    """
    针对微信进行优化
    微信限制：图片大小不超过10MB，建议宽度1080px
    """
    img = Image.open(image_path)
    original_width, original_height = img.size
    
    print(f"📱 微信优化：原图 {original_width} × {original_height}")
    
    # 微信建议宽度1080px
    target_width = 1080
    
    if original_width > target_width:
        # 计算缩放比例
        ratio = target_width / original_width
        new_width = target_width
        new_height = int(original_height * ratio)
        
        print(f"   缩放至：{new_width} × {new_height}")
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 添加页眉页脚
    title = "昨晚，人类重返月球！"
    subtitle = "54年后，我们为何再次出发？"
    
    img_with_header = add_social_media_header(img, title, subtitle)
    img_with_footer = add_social_media_footer(img_with_header)
    
    # 保存为JPEG（微信更兼容）
    # 调整质量使文件大小小于10MB
    quality = 90
    img_with_footer.save(output_path, 'JPEG', quality=quality, optimize=True)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    
    # 如果文件太大，降低质量
    if file_size > 9.5:
        quality = 85
        img_with_footer.save(output_path, 'JPEG', quality=quality, optimize=True)
        file_size = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"   💾 文件大小：{file_size:.2f} MB")
    print(f"   ✅ 已保存：{output_path}")
    
    return output_path

def optimize_for_weibo(image_path, output_path):
    """
    针对微博进行优化
    微博长图建议：宽度1000px以内，高度不限
    """
    img = Image.open(image_path)
    original_width, original_height = img.size
    
    print(f"🐦 微博优化：原图 {original_width} × {original_height}")
    
    # 微博建议宽度1000px
    target_width = 1000
    
    if original_width > target_width:
        ratio = target_width / original_width
        new_width = target_width
        new_height = int(original_height * ratio)
        
        print(f"   缩放至：{new_width} × {new_height}")
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 微博喜欢更鲜艳的图片
    # 轻微增加对比度
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)
    
    # 保存为PNG（微博支持透明背景）
    img.save(output_path, 'PNG', optimize=True)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"   💾 文件大小：{file_size:.2f} MB")
    print(f"   ✅ 已保存：{output_path}")
    
    return output_path

def create_thumbnail(long_image_path, thumbnail_path, size=(400, 800)):
    """
    创建缩略图（用于预览）
    """
    img = Image.open(long_image_path)
    
    # 计算缩放比例，保持宽高比
    original_width, original_height = img.size
    target_width, target_height = size
    
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    
    thumbnail = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    thumbnail.save(thumbnail_path, 'JPEG', quality=85)
    
    print(f"🖼️  缩略图：{new_width} × {new_height}")
    print(f"   📍 保存至：{thumbnail_path}")
    
    return thumbnail_path

if __name__ == "__main__":
    project_dir = "/mnt/d/编辑部/项目/2026-04-03-人类重返月球/05_发布"
    
    # 使用高质量长图作为源
    source_image = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_高质量长图.png")
    
    if not os.path.exists(source_image):
        print(f"❌ 找不到源图片：{source_image}")
        print("请先运行 pdf_to_long_image_optimized.py")
        exit(1)
    
    print("=" * 60)
    print("📱 社交媒体优化版本生成")
    print("=" * 60)
    
    # 创建各个平台优化版本
    wechat_output = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_微信版.jpg")
    weibo_output = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_微博版.png")
    thumbnail_output = os.path.join(project_dir, "昨晚，人类重返月球！54年后，我们为何再次出发？_缩略图.jpg")
    
    print("\n1. 微信优化版本")
    print("-" * 40)
    optimize_for_wechat(source_image, wechat_output)
    
    print("\n2. 微博优化版本")
    print("-" * 40)
    optimize_for_weibo(source_image, weibo_output)
    
    print("\n3. 缩略图生成")
    print("-" * 40)
    create_thumbnail(source_image, thumbnail_output, size=(400, 800))
    
    print("\n" + "=" * 60)
    print("🎉 社交媒体优化完成！")
    print("=" * 60)
    print("📁 生成文件清单：")
    print(f"   1. 📱 微信版：{wechat_output}")
    print(f"   2. 🐦 微博版：{weibo_output}")
    print(f"   3. 🖼️  缩略图：{thumbnail_output}")
    print(f"   4. 📸 原生长图：{source_image}")
    
    print("\n💡 平台建议：")
    print("   • 微信：使用JPG格式，宽度1080px，带页眉页脚")
    print("   • 微博：使用PNG格式，宽度1000px，对比度增强")
    print("   • 缩略图：用于文章列表预览")
    print("\n🚀 发布提示：")
    print("   • 微信：图片大小需＜10MB")
    print("   • 微博：支持长图滚动查看")
    print("   • 建议添加话题标签：#人类重返月球 #航天科普")