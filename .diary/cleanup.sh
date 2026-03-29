#!/bin/bash
# 日记系统清理脚本
# 每月1日执行，清理过期文件

set -e

echo "=== 日记系统清理开始 ==="
echo "当前时间: $(date)"

# 检查是否是每月1日
if [ "$(date +%d)" != "01" ]; then
    echo "不是每月1日，跳过清理"
    exit 0
fi

WORKSPACE="$HOME/.openclaw/workspace"
DIARY_DIR="$WORKSPACE/.diary"

echo "工作区: $WORKSPACE"
echo "日记目录: $DIARY_DIR"

# 1. 清理超过3个月的工作日志
echo "清理超过3个月的工作日志..."
find "$DIARY_DIR/logs" -maxdepth 1 -type d -name "*-*" -mtime +90 -exec echo "删除: {}" \; -exec rm -rf {} \;

# 2. 清理超过6个月的知识库文件
echo "清理超过6个月的知识库文件..."
find "$DIARY_DIR/knowledge" -name "*.md" -mtime +180 -exec echo "删除: {}" \; -delete

# 3. 更新MEMORY.md中的引用（如果需要）
echo "检查MEMORY.md中的过期引用..."
# 这里可以添加逻辑检查MEMORY.md中引用的文件是否还存在

echo "=== 清理完成 ==="
echo "清理时间: $(date)"