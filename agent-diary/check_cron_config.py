#!/usr/bin/env python3
"""
检查日记定时任务配置
"""

import json
import subprocess
import sys

def check_cron_tasks():
    """检查当前的日记定时任务配置"""
    
    print("📋 检查日记定时任务配置")
    print("=" * 60)
    
    # 运行 openclaw cron list 获取任务列表
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print("❌ 无法获取cron任务列表")
            print(f"错误: {result.stderr}")
            return
        
        lines = result.stdout.strip().split('\n')
        
        # 查找与日记相关的任务
        diary_tasks = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ["日记", "回顾", "diary", "review"]):
                diary_tasks.append(line)
        
        if not diary_tasks:
            print("ℹ️  没有找到日记相关的定时任务")
            return
        
        print(f"✅ 找到 {len(diary_tasks)} 个日记相关任务")
        print()
        
        # 分析每个任务
        for task_line in diary_tasks:
            print(f"🔍 分析任务: {task_line[:80]}...")
            
            # 尝试提取任务ID（假设ID是第一个字段）
            parts = task_line.split()
            if parts:
                task_id = parts[0]
                
                # 获取任务详情
                try:
                    detail_result = subprocess.run(
                        ["openclaw", "cron", "get", task_id],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if detail_result.returncode == 0:
                        try:
                            task_info = json.loads(detail_result.stdout)
                            
                            # 检查关键配置
                            issues = []
                            
                            # 检查消息内容
                            payload = task_info.get("payload", {})
                            message = payload.get("message", "")
                            
                            # 检查是否是技能触发词
                            trigger_words = ["写日记", "周回顾", "月回顾", "write diary", "weekly review", "monthly review"]
                            is_trigger_word = any(word in message for word in trigger_words)
                            
                            if not is_trigger_word:
                                issues.append(f"❌ 消息不是技能触发词: '{message}'")
                            else:
                                issues.append(f"✅ 消息是技能触发词: '{message}'")
                            
                            # 检查agentId
                            agent_id = task_info.get("agentId")
                            if not agent_id:
                                issues.append("❌ 没有指定agentId")
                            else:
                                issues.append(f"✅ 指定了agentId: {agent_id}")
                            
                            # 输出检查结果
                            print("  配置检查:")
                            for issue in issues:
                                print(f"    {issue}")
                            
                        except json.JSONDecodeError:
                            print("   ❌ 无法解析任务详情")
                    
                except subprocess.TimeoutExpired:
                    print("   ⏱️  获取任务详情超时")
            
            print()
    
    except FileNotFoundError:
        print("❌ openclaw命令未找到")
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")

def main():
    """主函数"""
    
    print("日记定时任务配置检查工具")
    print("=" * 60)
    print()
    print("这个工具会检查当前的日记定时任务配置，确保：")
    print("1. ✅ 定时任务指定了正确的agentId")
    print("2. ✅ 定时任务消息是技能触发词（'写日记'、'周回顾'、'月回顾'）")
    print("3. ✅ 避免日记保存到错误的文件夹")
    print()
    
    check_cron_tasks()
    
    print("=" * 60)
    print("📝 建议操作：")
    print("1. 如果发现配置问题，请重新创建定时任务")
    print("2. 使用正确的命令格式：")
    print("   openclaw cron add --name \"任务名\" \\")
    print("     --schedule \"0 2 * * *\" \\")
    print("     --payload '{\"kind\":\"agentTurn\",\"message\":\"写日记\"}' \\")
    print("     --agentId [你的agentId]")
    print("3. 验证任务：openclaw cron list")

if __name__ == "__main__":
    main()