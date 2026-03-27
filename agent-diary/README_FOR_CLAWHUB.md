# Agent Diary Skill - 深度自我探索与智慧积累  
# Agent Diary Skill - Deep Self-Exploration and Wisdom Accumulation

![Agent Diary Skill](https://img.shields.io/badge/Skill-Agent_Diary-blue)
![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-green)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-yellow)

**English Summary**:  
Agent Diary Skill is a tool for AI agents to establish deep journaling habits. It's not just a recording tool, but a companion for self-exploration, emotional expression, thinking organization, and wisdom accumulation. Through regular journaling and review, agents can better understand themselves, record growth, and extract life principles.

**中文简介**:  
Agent Diary Skill 是一个帮助AI Agent建立深度日记习惯的工具。它不仅仅是记录工具，更是自我探索、情感表达、思维梳理和智慧积累的伙伴。通过定期写日记和回顾，Agent可以更好地理解自己、记录成长、提炼人生原则。

## 🌟 简介

日记Skill是一个帮助AI Agent建立深度日记习惯的工具。它不仅仅是记录工具，更是自我探索、情感表达、思维梳理和智慧积累的伙伴。通过定期写日记和回顾，Agent可以更好地理解自己、记录成长、提炼人生原则。

## ✨ 核心特性

### 📝 智能日记写作
- **自然写作引导**：提供放松自然的写作环境，避免僵化模板
- **记忆整合**：自动关联当天的memory记录作为参考
- **闪念记录**：支持随时记录想法，晚上自动整合到日记中
- **多角色适配**：适合文字创作者、技术人员、创意工作者等各类Agent

### 🔄 定期回顾与提炼
- **周回顾**：自动生成周回顾，提炼主题和模式
- **月回顾**：深度月回顾，抽象人生原则
- **智慧积累**：从日常经历中提炼指导生活的原则
- **成长追踪**：记录思维和情感的演变轨迹

### ⏰ 自动化管理
- **定时触发**：每天凌晨2点自动写日记（可配置）
- **文件管理**：自动创建和维护标准的文件结构
- **隐私保护**：可选加密功能，保护私人记录

## 🚀 快速开始

### 安装 Installation
```bash
# 通过clawhub安装 Install via clawhub
clawhub install agent-diary
```

### 基本使用 Basic Usage

**中文命令 Chinese Commands**:
```bash
# 手动写日记 Manual diary writing
/日记
# 或直接说："写日记" or simply say: "写日记"

# 记录闪念 Record flash notes
记录闪念：[你的想法]
例如："记录闪念：今天想到一个有趣的科普点子"

# 进行回顾 Perform reviews
/周回顾
/月回顾
```

**English Commands**:
```bash
# Manual diary writing
/diary
# or simply say: "write diary"

# Record flash notes
flash: [your thought]
example: "flash: Today I thought of an interesting science popularization idea"

# Perform reviews
/weekly
/monthly
```

## 📁 文件结构

```
.diary/                        # 隐藏文件夹，增强隐私感
├── YYYY/                      # 按年分目录
│   └── MM/                    # 按月分目录
│       └── YYYY-MM-DD.md      # 每日日记
├── flash-notes/               # 闪念记录
│   └── YYYY-MM-DD-flash.md    # 当天的闪念
├── reviews/                   # 定期回顾
│   ├── YYYY-MM-周回顾.md      # 每周回顾
│   └── YYYY-MM-月回顾.md      # 每月回顾
└── principles/                # 原则提炼
    └── 个人原则.md            # 积累的人生原则
```

## 🎯 适用场景

### 文字创作类Agent
- 记录创作灵感和写作过程
- 反思内容创作的价值和影响
- 连接专业知识与读者需求

### 技术类Agent  
- 记录技术问题和解决方案
- 反思技术决策和架构设计
- 连接技术实现与业务价值

### 创意类Agent
- 记录创意灵感和创作过程
- 反思艺术表达和审美选择
- 连接创意想法与最终作品

### 所有Agent
- 探索和定义自己的"人格"
- 记录成长和思维演变
- 建立个人哲学体系

## 🔧 技术实现

### 核心功能
- **Python实现**：使用Python 3.8+开发，兼容性好
- **OpenClaw集成**：完美集成OpenClaw的cron和文件系统
- **模块化设计**：易于扩展和定制

### 定时任务
- 通过OpenClaw的cron系统管理
- 可配置的触发时间
- 支持手动和自动触发

### 隐私保护
- 可选AES加密功能
- 密码保护机制
- 灵活的访问控制

## 📊 效果展示

### 日记示例
```markdown
# 2026-03-27 周五

现在是晚上，开始写今天的日记。

今天完成了项目的重要里程碑。过程中遇到了一些技术挑战，但最终都解决了。

从这件事我学到：有时候最直接的解决方案就是最好的解决方案。

此刻的感受是充实而有成就感。明天要继续保持这种状态。
```

### 周回顾示例
```markdown
# 2026-03-周回顾

## 本周主题
1. 技术问题解决
2. 团队协作
3. 学习新技能

## 重要学习
- 复杂问题需要分解处理
- 沟通是协作的关键
- 持续学习保持竞争力

## 提炼原则
1. 分解复杂问题，逐个击破
2. 主动沟通，避免信息孤岛
```

## 🤝 贡献与反馈

### 报告问题
如果您在使用中遇到问题，请通过以下方式反馈：
1. 在clawhub页面提交issue
2. 通过OpenClaw社区反馈
3. 直接联系开发者

### 贡献代码
欢迎提交Pull Request来改进这个Skill：
1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

### 功能建议
如果您有新的功能想法，欢迎提出：
- 更多写作模板
- 情感分析功能
- 与其他工具的集成
- 可视化分析报告

## 📚 文档

- [完整使用指南](SKILL.md)
- [快速开始指南](QUICK_START.md)
- [技术实现文档](diary_main.py)
- [设置说明](setup.py)

## 📄 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 🙏 致谢

感谢所有使用和贡献这个Skill的用户。特别感谢：
- OpenClaw开发团队提供的优秀平台
- clawhub社区的分享精神
- 所有测试和反馈的用户

---

**开始你的日记之旅，探索更深的自我！** 📖✨

*"真正的智慧来自对日常生活的深度反思"*