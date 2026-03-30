#!/usr/bin/env python3
"""
Workspace Cleaner 测试脚本
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加父目录到路径，以便导入cleanup模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from cleanup import WorkspaceCleaner

def create_test_workspace():
    """创建测试工作区"""
    test_dir = tempfile.mkdtemp(prefix="test_workspace_")
    print(f"创建测试工作区: {test_dir}")
    
    # 创建测试文件
    test_files = [
        # 核心文件
        ("IDENTITY.md", "身份文件"),
        ("SOUL.md", "灵魂文件"),
        ("AGENTS.md", "团队文件"),
        
        # 临时文件
        ("temp_file.tmp", "临时文件"),
        ("backup.bak", "备份文件"),
        ("app.log", "日志文件"),
        
        # 版本文件
        ("report-v1.md", "报告版本1"),
        ("report-v2.md", "报告版本2"),
        ("report_最新版.md", "最新报告"),
        
        # 草稿文件
        ("项目草稿.md", "项目草稿"),
        ("draft_proposal.md", "提案草稿"),
        
        # 测试文件
        ("test_function.py", "测试代码"),
        ("示例文件.md", "示例文件"),
        
        # 其他文件
        ("日常工作记录.md", "工作记录"),
        ("会议纪要.docx", "会议记录"),
    ]
    
    for filename, content in test_files:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {content}\n\n这是测试内容。")
    
    # 创建子目录
    subdirs = ['项目A', '项目B', '缓存']
    for subdir in subdirs:
        os.makedirs(os.path.join(test_dir, subdir), exist_ok=True)
        
        # 在子目录中创建一些文件
        for i in range(3):
            filepath = os.path.join(test_dir, subdir, f"文件{i}.txt")
            with open(filepath, 'w') as f:
                f.write(f"子目录 {subdir} 中的文件 {i}")
    
    return test_dir

def test_file_classification():
    """测试文件分类"""
    print("\n" + "="*60)
    print("测试文件分类")
    print("="*60)
    
    test_dir = create_test_workspace()
    
    try:
        cleaner = WorkspaceCleaner(test_dir)
        
        # 测试单个文件分类
        test_cases = [
            ("IDENTITY.md", ("core", "keep")),
            ("temp_file.tmp", ("temp", "archive")),
            ("report-v1.md", ("version", "archive")),
            ("项目草稿.md", ("draft", "archive")),
            ("test_function.py", ("test", "archive")),
            ("日常工作记录.md", ("other", "keep")),
        ]
        
        print("\n文件分类测试:")
        for filename, expected in test_cases:
            filepath = os.path.join(test_dir, filename)
            if os.path.exists(filepath):
                result = cleaner._get_file_type(filepath)
                status = "✓" if result == expected else "✗"
                print(f"  {status} {filename:20} -> {result} (期望: {expected})")
            else:
                print(f"  ✗ {filename:20} 文件不存在")
        
        return True
        
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"\n清理测试目录: {test_dir}")

def test_cleanup_dry_run():
    """测试清理模拟运行"""
    print("\n" + "="*60)
    print("测试清理模拟运行")
    print("="*60)
    
    test_dir = create_test_workspace()
    
    try:
        print(f"测试工作区: {test_dir}")
        print(f"初始文件数: {len(list(Path(test_dir).rglob('*')))}")
        
        # 执行模拟清理
        cleaner = WorkspaceCleaner(test_dir)
        stats = cleaner.cleanup(dry_run=True)
        
        print("\n模拟清理结果:")
        print(f"  总文件数: {stats['total_files']}")
        print(f"  保留文件: {stats['kept_files']}")
        print(f"  归档文件: {stats['archived_files']}")
        print(f"  删除文件: {stats['deleted_files']}")
        
        # 验证统计
        total = stats['kept_files'] + stats['archived_files'] + stats['deleted_files']
        assert total == stats['processed_files'], "统计不一致"
        
        print("✓ 模拟清理测试通过")
        return True
        
    except AssertionError as e:
        print(f"✗ 测试失败: {e}")
        return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

def test_actual_cleanup():
    """测试实际清理"""
    print("\n" + "="*60)
    print("测试实际清理")
    print("="*60)
    
    test_dir = create_test_workspace()
    
    try:
        print(f"测试工作区: {test_dir}")
        
        # 记录初始状态
        initial_files = list(Path(test_dir).rglob('*'))
        initial_count = len([f for f in initial_files if f.is_file()])
        print(f"初始文件数: {initial_count}")
        
        # 执行实际清理
        cleaner = WorkspaceCleaner(test_dir)
        stats = cleaner.cleanup(dry_run=False)
        
        # 检查归档目录
        archive_dir = Path(test_dir) / "归档"
        if archive_dir.exists():
            archived_files = list(archive_dir.rglob('*'))
            archived_count = len([f for f in archived_files if f.is_file()])
            print(f"归档文件数: {archived_count}")
        else:
            print("归档目录不存在")
            archived_count = 0
        
        # 检查剩余文件
        remaining_files = list(Path(test_dir).rglob('*'))
        # 排除归档目录
        remaining_files = [f for f in remaining_files if not str(f).startswith(str(archive_dir))]
        remaining_count = len([f for f in remaining_files if f.is_file()])
        print(f"剩余文件数: {remaining_count}")
        
        # 验证
        print("\n验证结果:")
        
        # 核心文件应该保留
        core_files = ['IDENTITY.md', 'SOUL.md', 'AGENTS.md']
        for core_file in core_files:
            filepath = Path(test_dir) / core_file
            if filepath.exists():
                print(f"  ✓ 核心文件保留: {core_file}")
            else:
                print(f"  ✗ 核心文件丢失: {core_file}")
        
        # 临时文件应该被归档
        temp_files = ['temp_file.tmp', 'backup.bak', 'app.log']
        temp_found = False
        for temp_file in temp_files:
            # 检查是否在归档目录中
            for archived in archived_files:
                if temp_file in str(archived):
                    temp_found = True
                    break
        if temp_found:
            print("  ✓ 临时文件已归档")
        else:
            print("  ✗ 临时文件未找到")
        
        print("✓ 实际清理测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

def test_recycle_bin():
    """测试回收站功能"""
    print("\n" + "="*60)
    print("测试回收站")
    print("="*60)
    
    test_dir = create_test_workspace()
    
    try:
        # 创建自定义配置，启用回收站
        config_content = """
strategy: "balanced"
recycle_bin:
  enabled: true
  retention_days: 7
  auto_cleanup: false
"""
        
        config_path = Path(test_dir) / "test_config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        # 创建清理器
        cleaner = WorkspaceCleaner(test_dir, str(config_path))
        
        # 测试移动到回收站
        test_file = Path(test_dir) / "test_delete.txt"
        test_file.write_text("测试删除的文件")
        
        print(f"测试文件: {test_file}")
        print(f"文件大小: {test_file.stat().st_size} 字节")
        
        # 移动到回收站
        success = cleaner._move_to_recycle_bin(str(test_file))
        
        if success:
            print("✓ 文件成功移动到回收站")
            
            # 检查回收站
            recycle_bin = Path(cleaner.recycle_bin_path)
            if recycle_bin.exists():
                items = list(recycle_bin.glob("*"))
                print(f"回收站文件数: {len([i for i in items if not i.name.endswith('.meta.json')])}")
                
                # 检查元数据
                meta_files = list(recycle_bin.glob("*.meta.json"))
                if meta_files:
                    print(f"元数据文件数: {len(meta_files)}")
                    print("✓ 回收站功能正常")
                else:
                    print("✗ 未找到元数据文件")
            else:
                print("✗ 回收站目录不存在")
        else:
            print("✗ 移动到回收站失败")
        
        return success
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

def run_all_tests():
    """运行所有测试"""
    print("开始Workspace Cleaner测试套件")
    print("="*60)
    
    tests = [
        ("文件分类测试", test_file_classification),
        ("模拟清理测试", test_cleanup_dry_run),
        ("实际清理测试", test_actual_cleanup),
        ("回收站测试", test_recycle_bin),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n▶ 执行: {test_name}")
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = 0
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {status}: {test_name}")
        if success:
            passed += 1
    
    total = len(results)
    print(f"\n通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过!")
        return True
    else:
        print("⚠ 部分测试失败")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Workspace Cleaner 测试脚本')
    parser.add_argument('--test', '-t', choices=['all', 'classification', 'dry-run', 'actual', 'recycle'],
                       default='all', help='选择测试项目')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.test == 'all':
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif args.test == 'classification':
        success = test_file_classification()
    elif args.test == 'dry-run':
        success = test_cleanup_dry_run()
    elif args.test == 'actual':
        success = test_actual_cleanup()
    elif args.test == 'recycle':
        success = test_recycle_bin()
    else:
        print(f"未知测试: {args.test}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()