# MEMORY.md - Your Long-Term Memory

This file stores curated memories, significant decisions, and lessons learned to help me provide better assistance.

## Key Learnings & Decisions

- **本地Agent沟通：** 不再通过Telegram群与Jarvis沟通，直接在本地agent之间传递信息

- **Verification of System Operations:** For any system configuration or task creation (e.g., setting up cron jobs, modifying configurations), I must verify that the operation was successful after it's performed. If the operation fails, I should attempt to retry it immediately or report the failure to you.

- **每日写日记cron任务：** 多个agent（writer、arteditor）都设置了凌晨1点写日记的cron任务
  - 时间：每天凌晨1点（Asia/Shanghai时区）
  - 内容：回顾工作进展、学习收获、遇到的问题、明天的计划
  
- **日记文件整理规范（啸的建议）：**
  - **memory/** 目录 → 事务性、工作相关记录
  - **diary/** 目录 → 个人小天地，放松写日记，记录心情、感悟和成长
  - 日记文件命名格式：YYYY-MM-DD.md
