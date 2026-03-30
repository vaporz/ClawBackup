#!/usr/bin/env python3
"""
Workspace Cleaner - 核心清理逻辑
帮助agent保持工作区整洁，建立"吃完饭擦桌子"的好习惯。
"""

import os
import sys
import shutil
import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path
import argparse
from typing import Dict, List, Tuple, Optional

class WorkspaceCleaner:
    """工作区清理器"""
    
    def __init__(self, workspace_path: str = None, config_path: str = None):
        """
        初始化清理器
        
        Args:
            workspace_path: 工作区路径，默认为当前工作区
            config_path: 配置文件路径
        """
        self.workspace_path = workspace_path or os.getcwd()
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'config.yaml'
        )
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化目录
        self._init_directories()
        
        # 清理统计
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'kept_files': 0,
            'archived_files': 0,
            'deleted_files': 0,
            'space_saved': 0,
            'problems_found': []
        }
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            'strategy': 'balanced',
            'retention': {
                'core_files': 'keep',
                'temp_files': 'archive_30d',
                'version_files': 'keep_latest',
                'cache_files': 'delete_7d'
            },
            'archive': {
                'location': './归档',
                'organization': 'monthly',
                'keep_metadata': True
            },
            'recycle_bin': {
                'enabled': True,
                'retention_days': 30,
                'auto_cleanup': True
            },
            'notifications': {
                'on_complete': True,
                'on_problem': True,
                'on_threshold': True
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                # 合并配置
                config = {**default_config, **user_config}
            else:
                config = default_config
        except Exception as e:
            print(f"警告：加载配置文件失败，使用默认配置: {e}")
            config = default_config
        
        return config
    
    def _init_directories(self):
        """初始化必要的目录"""
        # 归档目录
        archive_path = self.config['archive']['location']
        if not os.path.isabs(archive_path):
            archive_path = os.path.join(self.workspace_path, archive_path)
        
        self.archive_path = archive_path
        os.makedirs(self.archive_path, exist_ok=True)
        
        # 回收站目录
        self.recycle_bin_path = os.path.join(self.archive_path, 'recycle-bin')
        os.makedirs(self.recycle_bin_path, exist_ok=True)
        
        # 按年月创建归档子目录
        today = datetime.now()
        year_month = today.strftime('%Y-%m')
        self.monthly_archive = os.path.join(self.archive_path, year_month)
        os.makedirs(self.monthly_archive, exist_ok=True)
        
        # 创建分类子目录
        for subdir in ['drafts', 'tests', 'versions', 'temp']:
            os.makedirs(os.path.join(self.monthly_archive, subdir), exist_ok=True)
    
    def _get_file_type(self, filepath: str) -> Tuple[str, str]:
        """
        识别文件类型
        
        Returns:
            (文件类型, 建议操作)
        """
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()
        
        # 核心文件规则
        core_files = [
            'IDENTITY.md', 'SOUL.md', 'USER.md', 'AGENTS.md',
            'MEMORY.md', 'TOOLS.md', 'HEARTBEAT.md'
        ]
        
        if filename in core_files:
            return 'core', 'keep'
        
        # 临时文件规则
        temp_patterns = ['.tmp', '.temp', '.bak', '.backup', '.log', '.debug']
        if any(filename.endswith(pattern) for pattern in temp_patterns):
            return 'temp', 'archive'
        
        # 版本文件识别（同一文件多个版本）
        version_patterns = ['-v', '_v', '版本', 'version', '副本', 'copy']
        if any(pattern in filename.lower() for pattern in version_patterns):
            return 'version', 'archive'
        
        # 测试文件
        test_patterns = ['test_', '_test.', 'debug_', '示例', 'example']
        if any(filename.lower().startswith(pattern) for pattern in test_patterns[:3]) or \
           any(pattern in filename.lower() for pattern in test_patterns[3:]):
            return 'test', 'archive'
        
        # 草稿文件
        draft_patterns = ['草稿', 'draft', '初稿', 'rough']
        if any(pattern in filename.lower() for pattern in draft_patterns):
            return 'draft', 'archive'
        
        # 默认：保留
        return 'other', 'keep'
    
    def _should_process_file(self, filepath: str) -> bool:
        """判断是否应该处理该文件"""
        # 跳过目录
        if os.path.isdir(filepath):
            return False
        
        # 跳过隐藏文件
        filename = os.path.basename(filepath)
        if filename.startswith('.'):
            return False
        
        # 跳过skill目录
        if '/skills/' in filepath.replace('\\', '/'):
            return False
        
        # 跳过归档目录
        if filepath.startswith(self.archive_path):
            return False
        
        return True
    
    def _get_archive_path(self, filepath: str, file_type: str) -> str:
        """获取归档路径"""
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 根据文件类型选择归档子目录
        if file_type == 'draft':
            subdir = 'drafts'
        elif file_type == 'test':
            subdir = 'tests'
        elif file_type == 'version':
            subdir = 'versions'
        else:
            subdir = 'temp'
        
        # 添加时间戳避免重名
        name, ext = os.path.splitext(filename)
        archived_name = f"{name}_{timestamp}{ext}"
        
        return os.path.join(self.monthly_archive, subdir, archived_name)
    
    def _move_to_recycle_bin(self, filepath: str) -> bool:
        """移动到回收站"""
        try:
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            recycle_path = os.path.join(self.recycle_bin_path, f"{filename}_{timestamp}")
            
            shutil.move(filepath, recycle_path)
            
            # 记录删除元数据
            metadata = {
                'original_path': filepath,
                'deleted_at': datetime.now().isoformat(),
                'file_size': os.path.getsize(recycle_path) if os.path.exists(recycle_path) else 0
            }
            
            metadata_path = recycle_path + '.meta.json'
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            self.stats['problems_found'].append(f"移动到回收站失败 {filepath}: {e}")
            return False
    
    def _cleanup_recycle_bin(self):
        """清理过期的回收站文件"""
        if not self.config['recycle_bin']['auto_cleanup']:
            return
        
        retention_days = self.config['recycle_bin']['retention_days']
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        for item in os.listdir(self.recycle_bin_path):
            item_path = os.path.join(self.recycle_bin_path, item)
            
            # 跳过元数据文件
            if item.endswith('.meta.json'):
                continue
            
            # 获取删除时间
            metadata_path = item_path + '.meta.json'
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    deleted_at = datetime.fromisoformat(metadata['deleted_at'])
                    
                    if deleted_at < cutoff_date:
                        # 永久删除
                        os.remove(item_path)
                        os.remove(metadata_path)
                        print(f"清理过期回收站文件: {item}")
                except Exception as e:
                    print(f"清理回收站文件失败 {item}: {e}")
    
    def scan_workspace(self) -> List[str]:
        """扫描工作区文件"""
        files = []
        
        for root, dirs, filenames in os.walk(self.workspace_path):
            # 跳过归档目录
            if root.startswith(self.archive_path):
                continue
            
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if self._should_process_file(filepath):
                    files.append(filepath)
        
        self.stats['total_files'] = len(files)
        return files
    
    def process_file(self, filepath: str):
        """处理单个文件"""
        self.stats['processed_files'] += 1
        
        try:
            file_type, action = self._get_file_type(filepath)
            file_size = os.path.getsize(filepath)
            
            if action == 'keep':
                self.stats['kept_files'] += 1
                print(f"保留: {os.path.basename(filepath)} ({file_type})")
                
            elif action == 'archive':
                # 归档文件
                archive_path = self._get_archive_path(filepath, file_type)
                shutil.move(filepath, archive_path)
                self.stats['archived_files'] += 1
                self.stats['space_saved'] += file_size
                print(f"归档: {os.path.basename(filepath)} -> {os.path.relpath(archive_path, self.workspace_path)}")
                
            elif action == 'delete':
                # 安全删除到回收站
                if self.config['recycle_bin']['enabled']:
                    if self._move_to_recycle_bin(filepath):
                        self.stats['deleted_files'] += 1
                        self.stats['space_saved'] += file_size
                        print(f"删除到回收站: {os.path.basename(filepath)}")
                else:
                    os.remove(filepath)
                    self.stats['deleted_files'] += 1
                    self.stats['space_saved'] += file_size
                    print(f"删除: {os.path.basename(filepath)}")
                    
        except Exception as e:
            problem = f"处理文件失败 {filepath}: {e}"
            self.stats['problems_found'].append(problem)
            print(f"错误: {problem}")
    
    def cleanup(self, dry_run: bool = False) -> Dict:
        """
        执行清理
        
        Args:
            dry_run: 模拟运行，不实际执行
            
        Returns:
            清理统计信息
        """
        print(f"开始清理工作区: {self.workspace_path}")
        print(f"策略: {self.config['strategy']}")
        print("-" * 50)
        
        # 扫描文件
        files = self.scan_workspace()
        print(f"找到 {len(files)} 个待处理文件")
        
        if dry_run:
            print("\n模拟运行结果（不实际执行）:")
            for filepath in files[:10]:  # 只显示前10个
                file_type, action = self._get_file_type(filepath)
                print(f"  {action:8} {file_type:10} {os.path.basename(filepath)}")
            
            if len(files) > 10:
                print(f"  ... 还有 {len(files) - 10} 个文件")
            
            # 模拟统计
            self.stats['total_files'] = len(files)
            self.stats['processed_files'] = len(files)
            self.stats['kept_files'] = sum(1 for f in files if self._get_file_type(f)[1] == 'keep')
            self.stats['archived_files'] = sum(1 for f in files if self._get_file_type(f)[1] == 'archive')
            self.stats['deleted_files'] = sum(1 for f in files if self._get_file_type(f)[1] == 'delete')
            
        else:
            # 实际执行清理
            for filepath in files:
                self.process_file(filepath)
            
            # 清理回收站
            self._cleanup_recycle_bin()
        
        # 生成报告
        self._generate_report()
        
        return self.stats
    
    def _generate_report(self):
        """生成清理报告"""
        print("\n" + "=" * 50)
        print("清理完成报告")
        print("=" * 50)
        
        print(f"总文件数: {self.stats['total_files']}")
        print(f"处理文件: {self.stats['processed_files']}")
        print(f"保留文件: {self.stats['kept_files']}")
        print(f"归档文件: {self.stats['archived_files']}")
        print(f"删除文件: {self.stats['deleted_files']}")
        
        space_saved_mb = self.stats['space_saved'] / (1024 * 1024)
        if space_saved_mb > 0:
            print(f"节省空间: {space_saved_mb:.2f} MB")
        
        if self.stats['problems_found']:
            print(f"\n发现问题 ({len(self.stats['problems_found'])} 个):")
            for problem in self.stats['problems_found'][:5]:  # 只显示前5个
                print(f"  - {problem}")
            if len(self.stats['problems_found']) > 5:
                print(f"  ... 还有 {len(self.stats['problems_found']) - 5} 个问题")
        
        # 保存报告到文件
        report_path = os.path.join(self.archive_path, '清理报告.json')
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'workspace': self.workspace_path,
            'strategy': self.config['strategy'],
            'stats': self.stats,
            'archive_location': self.archive_path
        }
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            print(f"\n详细报告已保存: {report_path}")
        except Exception as e:
            print(f"\n保存报告失败: {e}")
    
    def restore_from_recycle_bin(self, pattern: str = None):
        """从回收站恢复文件"""
        print("回收站内容:")
        items = []
        
        for item in os.listdir(self.recycle_bin_path):
            if item.endswith('.meta.json'):
                continue
            
            item_path = os.path.join(self.recycle_bin_path, item)
            metadata_path = item_path + '.meta.json'
            
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    items.append({
                        'filename': item,
                        'original_path': metadata.get('original_path', '未知'),
                        'deleted_at': metadata.get('deleted_at', '未知'),
                        'size': os.path.getsize(item_path) if os.path.exists(item_path) else 0
                    })
                except Exception as e:
                    print(f"读取元数据失败 {item}: {e}")
        
        if not items:
            print("回收站为空")
            return
        
        # 显示回收站内容
        for i, item in enumerate(items, 1):
            print(f"{i:2}. {item['filename']:30} 原路径: {item['original_path']}")
        
        # 如果提供了模式，直接恢复匹配的文件
        if pattern:
            matched = [item for item in items if pattern in item['filename']]
            if matched:
                for item in matched:
                    self._restore_item(item['filename'])
            else:
                print(f"未找到匹配 '{pattern}' 的文件")
        
        else:
            # 交互式恢复
            choice = input("\n输入要恢复的文件编号 (多个用逗号分隔，或 'all' 恢复所有): ").strip()
            
            if choice.lower() == 'all':
                for item in items:
                    self._restore_item(item['filename'])
            elif choice:
                try:
                    indices = [int(idx.strip()) - 1 for idx in choice.split(',')]
                    for idx in indices:
                        if 0 <= idx < len(items):
                            self._restore_item(items[idx]['filename'])
                except ValueError:
                    print("输入无效")
    
    def _restore_item(self, filename: str):
        """恢复单个文件"""
        item_path = os.path.join(self.recycle_bin_path, filename)
        metadata_path = item_path + '.meta.json'
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            original_path = metadata.get('original_path')
            if not original_path:
                print(f"无法恢复 {filename}: 原路径信息缺失")
                return
            
            # 检查原路径是否已存在
            if os.path.exists(original_path):
                backup_path = original_path + '.restore_backup'
                shutil.move(original_path, backup_path)
                print(f"原文件已备份到: {backup_path}")
            
            # 恢复文件
            shutil.move(item_path, original_path)
            os.remove(metadata_path)
            print(f"已恢复: {filename} -> {original_path}")
            
        except Exception as e:
            print(f"恢复文件失败 {filename}: {e}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='工作区清理工具')
    parser.add_argument('--workspace', '-w', help='工作区路径', default=os.getcwd())
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--dry-run', '-d', action='store_true', help='模拟运行，不实际执行')
    parser.add_argument('--strategy', '-s', choices=['strict', 'balanced', 'loose'], 
                       help='清理策略')
    parser.add_argument('--restore', '-r', help='从回收站恢复文件（支持模式匹配）')
    parser.add_argument('--list-recycle', '-l', action='store_true', help='列出回收站内容')
    
    args = parser.parse_args()
    
    # 创建清理器
    cleaner = WorkspaceCleaner(args.workspace, args.config)
    
    # 应用命令行策略
    if args.strategy:
        cleaner.config['strategy'] = args.strategy
    
    # 执行相应操作
    if args.restore:
        cleaner.restore_from_recycle_bin(args.restore)
    elif args.list_recycle:
        cleaner.restore_from_recycle_bin()  # 不传参数会显示列表
    else:
        stats = cleaner.cleanup(dry_run=args.dry_run)
        
        # 返回退出码
        if stats['problems_found']:
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == '__main__':
    main()