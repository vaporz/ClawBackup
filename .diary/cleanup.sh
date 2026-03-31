#!/bin/bash
# Agent Diary 清理脚本
# 每月1日自动执行，清理过期文件
# 版本: 1.0
# 创建: 2026-03-29

set -e

DIARY_DIR="$(dirname "$0")"
CURRENT_YEAR=$(date +%Y)
CURRENT_MONTH=$(date +%m)
CURRENT_DAY=$(date +%d)

echo "=== Agent Diary 清理脚本 ==="
echo "执行时间: $(date)"
echo "工作目录: $DIARY_DIR"
echo ""

# 只在每月1日执行清理
if [ "$CURRENT_DAY" != "01" ]; then
    echo "⚠️  今天不是每月1日，跳过清理"
    echo "下次清理时间: 下个月1日"
    exit 0
fi

echo "📅 开始每月清理..."
echo ""

# 1. 清理工作日志（保留3个月）
LOGS_DIR="$DIARY_DIR/logs"
if [ -d "$LOGS_DIR" ]; then
    echo "🧹 清理工作日志（保留3个月）..."
    
    # 计算3个月前的年月
    THREE_MONTHS_AGO=$(date -d "3 months ago" +%Y-%m)
    THREE_MONTHS_AGO_YEAR=$(echo "$THREE_MONTHS_AGO" | cut -d'-' -f1)
    THREE_MONTHS_AGO_MONTH=$(echo "$THREE_MONTHS_AGO" | cut -d'-' -f2)
    
    # 删除3个月前的日志目录
    for year_dir in "$LOGS_DIR"/*; do
        if [ -d "$year_dir" ]; then
            year=$(basename "$year_dir")
            for month_dir in "$year_dir"/*; do
                if [ -d "$month_dir" ]; then
                    month=$(basename "$month_dir")
                    
                    # 比较年月
                    if [ "$year" -lt "$THREE_MONTHS_AGO_YEAR" ] || \
                       ([ "$year" -eq "$THREE_MONTHS_AGO_YEAR" ] && [ "$month" -lt "$THREE_MONTHS_AGO_MONTH" ]); then
                        echo "  删除: $year-$month"
                        rm -rf "$month_dir"
                    fi
                fi
            done
            
            # 如果年份目录为空，删除它
            if [ -z "$(ls -A "$year_dir")" ]; then
                rmdir "$year_dir"
            fi
        fi
    done
    echo "✅ 工作日志清理完成"
else
    echo "⚠️  工作日志目录不存在: $LOGS_DIR"
fi

echo ""

# 2. 清理知识库（保留6个月）
KNOWLEDGE_DIR="$DIARY_DIR/knowledge"
if [ -d "$KNOWLEDGE_DIR" ]; then
    echo "📚 清理知识库（保留6个月）..."
    
    # 计算6个月前的日期
    SIX_MONTHS_AGO=$(date -d "6 months ago" +%s)
    
    # 删除6个月前的知识文件
    find "$KNOWLEDGE_DIR" -name "*.md" -type f | while read -r file; do
        file_mtime=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file")
        if [ "$file_mtime" -lt "$SIX_MONTHS_AGO" ]; then
            filename=$(basename "$file")
            echo "  删除过期知识: $filename"
            rm "$file"
        fi
    done
    echo "✅ 知识库清理完成"
else
    echo "⚠️  知识库目录不存在: $KNOWLEDGE_DIR"
fi

echo ""

# 3. 个人日记永久保留，不清理
echo "📖 个人日记永久保留"
echo "   位置: $DIARY_DIR/$CURRENT_YEAR/$CURRENT_MONTH/"
echo "   保留策略: 永久"

echo ""

# 4. 闪念记录（日记写作时会自动整合，可选择性清理）
FLASH_NOTES_DIR="$DIARY_DIR/flash-notes"
if [ -d "$FLASH_NOTES_DIR" ]; then
    echo "💡 检查闪念记录..."
    flash_count=$(find "$FLASH_NOTES_DIR" -name "*.md" -type f | wc -l)
    echo "   当前闪念文件数: $flash_count"
    echo "   建议: 写日记时会自动整合闪念，可手动清理已整合的文件"
fi

echo ""

# 5. 创建下个月目录结构
NEXT_MONTH=$(date -d "next month" +%Y-%m)
NEXT_YEAR=$(echo "$NEXT_MONTH" | cut -d'-' -f1)
NEXT_MONTH_NUM=$(echo "$NEXT_MONTH" | cut -d'-' -f2)

echo "📁 准备下个月目录结构..."
mkdir -p "$DIARY_DIR/logs/$NEXT_YEAR-$NEXT_MONTH_NUM"
mkdir -p "$DIARY_DIR/$NEXT_YEAR/$NEXT_MONTH_NUM"
echo "✅ 创建: logs/$NEXT_YEAR-$NEXT_MONTH_NUM/"
echo "✅ 创建: $NEXT_YEAR/$NEXT_MONTH_NUM/"

echo ""
echo "=== 清理完成 ==="
echo "📊 清理统计:"
echo "   - 工作日志: 保留最近3个月"
echo "   - 知识库: 保留最近6个月"
echo "   - 个人日记: 永久保留"
echo "   - 下个月目录: 已创建"
echo ""
echo "💡 提示:"
echo "   1. 工作日志用于记录具体任务，为写日记提供事实依据"
echo "   2. 知识库用于存储规范流程，为决策提供背景知识"
echo "   3. 个人日记用于反思成长，记录主观感受和思考"
echo ""
echo "下次清理: 下个月1日"