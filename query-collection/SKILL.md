# Query Collection Skill

信息收集结果查询skill，为其他agent提供快速查询抓取结果的能力。

## 功能描述

这个skill包装了信息收集系统的查询功能，让其他agent可以：
1. 查询指定日期的收集结果
2. 按条件筛选内容（来源、分类、关键词等）
3. 获取JSON格式数据用于进一步处理
4. 获取可读格式用于人类查看

## 适用场景

- **主编agent**：查询今日收集的科技新闻，用于选题
- **写作agent**：查询特定主题的内容，获取写作素材
- **美编agent**：查询有趣故事，寻找配图灵感
- **其他agent**：需要了解信息收集结果的任何场景

## 使用方法

### 1. 基础查询
```bash
# 查询指定日期的收集结果（默认返回JSON）
query-collection 20260330

# 查询指定日期和条数
query-collection 20260330 10

# 查询并排序
query-collection 20260330 10 desc
```

### 2. 高级查询
```bash
# 使用高级查询工具
query-collection-advanced --date 20260330 --source "36氪" --limit 5

# 查询有摘要的内容
query-collection-advanced --date 20260330 --has-summary

# 按关键词搜索
query-collection-advanced --keyword "人工智能" --limit 10
```

### 3. 输出控制
```bash
# 返回可读格式（人类查看）
query-collection 20260330 --human

# 安静模式（只输出数据）
query-collection-advanced --date 20260330 --quiet

# 输出到文件
query-collection-advanced --date 20260330 --output results.json
```

### 4. 统计信息
```bash
# 显示统计信息
query-collection-advanced --date 20260330 --stats
```

## 参数说明

### 基础查询参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `date` | 查询日期 (YYYYMMDD或YYYY-MM-DD) | `20260330` |
| `limit` | 返回条数 (0=所有) | `10` |
| `order` | 排序方式 (desc/asc) | `desc` |
| `--human` | 返回可读格式 | `--human` |

### 高级查询参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--date` | 日期或日期范围 | `20260325-20260330` |
| `--source` | 按来源筛选 | `--source "36氪"` |
| `--category` | 按分类筛选 | `--category tech` |
| `--keyword` | 按关键词搜索 | `--keyword "人工智能"` |
| `--has-summary` | 只查询有摘要的 | `--has-summary` |
| `--limit` | 返回条数 | `--limit 5` |
| `--order` | 排序方式 | `--order asc` |
| `--order-by` | 排序字段 | `--order-by title` |
| `--format` | 输出格式 | `--format json` |
| `--human` | 可读格式 | `--human` |
| `--quiet` | 安静模式 | `--quiet` |
| `--output` | 输出到文件 | `--output data.json` |
| `--stats` | 显示统计 | `--stats` |

## 输出格式

### JSON格式（默认，适合agent处理）
```json
[
  {
    "id": 118,
    "hash": "ccdf17b7ce84a9e58b0ee78baf75aac0",
    "title": "测试标题",
    "link": "http://example.com/article",
    "source": "测试来源",
    "category": "tech",
    "summary": "内容摘要...",
    "added_at": "2026-03-30 17:26:13",
    "content_date": "2026-03-30T17:26:13.039832",
    "extraction_method": "jina"
  }
]
```

### 可读格式（--human，适合人类查看）
```
📄 测试标题
   🔗 链接: http://example.com/article
   📍 来源: 测试来源
   📂 分类: tech
   📝 摘要: 内容摘要...
   ⏰ 添加时间: 2026-03-30 17:26:13
   📅 内容时间: 2026-03-30T17:26:13.039832
   🔧 提取方法: jina
   🔑 哈希: ccdf17b7ce84a9e5...
```

## 与其他agent的集成示例

### 1. 主编agent查询今日科技新闻
```bash
# 查询今日科技新闻，获取选题素材
query-collection-advanced --date $(date +%Y%m%d) --category tech --limit 10 --stats
```

### 2. 写作agent查询特定主题
```bash
# 查询人工智能相关内容，获取写作素材
query-collection-advanced --keyword "人工智能" --has-summary --limit 20
```

### 3. 美编agent查询有趣故事
```bash
# 查询有趣故事，寻找配图灵感
query-collection-advanced --category "fun-stories" --has-summary --limit 5 --human
```

### 4. 在Python脚本中使用
```python
import subprocess
import json

# 执行查询
result = subprocess.run(
    ["query-collection-advanced", "--date", "20260330", "--quiet"],
    capture_output=True,
    text=True
)

# 解析JSON结果
data = json.loads(result.stdout)
for item in data:
    print(f"标题: {item['title']}")
    print(f"链接: {item['link']}")
    print(f"摘要: {item.get('summary', '无摘要')}")
```

## 数据源说明

### 数据库位置
- SQLite数据库: `data/history/history.db`
- 包含所有历史收集记录
- 支持快速查询和统计分析

### 数据字段
- `title`: 内容标题
- `link`: 内容链接
- `source`: 内容来源
- `category`: 内容分类 (tech/science/education/fun-stories)
- `summary`: 内容摘要
- `added_at`: 添加时间
- `content_date`: 内容发布时间
- `extraction_method`: 提取方法 (jina/standard)

## 性能考虑

### 查询性能
- 数据库已建立索引，查询速度快
- 支持复杂条件组合查询
- 支持大数据量分页查询

### 内存使用
- 按需加载数据，内存占用小
- 支持流式处理大数据集

### 并发访问
- SQLite支持多进程只读访问
- 适合多个agent同时查询

## 错误处理

### 常见错误
1. **数据库不存在**: 检查数据库文件路径
2. **日期格式错误**: 使用正确的日期格式
3. **无查询结果**: 调整查询条件

### 错误信息
- 友好的错误提示
- 详细的帮助信息
- 示例用法展示

## 更新日志

### v1.0 (2026-03-30)
- 初始版本发布
- 基础查询功能
- 高级查询功能
- 多种输出格式
- 统计功能

## 联系信息

- **Skill作者**: 小信（信息收集官）
- **所属项目**: 信息收集系统
- **创建时间**: 2026-03-30
- **最后更新**: 2026-03-30

## 许可证

本skill遵循OpenClaw Skill标准协议。