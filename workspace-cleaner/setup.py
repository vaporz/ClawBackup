#!/usr/bin/env python3
"""
Workspace Cleaner 安装脚本
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def setup_skill(workspace_path=None, interactive=True):
    """
    安装workspace-cleaner skill
    
    Args:
        workspace_path: 工作区路径，默认为当前目录
        interactive: 是否交互式配置
    """
    print("=" * 60)
    print("Workspace Cleaner Skill 安装程序")
    print("=" * 60)
    
    # 确定工作区路径
    if workspace_path:
        workspace = Path(workspace_path).absolute()
    else:
        workspace = Path.cwd()
    
    print(f"工作区: {workspace}")
    
    # 检查是否在OpenClaw工作区
    if not (workspace / ".openclaw").exists():
        print("警告: 未检测到OpenClaw工作区，可能安装位置不正确")
        if interactive:
            response = input("是否继续? (y/n): ").lower()
            if response != 'y':
                print("安装取消")
                return False
    
    # 创建配置目录
    config_dir = workspace / ".cleanup"
    config_dir.mkdir(exist_ok=True)
    
    # 复制配置文件
    skill_dir = Path(__file__).parent
    config_template = skill_dir / "config.yaml"
    user_config = config_dir / "config.yaml"
    
    if not user_config.exists():
        shutil.copy(config_template, user_config)
        print(f"✓ 配置文件已创建: {user_config}")
    else:
        print(f"✓ 配置文件已存在: {user_config}")
    
    # 创建归档目录
    archive_dir = workspace / "归档"
    archive_dir.mkdir(exist_ok=True)
    print(f"✓ 归档目录已创建: {archive_dir}")
    
    # 交互式配置
    if interactive:
        configure_interactive(user_config)
    
    # 创建清理脚本快捷方式
    create_shortcuts(skill_dir, workspace)
    
    # 设置定时任务
    setup_cron_job(workspace, interactive)
    
    print("\n" + "=" * 60)
    print("安装完成!")
    print("=" * 60)
    print("\n使用方法:")
    print("  1. 手动清理: python cleanup.py")
    print("  2. 模拟运行: python cleanup.py --dry-run")
    print("  3. 查看帮助: python cleanup.py --help")
    print("\n集成使用:")
    print("  1. 在OpenClaw中: '清理工作区'")
    print("  2. 定时任务: 每周日晚上10点自动清理")
    print("\n配置文件: .cleanup/config.yaml")
    print("归档目录: 归档/")
    
    return True

def configure_interactive(config_path):
    """交互式配置"""
    print("\n--- 交互式配置 ---")
    
    try:
        import yaml
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 选择清理策略
        print("\n选择清理策略:")
        print("  1. strict (严格) - 只保留核心文件")
        print("  2. balanced (平衡) - 保留核心文件和近期工作文件（推荐）")
        print("  3. loose (宽松) - 保留较多文件")
        
        choice = input("请输入选项 (1-3, 默认2): ").strip()
        if choice == '1':
            config['strategy'] = 'strict'
        elif choice == '3':
            config['strategy'] = 'loose'
        else:
            config['strategy'] = 'balanced'
        
        # 是否启用定时清理
        print("\n是否启用定时自动清理?")
        print("  每周日晚上10点自动清理工作区")
        enable_cron = input("启用定时清理? (y/n, 默认y): ").lower().strip()
        config['scheduled']['enabled'] = enable_cron != 'n'
        
        # 是否启用回收站
        print("\n是否启用回收站?")
        print("  删除文件时会先移动到回收站，保留30天")
        enable_recycle = input("启用回收站? (y/n, 默认y): ").lower().strip()
        config['recycle_bin']['enabled'] = enable_recycle != 'n'
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print("✓ 配置已保存")
        
    except ImportError:
        print("警告: 未安装PyYAML，跳过交互式配置")
        print("请手动编辑配置文件: .cleanup/config.yaml")
    except Exception as e:
        print(f"配置保存失败: {e}")

def create_shortcuts(skill_dir, workspace):
    """创建快捷方式"""
    # 创建清理脚本的符号链接或副本
    cleanup_script = skill_dir / "cleanup.py"
    workspace_cleanup = workspace / "cleanup.py"
    
    try:
        if not workspace_cleanup.exists():
            # 尝试创建符号链接
            try:
                workspace_cleanup.symlink_to(cleanup_script)
                print("✓ 清理脚本符号链接已创建")
            except:
                # 回退到复制
                shutil.copy(cleanup_script, workspace_cleanup)
                print("✓ 清理脚本已复制到工作区")
        
        # 使脚本可执行
        workspace_cleanup.chmod(0o755)
        
    except Exception as e:
        print(f"创建快捷方式失败: {e}")

def setup_cron_job(workspace, interactive=True):
    """设置定时任务"""
    if not interactive:
        return
    
    print("\n--- 定时任务设置 ---")
    print("需要设置OpenClaw cron任务来自动清理")
    print("每周日晚上10点执行清理")
    
    response = input("\n是否现在设置定时任务? (y/n, 默认y): ").lower().strip()
    if response == 'n':
        print("跳过定时任务设置")
        print("提示: 可以稍后手动设置: openclaw cron create ...")
        return
    
    # 生成cron命令
    cron_command = f"cd {workspace} && python cleanup.py"
    
    print("\n请手动执行以下命令创建定时任务:")
    print("=" * 60)
    print(f"openclaw cron create \\")
    print(f'  --name "工作区自动清理" \\')
    print(f'  --schedule "0 22 * * 0" \\')  # 每周日22:00
    print(f'  --command "{cron_command}" \\')
    print(f'  --delivery.mode "announce"')
    print("=" * 60)
    
    print("\n或者使用以下简化命令:")
    print(f'openclaw cron create --name "工作区自动清理" --schedule "0 22 * * 0" --command "{cron_command}"')

def quick_setup():
    """快速安装（非交互式）"""
    parser = argparse.ArgumentParser(description='快速安装workspace-cleaner')
    parser.add_argument('--workspace', '-w', help='工作区路径', default=os.getcwd())
    parser.add_argument('--strategy', '-s', choices=['strict', 'balanced', 'loose'],
                       default='balanced', help='清理策略')
    parser.add_argument('--no-cron', action='store_true', help='不设置定时任务')
    parser.add_argument('--no-recycle', action='store_true', help='不启用回收站')
    
    args = parser.parse_args()
    
    print("执行快速安装...")
    
    # 非交互式安装
    success = setup_skill(args.workspace, interactive=False)
    
    if success:
        # 应用命令行参数
        config_path = Path(args.workspace) / ".cleanup" / "config.yaml"
        
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            config['strategy'] = args.strategy
            config['scheduled']['enabled'] = not args.no_cron
            config['recycle_bin']['enabled'] = not args.no_recycle
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            
            print("✓ 配置已应用")
            
        except Exception as e:
            print(f"配置应用失败: {e}")
    
    return success

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Workspace Cleaner 安装程序')
    parser.add_argument('--workspace', '-w', help='工作区路径', default=os.getcwd())
    parser.add_argument('--quick', '-q', action='store_true', help='快速安装（非交互式）')
    parser.add_argument('--configure', '-c', action='store_true', help='只进行配置，不安装')
    
    args = parser.parse_args()
    
    if args.quick:
        # 传递参数给quick_setup
        import sys
        quick_args = ['--workspace', args.workspace]
        sys.argv = [sys.argv[0]] + quick_args
        quick_setup()
    elif args.configure:
        # 只配置
        config_path = Path(args.workspace) / ".cleanup" / "config.yaml"
        if config_path.exists():
            configure_interactive(config_path)
        else:
            print("错误: 配置文件不存在，请先安装")
            sys.exit(1)
    else:
        # 完整安装
        setup_skill(args.workspace, interactive=True)

if __name__ == '__main__':
    main()