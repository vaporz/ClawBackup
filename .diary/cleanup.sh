#!/bin/bash
# 日记系统清理脚本
# 每月1日凌晨3点执行

echo "=== 日记系统清理脚本开始执行 ==="
echo "执行时间: $(date)"
echo ""

# 切换到日记目录
cd "$(dirname "$0")" || exit 1

# 1. 清理工作日志（保留3个月）
echo "1. 清理工作日志（保留3个月）..."
CURRENT_YEAR_MONTH=$(date +%Y-%m)
THREE_MONTHS_AGO=$(date -d "3 months ago" +%Y-%m)

if [ -d "logs" ]; then
    for dir in logs/*; do
        if [ -d "$dir" ]; then
            dir_name=$(basename "$dir")
            # 比较年月，删除3个月前的日志
            if [[ "$dir_name" < "$THREE_MONTHS_AGO" ]]; then
                echo "  删除过期工作日志: $dir"
                rm -rf "$dir"
            fi
        fi
    done
else
    echo "  工作日志目录不存在，跳过清理"
fi

echo ""

# 2. 清理知识库（保留6个月）
echo "2. 清理知识库（保留6个月）..."
SIX_MONTHS_AGO=$(date -d "6 months ago" +%Y-%m)

if [ -d "knowledge" ]; then
    # 知识库文件直接放在knowledge目录下，按文件名判断
    for file in knowledge/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            # 假设文件名格式为 YYYY-MM-*.md
            file_date=$(echo "$filename" | grep -o '^[0-9]\{4\}-[0-9]\{2\}')
            if [ -n "$file_date" ] && [[ "$file_date" < "$SIX_MONTHS_AGO" ]]; then
                echo "  删除过期知识库文件: $filename"
                rm "$file"
            fi
        fi
    done
else
    echo "  知识库目录不存在，跳过清理"
fi

echo ""

# 3. 个人日记永久保留，不清理
echo "3. 个人日记永久保留，跳过清理"
echo ""

# 4. 闪念记录（保留1个月）
echo "4. 清理闪念记录（保留1个月）..."
ONE_MONTH_AGO=$(date -d "1 month ago" +%Y-%m-%d)

if [ -d "flash-notes" ]; then
    for file in flash-notes/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            # 文件名格式为 YYYY-MM-DD-flash.md
            file_date=$(echo "$filename" | grep -o '^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
            if [ -n "$file_date" ] && [[ "$file_date" < "$ONE_MONTH_AGO" ]]; then
                echo "  删除过期闪念记录: $filename"
                rm "$file"
            fi
        fi
    done
else
    echo "  闪念记录目录不存在，跳过清理"
fi

echo ""
echo "=== 清理完成 ==="
echo "清理时间: $(date)"