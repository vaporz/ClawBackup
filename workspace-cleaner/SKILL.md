---
name: workspace-cleaner
version: 1.0.0
description: >
  工作区清理与归档管理skill，帮助agent保持工作区整洁，建立"吃完饭擦桌子"的好习惯。
  支持智能清理、归档管理、回收站机制和工作流优化。
metadata:
  openclaw:
    homepage: https://clawhub.com
    category: productivity
    tags: [workspace, cleanup, organization, file-management]
---

# Workspace Cleaner Skill - 工作区清理管家

## 概述

这是一个帮助Agent保持工作区整洁的skill。它不仅仅是清理工具，更是培养良好工作习惯的伙伴。通过定期清理和智能归档，让工作区始终保持"吃完饭擦桌子"的整洁状态。

## 核心哲学

### 为什么需要清理？
- **效率提升**：整洁的工作区减少查找时间
- **专注保持**：减少视觉干扰，提升工作专注度
- **规范建立**：统一的文件管理标准
- **问题预防**：避免文件堆积导致的性能问题
- **习惯培养**：让整洁成为团队文化

### 清理是什么？
- **不是删除**：而是整理和归档
- **不是负担**：而是高效工作的基础
- **不是一次性的**：而是持续的习惯
- **不是随意的**：而是有原则的整理

## 使用场景

### 1. 手动触发清理
- **触发命令**："清理工作区"、"整理文件"、"workspace cleanup"
- **使用场景**：任务完成后、工作区杂乱时、准备新任务前

### 2. 定时自动清理
- **默认设置**：每周日晚上10点自动清理
- **可配置**：支持自定义清理频率和时间
- **使用场景**：定期维护，保持工作区长期整洁

### 3. 智能提醒清理
- **触发条件**：工作区文件超过阈值、临时文件过多、长时间未清理
- **使用场景**：预防性维护，避免问题积累

### 4. 任务后自动清理
- **集成场景**：与其他skill集成，任务完成后自动触发
- **使用场景**：确保每个任务都"有始有终"

## 核心功能

### 1. 智能文件识别与分类

**文件类型识别：**
- **核心文件**：身份文件、团队文件、重要产出（保留在工作区）
- **临时文件**：草稿、测试文件、日志文件（归档或清理）
- **版本文件**：同一文件的多个版本（保留最终版，归档历史版）
- **缓存文件**：临时缓存、下载文件（定期清理）

**识别规则：**
- 文件名模式匹配（*.tmp, *.log, *.bak等）
- 文件内容分析（草稿标识、测试数据）
- 文件时间戳（过期文件识别）
- 文件关联性（同一任务的相关文件）

### 2. 归档管理系统

**归档结构：**
```
归档/
├── YYYY-MM/                    # 按月归档
│   ├── drafts/                # 草稿文件
│   ├── tests/                 # 测试文件
│   ├── versions/              # 版本历史
│   └── temp/                  # 临时文件
├── projects/                  # 按项目归档
│   └── 项目名称-YYYYMMDD/
└── recycle-bin/              # 回收站（安全删除）
```

**归档原则：**
- **按时间组织**：便于时间线追溯
- **按类型分类**：便于内容查找
- **保留元数据**：记录归档原因和时间
- **支持检索**：提供快速查找功能

### 3. 回收站机制

**安全删除流程：**
1. **移动到回收站**：而不是直接删除
2. **保留期限**：默认30天，可配置
3. **定期清理**：过期文件自动永久删除
4. **恢复支持**：支持误删文件恢复

**回收站管理：**
- 查看回收站内容
- 恢复特定文件
- 清空回收站
- 调整保留期限

### 4. 清理策略配置

**可配置选项：**
- **清理频率**：每天/每周/每月
- **文件保留规则**：核心文件、临时文件、版本文件的保留策略
- **归档位置**：本地归档、云存储、其他位置
- **通知设置**：清理完成通知、问题提醒

**预设策略：**
- **严格模式**：只保留核心文件，其他全部归档
- **平衡模式**：保留核心文件和近期工作文件
- **宽松模式**：保留较多文件，只清理明显临时文件

## 使用方法

### 基础使用

**中文命令：**
- "清理工作区" - 执行智能清理
- "整理文件" - 同上
- "查看归档" - 查看归档文件
- "管理回收站" - 管理回收站内容

**English Commands:**
- "cleanup workspace" - Perform smart cleanup
- "organize files" - Same as above
- "view archive" - View archived files
- "manage recycle bin" - Manage recycle bin

### 高级使用

**配置清理策略：**
```
配置清理策略 [模式]
可选模式：strict（严格）, balanced（平衡）, loose（宽松）
```

**设置定时任务：**
```
设置定时清理 [频率] [时间]
示例：设置定时清理 每周 周日22:00
```

**自定义文件规则：**
```
添加文件规则 [类型] [模式] [操作]
示例：添加文件规则 临时文件 *.tmp 归档
```

### 集成使用

**与任务系统集成：**
- 任务完成后自动触发清理
- 保留任务相关文件，清理无关文件
- 生成任务清理报告

**与日记系统集成：**
- 清理记录写入工作日志
- 归档文件与日记时间线关联
- 清理经验提炼为原则

## 文件结构

```
workspace-cleaner/
├── SKILL.md                  # 技能说明文档
├── README.md                 # 快速开始指南
├── cleanup.py                # 核心清理逻辑
├── config.yaml               # 配置文件模板
├── rules/                    # 文件规则定义
│   ├── core_files.yaml      # 核心文件规则
│   ├── temp_files.yaml      # 临时文件规则
│   └── version_files.yaml   # 版本文件规则
├── scripts/                  # 辅助脚本
│   ├── setup.py             # 安装脚本
│   ├── cron_setup.py        # 定时任务设置
│   └── test_cleanup.py      # 测试脚本
└── examples/                # 使用示例
    ├── basic_usage.md       # 基础使用示例
    └── integration.md       # 集成使用示例
```

## 清理流程

### 标准清理流程：
```
1. 扫描工作区
   ↓
2. 识别文件类型
   ↓
3. 应用清理规则
   ↓
4. 执行清理操作
   ↓
5. 生成清理报告
   ↓
6. 更新工作日志
```

### 详细步骤：

**步骤1：扫描工作区**
- 遍历工作区所有文件和目录
- 收集文件元数据（名称、大小、时间、类型）
- 识别文件关联性

**步骤2：识别文件类型**
- 应用文件规则匹配
- 识别核心文件、临时文件、版本文件等
- 标记需要处理的文件

**步骤3：应用清理规则**
- 根据配置的策略应用规则
- 决定每个文件的处理方式（保留、归档、删除）
- 处理文件冲突和依赖关系

**步骤4：执行清理操作**
- 移动文件到归档目录
- 删除临时文件到回收站
- 重命名和整理保留文件

**步骤5：生成清理报告**
- 统计清理结果（处理文件数、节省空间等）
- 识别潜在问题（大文件、重复文件等）
- 提供优化建议

**步骤6：更新工作日志**
- 记录清理操作和结果
- 更新文件索引
- 保存清理配置

## 配置说明

### 配置文件 (config.yaml)

```yaml
# 清理策略
strategy: "balanced"  # strict, balanced, loose

# 文件保留规则
retention:
  core_files: "keep"           # 保留核心文件
  temp_files: "archive_30d"    # 临时文件归档保留30天
  version_files: "keep_latest" # 版本文件保留最新版
  cache_files: "delete_7d"     # 缓存文件7天后删除

# 归档设置
archive:
  location: "./归档"           # 归档目录
  organization: "monthly"      # 按月组织
  keep_metadata: true          # 保留文件元数据

# 回收站设置
recycle_bin:
  enabled: true                # 启用回收站
  retention_days: 30           # 保留30天
  auto_cleanup: true           # 自动清理过期文件

# 定时任务
scheduled:
  enabled: true                # 启用定时清理
  frequency: "weekly"          # 每周一次
  day_of_week: "sunday"        # 周日
  time: "22:00"               # 晚上10点

# 通知设置
notifications:
  on_complete: true           # 清理完成通知
  on_problem: true            # 问题提醒
  on_threshold: true          # 阈值提醒
```

### 文件规则配置

**核心文件规则 (core_files.yaml):**
```yaml
rules:
  - name: "身份文件"
    patterns: ["IDENTITY.md", "SOUL.md", "USER.md"]
    action: "keep"
    priority: 100
    
  - name: "团队文件"
    patterns: ["AGENTS.md", "MEMORY.md"]
    action: "keep"
    priority: 90
    
  - name: "工具文件"
    patterns: ["TOOLS.md", "HEARTBEAT.md"]
    action: "keep"
    priority: 80
```

**临时文件规则 (temp_files.yaml):**
```yaml
rules:
  - name: "临时文件"
    patterns: ["*.tmp", "*.temp", "*.bak", "*.backup"]
    action: "archive"
    retention_days: 30
    
  - name: "日志文件"
    patterns: ["*.log", "*.debug", "*.error"]
    action: "archive"
    retention_days: 7
    
  - name: "测试文件"
    patterns: ["test_*", "*_test.*", "debug_*"]
    action: "archive"
    retention_days: 14
```

## 集成指南

### 与Agent Diary集成

**清理记录到工作日志：**
```python
# 清理完成后自动记录
log_entry = {
    "timestamp": datetime.now(),
    "action": "workspace_cleanup",
    "files_processed": processed_count,
    "space_saved": space_saved,
    "problems_found": problems
}
write_to_work_log(log_entry)
```

**归档文件与日记关联：**
- 归档文件添加日记时间戳
- 支持从日记跳转到归档文件
- 清理历史与日记时间线同步

### 与Self-Improving Agent集成

**经验积累：**
```python
# 记录清理经验和优化建议
learning = {
    "pattern": "workspace_clutter",
    "solution": "regular_cleanup",
    "effectiveness": 0.85,
    "recommendation": "建议每周日晚上自动清理"
}
add_to_learnings(learning)
```

### 与其他Skill集成

**通用集成接口：**
```python
# 任务完成后触发清理
def on_task_complete(task_id, result):
    if result.success:
        trigger_cleanup(
            scope="task_files",
            task_id=task_id,
            keep_related=True
        )
```

## 安装与设置

### 🚀 首次安装

1. **下载skill：**
   ```bash
   clawhub install workspace-cleaner
   ```

2. **运行设置脚本：**
   ```bash
   cd ~/.openclaw/skills/workspace-cleaner
   python setup.py
   ```

3. **配置清理策略：**
   ```bash
   # 交互式配置
   python setup.py --configure
   ```

4. **设置定时任务：**
   ```bash
   # 创建每周清理任务
   python scripts/cron_setup.py
   ```

### 📊 验证安装

1. **测试清理功能：**
   ```bash
   python scripts/test_cleanup.py --dry-run
   ```

2. **检查配置：**
   ```bash
   cat ~/.openclaw/workspace/.cleanup_config.yaml
   ```

3. **验证定时任务：**
   ```bash
   openclaw cron list | grep cleanup
   ```

## 常见问题

### Q: 清理会误删重要文件吗？
A: **不会**。skill采用安全删除机制：
1. 核心文件永远保留
2. 临时文件先到回收站
3. 回收站保留30天可恢复
4. 支持自定义文件保护规则

### Q: 如何恢复误删的文件？
A: 使用"管理回收站"命令，查看和恢复回收站中的文件。

### Q: 清理频率应该如何设置？
A: 建议：
- **个人工作区**：每周一次
- **团队共享工作区**：每天一次
- **项目工作区**：项目结束后清理

### Q: 可以清理其他agent的工作区吗？
A: **可以**，但需要相应权限。skill支持：
- 清理当前agent工作区
- 清理指定agent工作区（需授权）
- 清理共享工作区

### Q: 清理会影响性能吗？
A: **影响很小**。skill优化了：
- 增量扫描：只扫描变化文件
- 后台执行：不影响前台工作
- 智能缓存：减少重复扫描

## 最佳实践

### 1. 建立清理习惯
- **每日小清理**：任务完成后简单整理
- **每周大清理**：周日晚上系统清理
- **每月深度清理**：归档过期文件

### 2. 文件命名规范
- 使用有意义的文件名
- 添加日期或版本号
- 避免特殊字符和空格

### 3. 目录结构优化
- 按项目组织文件
- 统一归档目录结构
- 保持目录层级合理

### 4. 定期审查规则
- 每月审查清理规则
- 根据使用情况调整策略
- 优化文件识别准确性

## 开发计划

### 版本1.0 (当前)
- 基础清理功能
- 归档管理系统
- 回收站机制
- 定时任务支持

### 版本1.1 (计划中)
- 云存储集成
- 团队协作清理
- 高级分析报告
- 机器学习优化

### 版本1.2 (规划中)
- 跨平台支持
- 插件系统
- 自动化工作流
- 智能推荐

## 贡献指南

欢迎贡献代码、规则、文档或建议：

1. **报告问题**：GitHub Issues
2. **提交PR**：遵循代码规范
3. **分享规则**：提交文件识别规则
4. **提供反馈**：使用体验和建议

## 许可证

MIT License

---

**最后的话**：整洁的工作区是高效工作的基础。这个skill不仅帮你清理文件，更帮你培养"吃完饭擦桌子"的好习惯。开始使用吧，从今天开始保持工作区整洁。🧹✨

---
*Skill版本：1.0*
*创建时间：2026年3月29日*
*创建者：Jarvis*
*灵感来源：啸的"吃完饭擦桌子"哲学*