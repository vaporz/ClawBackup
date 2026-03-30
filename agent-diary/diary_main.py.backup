#!/usr/bin/env python3
"""
Agent Diary Skill Main Script
处理日记写作、闪念记录、回顾提炼等功能
Handles diary writing, flash notes recording, review and extraction functions
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class DiarySkill:
    """日记Skill核心类"""
    
    def __init__(self, workspace_path: str = None):
        """初始化日记Skill
        
        Args:
            workspace_path: 工作空间路径，必须提供
        """
        if workspace_path is None:
            # 尝试从环境变量获取当前agent的workspace
            env_workspace = os.environ.get("OPENCLAW_WORKSPACE")
            if env_workspace:
                self.workspace_path = env_workspace
            else:
                # 如果环境变量也没有，使用传统方式但记录警告
                default_path = os.path.expanduser("~/.openclaw/workspace")
                if os.path.exists(default_path):
                    self.workspace_path = default_path
                else:
                    # 最后尝试猜测当前agent的workspace
                    import inspect
                    try:
                        # 尝试获取调用者的文件路径来推断workspace
                        frame = inspect.currentframe()
                        caller_frame = frame.f_back
                        caller_file = caller_frame.f_code.co_filename
                        # 从文件路径中提取可能的workspace
                        if "/.openclaw/agents/" in caller_file:
                            parts = caller_file.split("/.openclaw/agents/")
                            if len(parts) > 1:
                                agent_part = parts[1].split("/")[0]
                                guessed_path = os.path.expanduser(f"~/.openclaw/workspace-{agent_part}")
                                if os.path.exists(guessed_path):
                                    self.workspace_path = guessed_path
                                else:
                                    raise ValueError(f"无法确定workspace路径。请提供workspace_path参数。尝试的路径不存在: {guessed_path}")
                            else:
                                raise ValueError("无法确定workspace路径。请提供workspace_path参数。")
                        else:
                            raise ValueError("无法确定workspace路径。请提供workspace_path参数。")
                    except Exception as e:
                        raise ValueError(f"无法确定workspace路径: {e}. 请显式提供workspace_path参数。")
        else:
            self.workspace_path = workspace_path
            
        # 日记相关目录（使用隐藏文件夹）
        self.diary_dir = os.path.join(self.workspace_path, ".diary")
        self.flash_notes_dir = os.path.join(self.diary_dir, "flash-notes")
        self.reviews_dir = os.path.join(self.diary_dir, "reviews")
        self.principles_dir = os.path.join(self.diary_dir, "principles")
        
        # 创建必要的目录
        self._create_directories()
        
        # 当前日期
        self.today = datetime.datetime.now()
        self.date_str = self.today.strftime("%Y-%m-%d")
        
    def _create_directories(self):
        """创建必要的目录结构"""
        directories = [
            self.diary_dir,
            self.flash_notes_dir,
            self.reviews_dir,
            self.principles_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def get_today_diary_path(self) -> str:
        """获取今天日记文件的路径（按年月分层）"""
        year = self.today.strftime("%Y")
        month = self.today.strftime("%m")
        
        # 创建年月目录
        year_month_dir = os.path.join(self.diary_dir, year, month)
        os.makedirs(year_month_dir, exist_ok=True)
        
        return os.path.join(year_month_dir, f"{self.date_str}.md")
    
    def get_today_flash_notes_path(self) -> str:
        """获取今天闪念记录文件的路径"""
        return os.path.join(self.flash_notes_dir, f"{self.date_str}-flash.md")
    
    def write_diary(self, memory_content: str = "", flash_notes: str = "") -> Dict[str, Any]:
        """写今天的日记
        
        Args:
            memory_content: 当天的memory内容
            flash_notes: 当天的闪念记录
            
        Returns:
            包含日记信息和路径的字典
        """
        diary_path = self.get_today_diary_path()
        
        # 检查是否已经写过今天的日记
        if os.path.exists(diary_path):
            with open(diary_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            return {
                "status": "already_exists",
                "path": diary_path,
                "content": existing_content[:500] + "..." if len(existing_content) > 500 else existing_content
            }
        
        # 准备日记内容
        time_str = self.today.strftime("%Y年%m月%d日 %H:%M")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][self.today.weekday()]
        
        # 构建日记内容
        diary_content = f"""# {self.date_str} {weekday}

现在是{time_str}，开始写今天的日记。

## 今日回顾

"""
        
        # 如果有memory内容，添加简要回顾
        if memory_content:
            diary_content += "### 从工作记录中回顾\n"
            # 这里可以添加对memory内容的简要总结
            diary_content += "（今天的工作和学习记录已查看）\n\n"
        
        # 如果有闪念记录，整合进来
        if flash_notes:
            diary_content += "### 今天的闪念\n"
            diary_content += flash_notes + "\n\n"
        
        # 添加写作引导
        diary_content += """## 开始写作

现在，放松地开始写吧。可以思考：

1. 今天发生了什么值得记录的事？
2. 有什么想吐槽或想夸的？
3. 有什么新的感悟或思考？
4. 此刻的感受是什么？
5. 这件事让我想起了什么？

---

"""
        
        # 写入文件
        with open(diary_path, 'w', encoding='utf-8') as f:
            f.write(diary_content)
        
        return {
            "status": "created",
            "path": diary_path,
            "content": diary_content
        }
    
    def record_flash_note(self, note: str) -> Dict[str, Any]:
        """记录一个闪念
        
        Args:
            note: 闪念内容
            
        Returns:
            包含记录信息的字典
        """
        flash_path = self.get_today_flash_notes_path()
        
        # 读取现有的闪念记录
        existing_notes = []
        if os.path.exists(flash_path):
            with open(flash_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                if existing_content.strip():
                    existing_notes = existing_content.strip().split('\n')
        
        # 添加时间戳
        time_str = datetime.datetime.now().strftime("%H:%M")
        new_note = f"[{time_str}] {note}"
        
        # 添加到列表并保存
        existing_notes.append(new_note)
        
        with open(flash_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(existing_notes))
        
        return {
            "status": "recorded",
            "path": flash_path,
            "note": new_note,
            "total_notes": len(existing_notes)
        }
    
    def get_flash_notes(self) -> List[str]:
        """获取今天的闪念记录
        
        Returns:
            闪念列表
        """
        flash_path = self.get_today_flash_notes_path()
        
        if not os.path.exists(flash_path):
            return []
        
        with open(flash_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return []
        
        return [note.strip() for note in content.strip().split('\n') if note.strip()]
    
    def weekly_review(self) -> Dict[str, Any]:
        """进行周回顾
        
        Returns:
            回顾结果
        """
        # 获取本周的日期范围
        today = datetime.datetime.now()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        
        start_str = start_of_week.strftime("%Y-%m-%d")
        end_str = end_of_week.strftime("%Y-%m-%d")
        week_str = start_of_week.strftime("%Y-%m-周回顾")
        
        review_path = os.path.join(self.reviews_dir, f"{week_str}.md")
        
        # 收集本周的日记（支持新的分层结构）
        week_diaries = []
        current = start_of_week
        while current <= end_of_week:
            # 构建分层路径
            year = current.strftime("%Y")
            month = current.strftime("%m")
            diary_path = os.path.join(self.diary_dir, year, month, f"{current.strftime('%Y-%m-%d')}.md")
            
            # 也检查旧路径（兼容性）
            old_diary_path = os.path.join(self.diary_dir, f"{current.strftime('%Y-%m-%d')}.md")
            
            if os.path.exists(diary_path):
                with open(diary_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                week_diaries.append({
                    "date": current.strftime("%Y-%m-%d"),
                    "content": content
                })
            elif os.path.exists(old_diary_path):
                # 如果旧路径存在，也读取（兼容旧文件）
                with open(old_diary_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                week_diaries.append({
                    "date": current.strftime("%Y-%m-%d"),
                    "content": content
                })
                
            current += datetime.timedelta(days=1)
        
        # 构建回顾内容
        review_content = f"""# {week_str} ({start_str} 至 {end_str})

## 本周日记概览

本周共写了 {len(week_diaries)} 篇日记。

### 主要主题
（从日记中识别重复出现的主题）

### 情绪趋势
（分析本周的情绪变化）

### 重要学习
1. 
2. 
3. 

### 值得记录的瞬间
- 

## 反思与提炼

### 本周的成长
- 

### 遇到的挑战
- 

### 下周的期待
- 

## 原则提炼

从本周经历中，可以提炼出什么人生原则？

1. 
2. 

---
*回顾时间：{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}*
"""
        
        # 写入回顾文件
        with open(review_path, 'w', encoding='utf-8') as f:
            f.write(review_content)
        
        return {
            "status": "review_created",
            "path": review_path,
            "week": f"{start_str} 至 {end_str}",
            "diary_count": len(week_diaries),
            "content_preview": review_content[:500] + "..." if len(review_content) > 500 else review_content
        }
    
    def migrate_old_diaries(self) -> Dict[str, Any]:
        """迁移旧的日记文件到新的分层结构
        
        Returns:
            迁移结果
        """
        migrated_files = []
        failed_files = []
        
        # 扫描.diary目录下的所有.md文件（排除子目录）
        for filename in os.listdir(self.diary_dir):
            if filename.endswith('.md') and os.path.isfile(os.path.join(self.diary_dir, filename)):
                # 尝试解析日期
                try:
                    # 文件名格式：YYYY-MM-DD.md
                    date_str = filename[:-3]  # 去掉.md
                    year = date_str[:4]
                    month = date_str[5:7]
                    
                    # 验证日期格式
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    
                    # 目标路径
                    target_dir = os.path.join(self.diary_dir, year, month)
                    os.makedirs(target_dir, exist_ok=True)
                    target_path = os.path.join(target_dir, filename)
                    source_path = os.path.join(self.diary_dir, filename)
                    
                    # 移动文件
                    if not os.path.exists(target_path):
                        os.rename(source_path, target_path)
                        migrated_files.append(filename)
                    else:
                        # 目标文件已存在，可能是重复迁移
                        failed_files.append(f"{filename} (目标文件已存在)")
                        
                except (ValueError, IndexError):
                    # 不是日期格式的文件，不迁移
                    failed_files.append(f"{filename} (不是日期格式)")
        
        return {
            "status": "migration_completed",
            "migrated": migrated_files,
            "failed": failed_files,
            "total_migrated": len(migrated_files),
            "total_failed": len(failed_files)
        }
    
    def monthly_review(self) -> Dict[str, Any]:
        """进行月回顾
        
        Returns:
            回顾结果
        """
        today = datetime.datetime.now()
        month_str = today.strftime("%Y-%m")
        
        review_path = os.path.join(self.reviews_dir, f"{month_str}-月回顾.md")
        
        # 构建回顾内容
        review_content = f"""# {month_str} 月回顾

## 本月概览

### 日记统计
- 总日记篇数：[需要统计]
- 平均日记长度：[需要统计]

### 主题分析
1. 
2. 
3. 

### 情绪地图
（绘制本月的情绪波动图）

## 深度反思

### 本月的重大成长
- 

### 突破性认知
- 

### 需要改进的方面
- 

## 原则与智慧提炼

### 本月提炼的人生原则
1. 
2. 
3. 

### 对下个月的指导
- 

### 长期人生准则更新
- 

## 感恩与展望

### 本月感恩的事
- 

### 下月期待的事
- 

### 长期目标进展
- 

---
*回顾时间：{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}*
*"真正的智慧来自对日常生活的深度反思"*
"""
        
        # 写入回顾文件
        with open(review_path, 'w', encoding='utf-8') as f:
            f.write(review_content)
        
        return {
            "status": "monthly_review_created",
            "path": review_path,
            "month": month_str,
            "content_preview": review_content[:500] + "..." if len(review_content) > 500 else review_content
        }

def main():
    """主函数，用于测试"""
    skill = DiarySkill()
    
    print("日记Skill测试")
    print("=" * 50)
    
    # 测试写日记
    print("1. 测试写日记...")
    result = skill.write_diary()
    print(f"   状态: {result['status']}")
    print(f"   路径: {result['path']}")
    
    # 测试记录闪念
    print("\n2. 测试记录闪念...")
    flash_result = skill.record_flash_note("测试闪念：今天天气真好")
    print(f"   状态: {flash_result['status']}")
    print(f"   闪念: {flash_result['note']}")
    
    # 测试获取闪念
    print("\n3. 测试获取闪念...")
    flash_notes = skill.get_flash_notes()
    print(f"   今日闪念数: {len(flash_notes)}")
    for note in flash_notes:
        print(f"   - {note}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()