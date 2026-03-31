# Query Collection Skill 使用示例

## 快速开始

### 1. 检查skill是否可用
```bash
# 查看帮助
./query-collection.sh --help

# 测试连接
./query-collection.sh 20260330 1
```

### 2. 基础查询
```bash
# 查询今日收集结果（JSON格式）
./query-collection.sh $(date +%Y%m%d)

# 查询今日10条结果（可读格式）
./query-collection.sh $(date +%Y%m%d) 10 desc --human

# 查询昨日所有结果
./query-collection.sh $(date -d "yesterday" +%Y%m%d) 0
```

### 3. 高级查询
```bash
# 查询科技新闻
./query-collection-advanced.sh --date $(date +%Y%m%d) --category tech --limit 10

# 查询有摘要的内容
./query-collection-advanced.sh --date $(date +%Y%m%d) --has-summary --human

# 搜索特定关键词
./query-collection-advanced.sh --keyword "人工智能" --limit 20
```

## 与其他agent的集成示例

### 1. 主编agent使用示例
```bash
#!/bin/bash
# 主编的每日选题脚本

echo "📰 今日选题分析..."
echo "=" * 60

# 查询今日科技新闻
echo "1. 科技新闻:"
./query-collection-advanced.sh --date $(date +%Y%m%d) --category tech --limit 5 --human

echo
echo "2. 科学发现:"
./query-collection-advanced.sh --date $(date +%Y%m%d) --category science --limit 3 --human

echo
echo "3. 热门话题:"
./query-collection-advanced.sh --date $(date +%Y%m%d) --category "fun-stories" --limit 2 --human
```

### 2. 写作agent使用示例
```python
#!/usr/bin/env python3
# 写作agent的素材收集脚本

import subprocess
import json
import sys

def get_writing_materials(topic, limit=10):
    """获取写作素材"""
    cmd = [
        "./query-collection-advanced.sh",
        "--keyword", topic,
        "--has-summary",
        "--limit", str(limit),
        "--quiet"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 查询失败: {result.stderr}")
        return []
    
    try:
        data = json.loads(result.stdout)
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        return []

# 示例：获取人工智能相关素材
materials = get_writing_materials("人工智能", 5)
for i, item in enumerate(materials, 1):
    print(f"\n素材 {i}:")
    print(f"标题: {item['title']}")
    print(f"摘要: {item.get('summary', '无摘要')[:100]}...")
    print(f"链接: {item['link']}")
```

### 3. 美编agent使用示例
```bash
#!/bin/bash
# 美编的配图灵感脚本

echo "🎨 寻找配图灵感..."
echo "=" * 60

# 查询有趣故事
echo "有趣故事（配图灵感）:"
./query-collection-advanced.sh \
    --category "fun-stories" \
    --has-summary \
    --limit 3 \
    --human \
    --order-by title

# 查询科学图片相关
echo
echo "科学发现（可能需要图表）:"
./query-collection-advanced.sh \
    --category "science" \
    --keyword "发现|研究|实验" \
    --limit 2 \
    --human
```

## 实际工作流示例

### 1. 每日晨会数据准备
```bash
#!/bin/bash
# 晨会数据报告

DATE=$(date +%Y%m%d)
REPORT_FILE="morning_report_${DATE}.md"

echo "# ${DATE} 晨会数据报告" > $REPORT_FILE
echo "" >> $REPORT_FILE

# 收集统计数据
echo "## 📊 昨日收集统计" >> $REPORT_FILE
./query-collection-advanced.sh --date $(date -d "yesterday" +%Y%m%d) --stats >> $REPORT_FILE

echo "" >> $REPORT_FILE
echo "## 🔥 今日热门话题" >> $REPORT_FILE
./query-collection-advanced.sh --date $DATE --category "fun-stories" --limit 3 --human >> $REPORT_FILE

echo "" >> $REPORT_FILE
echo "## 🧪 科技前沿" >> $REPORT_FILE
./query-collection-advanced.sh --date $DATE --category "tech" --limit 3 --human >> $REPORT_FILE

echo "✅ 晨会报告已生成: $REPORT_FILE"
```

### 2. 周度内容分析
```bash
#!/bin/bash
# 周度内容分析

START_DATE=$(date -d "last monday" +%Y%m%d)
END_DATE=$(date +%Y%m%d)

echo "📈 周度内容分析 (${START_DATE} - ${END_DATE})"
echo "=" * 60

# 按分类统计
echo "## 分类分布"
./query-collection-advanced.sh \
    --date "${START_DATE}-${END_DATE}" \
    --stats \
    --quiet

# 热门来源
echo
echo "## 热门来源"
./query-collection-advanced.sh \
    --date "${START_DATE}-${END_DATE}" \
    --quiet \
    | python3 -c "
import json, sys, collections
data = json.load(sys.stdin)
sources = collections.Counter(item['source'] for item in data)
for source, count in sources.most_common(5):
    print(f'{source}: {count}条')
"
```

### 3. 主题研究支持
```bash
#!/bin/bash
# 主题研究：人工智能

TOPIC="人工智能"
echo "🔍 主题研究: $TOPIC"
echo "=" * 60

# 查询相关主题
echo "## 相关文章"
./query-collection-advanced.sh \
    --keyword "$TOPIC" \
    --has-summary \
    --limit 10 \
    --human \
    --order-by added_at \
    --order desc

# 统计信息
echo
echo "## 统计信息"
./query-collection-advanced.sh \
    --keyword "$TOPIC" \
    --stats \
    --quiet
```

## 高级用法

### 1. 管道处理
```bash
# 获取JSON数据并用jq处理
./query-collection-advanced.sh --date 20260330 --quiet | jq '.[] | {title, source, category}'

# 获取CSV格式并导入Excel
./query-collection-advanced.sh --date 20260330 --format csv --output data.csv

# 统计每日收集数量
for day in {25..30}; do
    count=$(./query-collection-advanced.sh --date "202603$day" --quiet | jq length)
    echo "2026-03-$day: $count 条"
done
```

### 2. 自动化脚本
```bash
#!/bin/bash
# 自动化内容监控脚本

# 监控新内容
NEW_CONTENT=$(./query-collection-advanced.sh \
    --date $(date +%Y%m%d) \
    --quiet \
    | jq 'length')

if [ "$NEW_CONTENT" -gt 0 ]; then
    echo "🎉 今日已收集 $NEW_CONTENT 条新内容"
    
    # 发送通知
    ./query-collection-advanced.sh \
        --date $(date +%Y%m%d) \
        --limit 3 \
        --human \
        | mail -s "今日内容摘要" editor@example.com
else
    echo "📭 今日暂无新内容"
fi
```

### 3. 数据导出备份
```bash
#!/bin/bash
# 月度数据导出

MONTH="202603"
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

# 导出整月数据
./query-collection-advanced.sh \
    --date "${MONTH}01-${MONTH}31" \
    --format json \
    --output "$BACKUP_DIR/${MONTH}_collection.json"

# 导出CSV格式
./query-collection-advanced.sh \
    --date "${MONTH}01-${MONTH}31" \
    --format csv \
    --output "$BACKUP_DIR/${MONTH}_collection.csv"

echo "✅ ${MONTH}月数据已备份到 $BACKUP_DIR/"
```

## 故障排除

### 1. 常见问题
```bash
# 问题：数据库不存在
# 解决：运行信息收集器
cd /home/zx/.openclaw/workspace-infocollecter
python3 scripts/collector.py

# 问题：日期格式错误
# 解决：使用正确格式
./query-collection.sh 2026-03-30  # 正确
./query-collection.sh 2026/03/30  # 错误

# 问题：无查询结果
# 解决：调整查询条件或日期
./query-collection.sh $(date +%Y%m%d)  # 今日
./query-collection.sh 20260325         # 指定日期
```

### 2. 性能优化
```bash
# 使用安静模式减少输出
./query-collection-advanced.sh --date 20260330 --quiet

# 限制返回条数
./query-collection-advanced.sh --date 20260330 --limit 100

# 使用简单查询条件
./query-collection.sh 20260330  # 比高级查询快
```

## 最佳实践

### 1. 日常使用
- 使用`--quiet`模式进行自动化处理
- 使用`--human`模式进行人工查看
- 定期使用`--stats`查看收集情况

### 2. 数据管理
- 定期备份重要数据
- 使用日期范围查询历史数据
- 利用统计功能分析收集效果

### 3. 团队协作
- 共享查询脚本给团队成员
- 建立标准查询模板
- 记录常用查询命令

## 更新与维护

### 1. 检查更新
```bash
# 查看skill版本
cat SKILL.md | grep -A2 "更新日志"

# 检查数据库状态
ls -la /home/zx/.openclaw/workspace-infocollecter/data/history/
```

### 2. 反馈与改进
- 发现问题请记录在issues中
- 建议新功能请提交feature request
- 使用问题请参考EXAMPLES.md

---

**更多示例请参考SKILL.md文档**