#!/usr/bin/env python3
"""
日记Skill设置脚本
设置定时任务和初始化配置
"""

import os
import sys
import json
import datetime
from pathlib import Path

def setup_cron_jobs():
    """设置日记相关的定时任务"""
    
    # 这里应该调用OpenClaw的cron API来设置定时任务
    # 由于我们无法直接调用，这里提供配置说明
    
    cron_config = {
        "daily_diary": {
            "name": "每日日记写作",
            "description": "每天凌晨2点自动写日记",
            "schedule": {
                "kind": "cron",
                "expr": "0 2 * * *",  # 每天凌晨2点
                "tz": "Asia/Shanghai"
            },
            "payload": {
                "kind": "agentTurn",
                "message": "写日记",
                "model": "deepseek/deepseek-chat"
            },
            "sessionTarget": "current",
            "delivery": {
                "mode": "none"  # 不发送通知，直接在当前会话执行
            }
        },
        "weekly_review": {
            "name": "每周回顾",
            "description": "每周日凌晨1点进行周回顾",
            "schedule": {
                "kind": "cron",
                "expr": "0 1 * * 0",  # 每周日凌晨1点
                "tz": "Asia/Shanghai"
            },
            "payload": {
                "kind": "agentTurn",
                "message": "周回顾",
                "model": "deepseek/deepseek-chat"
            },
            "sessionTarget": "current",
            "delivery": {
                "mode": "none"
            }
        },
        "monthly_review": {
            "name": "每月回顾",
            "description": "每月最后一天晚上11点进行月回顾",
            "schedule": {
                "kind": "cron",
                "expr": "0 23 28-31 * *",  # 每月最后一天晚上11点
                "tz": "Asia/Shanghai"
            },
            "payload": {
                "kind": "agentTurn", 
                "message": "月回顾",
                "model": "deepseek/deepseek-chat"
            },
            "sessionTarget": "current",
            "delivery": {
                "mode": "none"
            }
        }
    }
    
    return cron_config

def create_config_file():
    """创建配置文件"""
    
    config = {
        "version": "1.0",
        "created_at": datetime.datetime.now().isoformat(),
        "workspace_path": None,
        "settings": {
            "daily_time": "02:00",
            "weekly_review_day": "sunday",
            "weekly_review_time": "01:00",
            "monthly_review_time": "23:00",
            "encryption_enabled": False,
            "encryption_password": None
        },
        "directories": {
            "diary": ".diary",
            "flash_notes": ".diary/flash-notes",
            "reviews": ".diary/reviews",
            "principles": ".diary/principles"
        }
    }
    
    config_path = os.path.join(os.path.dirname(__file__), "diary_config.json")
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    return config_path

def create_usage_guide():
    """创建使用指南"""
    
    guide = """# 日记Skill使用指南

## 快速开始

### 1. 手动写日记
```
/日记
```
或直接说"写日记"

### 2. 记录闪念
```
记录闪念：[你的想法]
```
例如："记录闪念：今天想到一个有趣的科普点子"

### 3. 进行回顾
```
/周回顾
/月回顾
```

## 定时任务设置

日记Skill会自动设置以下定时任务：

1. **每日日记**：凌晨2点自动触发
2. **周回顾**：每周日凌晨1点自动触发  
3. **月回顾**：每月最后一天晚上11点自动触发

## 文件结构

日记Skill会在你的工作空间创建以下结构：

```
diary/
├── YYYY-MM-DD.md              # 每日日记
├── flash-notes/               # 闪念记录
│   └── YYYY-MM-DD-flash.md    # 当天的闪念
├── reviews/                   # 定期回顾
│   ├── YYYY-MM-周回顾.md      # 每周回顾
│   └── YYYY-MM-月回顾.md      # 每月回顾
└── principles/                # 原则提炼
    └── 个人原则.md            # 积累的人生原则
```

## 写作建议

### 开始写日记时，可以思考：
- 今天发生了什么值得记录的事？
- 有什么想吐槽或想夸的？
- 有什么新的感悟或思考？
- 此刻的感受是什么？
- 这件事让我想起了什么？

### 写作原则：
- 放松自然，像和朋友聊天
- 真实第一，想什么就写什么
- 允许思维跳跃
- 长短随意
- 为自己而写

## 回顾与提炼

### 周回顾：
- 识别重复出现的主题
- 分析情绪变化趋势
- 总结重要的学习收获
- 提炼初步的人生原则

### 月回顾：
- 进行深度反思
- 抽象更高层次的原则
- 更新个人哲学体系
- 规划下个月的成长方向

## 隐私设置

默认情况下，日记是普通文本文件。如果你需要加密：

1. 在配置中启用加密
2. 设置加密密码
3. 只有持有密码的人可以查看加密内容

## 故障排除

### Q: 定时任务没有触发？
A: 检查OpenClaw的cron服务是否正常运行：`openclaw cron status`

### Q: 闪念记录不见了？
A: 闪念会保存在当天的闪念文件中，写日记时会自动整合

### Q: 想调整定时时间？
A: 可以修改diary_config.json中的时间设置

## 支持与反馈

如果在使用中遇到问题或有改进建议，请告诉我们。

---

**记住**：日记是你送给未来自己的礼物。坚持写下去，你会看到自己的成长。📝✨
"""
    
    guide_path = os.path.join(os.path.dirname(__file__), "USAGE_GUIDE.md")
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    return guide_path

def main():
    """主设置函数"""
    
    print("日记Skill设置程序")
    print("=" * 50)
    
    # 创建配置文件
    config_path = create_config_file()
    print(f"✓ 配置文件已创建: {config_path}")
    
    # 创建使用指南
    guide_path = create_usage_guide()
    print(f"✓ 使用指南已创建: {guide_path}")
    
    # 显示cron配置
    cron_config = setup_cron_jobs()
    print("\n✓ 定时任务配置已生成")
    
    print("\n⚠️  ⚠️  ⚠️  重要提醒 ⚠️  ⚠️  ⚠️")
    print("=" * 60)
    print("这个脚本只生成配置，不会自动创建定时任务！")
    print("你需要手动运行以下OpenClaw命令来创建cron任务：")
    print("=" * 60)
    
    print("\n需要手动设置的定时任务：")
    print("=" * 50)
    
    for job_id, job_config in cron_config.items():
        print(f"\n{job_config['name']}:")
        print(f"  描述: {job_config['description']}")
        print(f"  时间: {job_config['schedule']['expr']} ({job_config['schedule']['tz']})")
        print(f"  消息: {job_config['payload']['message'][:50]}...")
        
        # 提供具体的OpenClaw命令示例
        print(f"\n  创建命令示例：")
        print(f"  openclaw cron add --name \"{job_config['name']}\" \\")
        print(f"    --schedule \"{job_config['schedule']['expr']}\" \\")
        print(f"    --payload '{json.dumps(job_config['payload'], ensure_ascii=False)}' \\")
        print(f"    --agentId [你的agentId]")
    
    print("\n" + "=" * 50)
    print("\n设置完成！")
    print("\n📋 下一步操作：")
    print("1. ⚠️  重要：手动运行上面的OpenClaw命令创建cron任务")
    print("2. 验证任务：运行 'openclaw cron list' 查看已创建的任务")
    print("3. 开始使用：说'写日记'或'记录闪念：[内容]'")
    print("4. 查看USAGE_GUIDE.md获取详细说明")
    print("\n💡 提示：如果你不确定如何运行这些命令，可以请求管理员帮助。")

if __name__ == "__main__":
    main()