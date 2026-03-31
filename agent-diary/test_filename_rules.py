#!/usr/bin/env python3
"""
测试日记文件名命名规则
验证修改后的agent-diary技能是否符合要求：
1. 文件名使用当前日期（写日记的日期）
2. 如果已存在当前日期的日记文件，在文件结尾继续追加
3. 日记文件保存在.diary目录下
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diary_main import DiarySkill

def test_diary_filename_rules():
    """测试日记文件名命名规则"""
    print("🧪 开始测试日记文件名命名规则...")
    
    # 创建临时工作空间
    temp_dir = tempfile.mkdtemp()
    print(f"📁 创建临时工作空间: {temp_dir}")
    
    try:
        # 创建DiarySkill实例
        diary = DiarySkill(temp_dir)
        
        # 测试1: 获取今天的日记路径
        diary_path = diary.get_today_diary_path()
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n✅ 测试1: 文件名使用当前日期")
        print(f"   当前日期: {today_str}")
        print(f"   生成的路径: {diary_path}")
        
        # 检查文件名是否正确
        expected_filename = f"{today_str}.md"
        actual_filename = os.path.basename(diary_path)
        
        if actual_filename == expected_filename:
            print(f"   ✅ 通过: 文件名正确 ({actual_filename})")
        else:
            print(f"   ❌ 失败: 期望 {expected_filename}, 实际 {actual_filename}")
            return False
        
        # 检查路径是否在.diary目录下
        if ".diary" in diary_path:
            print(f"   ✅ 通过: 文件保存在.diary目录下")
        else:
            print(f"   ❌ 失败: 文件不在.diary目录下")
            return False
        
        # 测试2: 创建日记文件
        print(f"\n✅ 测试2: 创建日记文件")
        result = diary.write_diary()
        
        if result["status"] == "created":
            print(f"   ✅ 通过: 成功创建日记文件")
            print(f"   文件路径: {result['path']}")
            
            # 验证文件是否存在
            if os.path.exists(result["path"]):
                print(f"   ✅ 通过: 文件确实存在")
            else:
                print(f"   ❌ 失败: 文件不存在")
                return False
        else:
            print(f"   ❌ 失败: 创建日记文件失败")
            return False
        
        # 测试3: 再次写日记（应该追加）
        print(f"\n✅ 测试3: 再次写日记（应该追加到现有文件）")
        result2 = diary.write_diary()
        
        if result2["status"] == "appended":
            print(f"   ✅ 通过: 成功追加到现有文件")
            print(f"   原始内容长度: {result2.get('existing_content_length', 'N/A')}")
            print(f"   追加的内容: {result2.get('appended_content', 'N/A')[:100]}...")
        else:
            print(f"   ❌ 失败: 期望追加但实际状态为 {result2['status']}")
            return False
        
        # 测试4: 检查文件内容
        print(f"\n✅ 测试4: 检查文件内容")
        with open(diary_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含两次写作的标记
        if "开始写今天的日记" in content and "继续写作" in content:
            print(f"   ✅ 通过: 文件包含初始内容和追加内容")
        else:
            print(f"   ❌ 失败: 文件内容不符合预期")
            return False
        
        print(f"\n🎉 所有测试通过！")
        return True
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"\n🧹 清理临时工作空间: {temp_dir}")

def test_date_logic():
    """测试日期逻辑：文件名使用当前日期，内容可以记录任何时间的事情"""
    print(f"\n📅 测试日期逻辑...")
    
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    
    print(f"   当前日期: {today_str}")
    print(f"   原则: 文件名使用当前日期 ({today_str}.md)")
    print(f"   内容: 可以记录今天、昨天或任何时间的事情")
    print(f"   示例: 2026年3月31日写的日记，文件名是 2026-03-31.md")
    print(f"         内容可以记录3月30日或更早的事情")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("📝 Agent-Diary 文件名命名规则测试")
    print("=" * 60)
    
    success = True
    
    # 运行测试
    if not test_diary_filename_rules():
        success = False
    
    if not test_date_logic():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过！文件名命名规则符合要求。")
    else:
        print("❌ 测试失败，请检查代码。")
    print("=" * 60)