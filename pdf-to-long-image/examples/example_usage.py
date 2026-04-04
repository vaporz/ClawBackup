#!/usr/bin/env python3
"""
PDF转长图片技能使用示例
"""

import os
import sys

# 添加技能脚本路径
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_dir = os.path.join(skill_dir, "scripts")
sys.path.insert(0, scripts_dir)

def example_basic():
    """基础使用示例"""
    print("📚 示例1: 基础转换")
    print("-" * 40)
    
    # 假设有一个PDF文件
    pdf_file = "example.pdf"  # 替换为实际文件
    output_file = "output_long.png"
    
    print(f"输入: {pdf_file}")
    print(f"输出: {output_file}")
    
    # 基础转换
    from pdf_to_long_image import pdf_to_long_image
    
    if os.path.exists(pdf_file):
        success = pdf_to_long_image(
            pdf_path=pdf_file,
            output_path=output_file,
            dpi=150,
            margin_removal=5,
            threshold=0.95
        )
        
        if success:
            print("✅ 转换成功！")
        else:
            print("❌ 转换失败")
    else:
        print(f"⚠️  示例文件不存在: {pdf_file}")
        print("   请替换为实际的PDF文件路径")

def example_advanced():
    """高级使用示例"""
    print("\n📚 示例2: 高级功能")
    print("-" * 40)
    
    # 使用优化版本
    try:
        from pdf_to_long_image_optimized import pdf_to_high_quality_long_image
        from create_social_media_version import optimize_for_wechat
        
        pdf_file = "document.pdf"
        
        if os.path.exists(pdf_file):
            # 1. 转换为高质量长图
            hq_output = "document_hq.png"
            print(f"1. 高质量转换: {hq_output}")
            pdf_to_high_quality_long_image(pdf_file, hq_output, dpi=200)
            
            # 2. 创建微信优化版
            wechat_output = "document_wechat.jpg"
            print(f"\n2. 微信优化: {wechat_output}")
            optimize_for_wechat(hq_output, wechat_output)
            
            print("\n✅ 高级转换完成！")
        else:
            print(f"⚠️  文件不存在: {pdf_file}")
            
    except ImportError as e:
        print(f"⚠️  需要高级脚本: {e}")

def example_command_line():
    """命令行使用示例"""
    print("\n📚 示例3: 命令行使用")
    print("-" * 40)
    
    commands = [
        "# 基础转换",
        "python scripts/pdf_to_long_image.py input.pdf output.png",
        "",
        "# 高质量转换（200 DPI）",
        "python scripts/pdf_to_long_image.py input.pdf output_hq.png --dpi 200",
        "",
        "# 保守裁剪（避免文字丢失）",
        "python scripts/pdf_to_long_image.py input.pdf output_safe.png --threshold 0.99",
        "",
        "# 创建JPEG格式（文件更小）",
        "python scripts/pdf_to_long_image.py input.pdf output.jpg",
    ]
    
    for cmd in commands:
        print(cmd)

def example_troubleshooting():
    """问题解决示例"""
    print("\n📚 示例4: 常见问题解决")
    print("-" * 40)
    
    problems = {
        "文字丢失": "使用 --threshold 0.99 或使用 pdf_to_long_image_fixed.py",
        "文件过大": "降低DPI（--dpi 120）或使用JPEG格式",
        "颜色失真": "使用PNG格式，检查PDF渲染设置",
        "内存不足": "分页处理或降低DPI",
    }
    
    for problem, solution in problems.items():
        print(f"❓ {problem}:")
        print(f"   💡 {solution}")
        print()

def main():
    """主函数"""
    print("=" * 60)
    print("📖 PDF转长图片技能使用示例")
    print("=" * 60)
    
    example_basic()
    example_advanced()
    example_command_line()
    example_troubleshooting()
    
    print("=" * 60)
    print("🎯 使用建议:")
    print("   1. 首次使用从基础版本开始")
    print("   2. 根据需求调整参数")
    print("   3. 转换后检查文字完整性")
    print("   4. 按平台要求选择输出格式")
    print("=" * 60)

if __name__ == "__main__":
    main()