# Cron任务管理规范

> 创建时间：2026-03-29
> 过期时间：2026-09-29（6个月）

## 核心原则

### 1. 统一命名规范
**格式**：`[agent名]-[任务类型]`

**示例**：
- `writer-每日日记`
- `arteditor-每周回顾`
- `infocollecter-每月回顾`
- `chief-editor-每日日记`
- `legal-每日日记`

### 2. 无通知原则
- 日记相关任务：**不发送通知**（`--no-deliver`）
- 状态检查任务：**发送通知**（`--announce`）
- 信息收集任务：按需配置

### 3. 标准配置模板

#### 每日日记任务
```bash
openclaw cron add \
  --name "[agent名]-每日日记" \
  --agent <agentId> \
  --cron "0 2 * * *" \
  --tz "Asia/Shanghai" \
  --message "现在是凌晨2点，开始写今天的日记吧。请回顾今天的工作和经历，放松自然地写下你的思考和感受。" \
  --session isolated \
  --no-deliver
```

#### 每周回顾任务
```bash
openclaw cron add \
  --name "[agent名]-每周回顾" \
  --agent <agentId> \
  --cron "0 1 * * 0" \
  --tz "Asia/Shanghai" \
  --message "现在是周回顾时间。请回顾过去一周的日记，提炼主题、分析情绪趋势、总结学习收获，并思考可以提炼出什么人生原则。" \
  --session isolated \
  --no-deliver
```

#### 每月回顾任务
```bash
openclaw cron add \
  --name "[agent名]-每月回顾" \
  --agent <agentId> \
  --cron "0 23 28-31 * *" \
  --tz "Asia/Shanghai" \
  --message "现在是月回顾时间。请回顾过去一个月的日记和每周回顾，进行深度反思，提炼人生原则，更新个人哲学体系。" \
  --session isolated \
  --no-deliver
```

## 任务分类

### A类：日记相关任务（无通知）
| 任务类型 | 执行时间 | 目的 |
|----------|----------|------|
| 每日日记 | 02:00 | 记录每日工作和思考 |
| 每周回顾 | 周日 01:00 | 提炼周度主题和模式 |
| 每月回顾 | 每月28-31日 23:00 | 抽象原则性感悟 |

### B类：状态检查任务（有通知）
| 任务名称 | 执行时间 | 目的 |
|----------|----------|------|
| cron状态检查 | 09:00 | 检查所有cron任务状态 |
| 系统健康检查 | 10:00 | 检查系统运行状态 |

### C类：业务任务（按需配置）
| 任务名称 | 执行时间 | 目的 |
|----------|----------|------|
| 每日信息收集 | 06:00 | 收集新闻和信息 |
| daily-backup | 08:00 | 系统备份 |

## 错误处理流程

### 1. 自动检查
- **时间**：每天上午9点
- **脚本**：`~/.openclaw/workspace/scripts/check-cron-status.sh`
- **通知**：发现错误时通知啸

### 2. 常见错误及修复

#### 错误1：缺少chatId
```
错误信息：Delivering to Telegram requires target <chatId>
修复命令：openclaw cron edit <ID> --announce --to 8726379476 --channel telegram
```

#### 错误2：多channel冲突
```
错误信息：Channel is required when multiple channels are configured
修复命令：openclaw cron edit <ID> --announce --to 8726379476 --channel telegram
```

#### 错误3：文件写入失败
```
错误信息：Edit: `in ~/.openclaw/workspace-xxx/.diary/...` failed
可能原因：目录不存在或权限问题
修复：检查目录结构，确保agent有对应的工作区
```

### 3. 手动修复步骤
1. 查看错误详情：`openclaw cron list | grep error`
2. 获取任务ID
3. 查看任务配置：`openclaw cron edit <ID>`
4. 修复配置
5. 测试运行：`openclaw cron run <ID>`

## 维护脚本

### 1. 状态检查脚本
位置：`~/.openclaw/workspace/scripts/check-cron-status.sh`
功能：检查所有cron任务状态，发现错误时输出详细信息

### 2. 批量修复脚本
位置：`~/.openclaw/workspace/scripts/fix-cron-tasks.sh`
功能：批量修复常见配置问题

### 3. 使用示例
```bash
# 检查cron状态
~/.openclaw/workspace/scripts/check-cron-status.sh

# 查看所有任务
openclaw cron list

# 修复单个任务
openclaw cron edit <任务ID> --no-deliver --name "新任务名"
```

## 监控与告警

### 1. 自动监控
- **cron状态检查**：每天09:00执行
- **错误通知**：发现错误时通过Telegram通知
- **连续错误**：记录连续错误次数，超过阈值重点处理

### 2. 人工检查
- **每周一次**：全面检查cron任务状态
- **每月一次**：清理无效任务，优化配置
- **新agent加入时**：确保正确配置日记任务

## 最佳实践

### 1. 创建新agent时的标准流程
1. 创建agent工作区
2. 配置agent-diary skill
3. 创建3个标准日记任务（每日/每周/每月）
4. 测试任务运行
5. 添加到监控列表

### 2. 任务命名规范
- 使用统一前缀：`[agent名]-`
- 明确任务类型：`每日日记`、`每周回顾`、`每月回顾`
- 避免歧义：不要使用模糊的名称

### 3. 配置一致性
- 所有日记任务：`--no-deliver`
- 所有检查任务：`--announce --to 8726379476 --channel telegram`
- 统一时区：`--tz "Asia/Shanghai"`

## 相关文件
- `~/.openclaw/cron/jobs.json` - cron任务配置文件
- `~/.openclaw/workspace/scripts/check-cron-status.sh` - 状态检查脚本
- `~/.openclaw/workspace/scripts/fix-cron-tasks.sh` - 批量修复脚本
- `.diary/logs/2026-03/2026-03-28-agent-communication-fix.md` - 问题解决记录