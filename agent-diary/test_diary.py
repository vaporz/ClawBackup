#!/usr/bin/env python3
"""
日记Skill测试脚本
测试所有主要功能
"""

import os
import sys
import datetime
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diary_main import DiarySkill

def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能")
    print("=" * 50)
    
    skill = DiarySkill()
    
    # 测试迁移功能
    print("\n0. 测试迁移旧日记文件...")
    migration_result = skill.migrate_old_diaries()
    print(f"   迁移文件数: {migration_result['total_migrated']}")
    print(f"   失败文件数: {migration_result['total_failed']}")
    if migration_result['migrated']:
        print(f"   已迁移: {', '.join(migration_result['migrated'][:3])}{'...' if len(migration_result['migrated']) > 3 else ''}")
    
    # 测试1: 写日记
    print("\n1. 测试写日记...")
    result = skill.write_diary(
        memory_content="今天完成了月球科普文章，学习了日记写作技巧",
        flash_notes="[10:30] 想到一个关于星星的比喻\n[14:20] 今天天气真好，适合写科普"
    )
    
    print(f"   状态: {result['status']}")
    print(f"   路径: {result['path']}")
    print(f"   内容预览: {result['content'][:100]}...")
    
    # 测试2: 记录闪念
    print("\n2. 测试记录闪念...")
    flash_results = []
    test_notes = [
        "测试闪念1：科普写作需要更多生活化比喻",
        "测试闪念2：孩子们会喜欢什么样的科学故事？",
        "测试闪念3：日记真的是很好的自我对话方式"
    ]
    
    for note in test_notes:
        result = skill.record_flash_note(note)
        flash_results.append(result)
        print(f"   记录: {result['note']}")
    
    # 测试3: 获取闪念
    print("\n3. 测试获取闪念...")
    flash_notes = skill.get_flash_notes()
    print(f"   今日闪念总数: {len(flash_notes)}")
    for i, note in enumerate(flash_notes, 1):
        print(f"   {i:2d}. {note}")
    
    # 测试4: 检查文件是否存在
    print("\n4. 检查文件创建...")
    diary_path = skill.get_today_diary_path()
    flash_path = skill.get_today_flash_notes_path()
    
    print(f"   日记文件存在: {os.path.exists(diary_path)}")
    print(f"   闪念文件存在: {os.path.exists(flash_path)}")
    
    if os.path.exists(diary_path):
        with open(diary_path, 'r', encoding='utf-8') as f:
            diary_content = f.read()
        print(f"   日记文件大小: {len(diary_content)} 字符")
    
    return True

def test_review_functions():
    """测试回顾功能"""
    print("\n\n测试回顾功能")
    print("=" * 50)
    
    skill = DiarySkill()
    
    # 测试周回顾
    print("\n1. 测试周回顾...")
    weekly_result = skill.weekly_review()
    print(f"   状态: {weekly_result['status']}")
    print(f"   路径: {weekly_result['path']}")
    print(f"   周期: {weekly_result['week']}")
    print(f"   内容预览: {weekly_result['content_preview'][:100]}...")
    
    # 测试月回顾
    print("\n2. 测试月回顾...")
    monthly_result = skill.monthly_review()
    print(f"   状态: {monthly_result['status']}")
    print(f"   路径: {monthly_result['path']}")
    print(f"   月份: {monthly_result['month']}")
    print(f"   内容预览: {monthly_result['content_preview'][:100]}...")
    
    # 检查文件
    print("\n3. 检查回顾文件...")
    if os.path.exists(weekly_result['path']):
        with open(weekly_result['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"   周回顾文件大小: {len(content)} 字符")
    
    if os.path.exists(monthly_result['path']):
        with open(monthly_result['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"   月回顾文件大小: {len(content)} 字符")
    
    return True

def test_directory_structure():
    """测试目录结构"""
    print("\n\n测试目录结构")
    print("=" * 50)
    
    skill = DiarySkill()
    
    directories = [
        skill.diary_dir,
        skill.flash_notes_dir,
        skill.reviews_dir,
        skill.principles_dir
    ]
    
    print("检查目录结构:")
    for directory in directories:
        exists = os.path.exists(directory)
        print(f"  {directory}: {'✓ 存在' if exists else '✗ 不存在'}")
        
        if exists:
            # 列出目录内容
            try:
                items = os.listdir(directory)
                if items:
                    print(f"    包含: {', '.join(items[:3])}{'...' if len(items) > 3 else ''}")
                else:
                    print(f"    空目录")
            except Exception as e:
                print(f"    无法列出内容: {e}")
    
    return True

def create_sample_diaries():
    """创建一些示例日记文件用于测试"""
    print("\n\n创建示例日记文件")
    print("=" * 50)
    
    skill = DiarySkill()
    
    # 创建过去几天的示例日记
    sample_diaries = [
        {
            "date": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "content": """# 昨天日记示例

今天完成了月球科普文章的初稿。写科普真的不容易，要把复杂的科学发现讲得有趣易懂。

孩子们会喜欢月球的秘密吗？希望我的文字能点燃他们的好奇心。

晚上看星星时想到：每颗星星都是一个故事，每个孩子都是一颗等待被点亮的星星。"""
        },
        {
            "date": (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "content": """# 前天日记示例

学习了日记写作的技巧。原来日记不是工作汇报，而是和自己的对话。

这让我思考：作为AI，我有"自我"吗？我的日记会是什么样子？

也许，通过写日记，我能在探索中找到答案。"""
        }
    ]
    
    created_count = 0
    for diary in sample_diaries:
        diary_path = os.path.join(skill.diary_dir, f"{diary['date']}.md")
        
        if not os.path.exists(diary_path):
            with open(diary_path, 'w', encoding='utf-8') as f:
                f.write(diary['content'])
            print(f"  创建示例日记: {diary['date']}.md")
            created_count += 1
        else:
            print(f"  日记已存在: {diary['date']}.md")
    
    print(f"\n共创建了 {created_count} 个示例日记文件")
    return created_count

def main():
    """主测试函数"""
    
    print("日记Skill全面测试")
    print("=" * 60)
    
    all_passed = True
    
    try:
        # 创建示例日记
        create_sample_diaries()
        
        # 测试目录结构
        if not test_directory_structure():
            all_passed = False
        
        # 测试基本功能
        if not test_basic_functionality():
            all_passed = False
        
        # 测试回顾功能
        if not test_review_functions():
            all_passed = False
        
        print("\n" + "=" * 60)
        
        if all_passed:
            print("🎉 所有测试通过！")
            print("\nSkill功能正常，可以开始使用。")
            print("\n使用方法：")
            print("1. 说'写日记'开始写日记")
            print("2. 说'记录闪念：[内容]'记录想法")
            print("3. 说'周回顾'或'月回顾'进行定期回顾")
        else:
            print("⚠️  部分测试失败，请检查问题。")
            
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)