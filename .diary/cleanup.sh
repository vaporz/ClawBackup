#!/bin/bash
# 日记系统清理脚本
# 每月1日凌晨3点执行

echo "=== 日记系统清理开始 ==="
echo "执行时间: $(date)"
echo "工作目录: $(pwd)"
echo

# 设置目录
DIARY_DIR="$(dirname "$0")"
LOGS_DIR="$DIARY_DIR/logs"
KNOWLEDGE_DIR="$DIARY_DIR/knowledge"

# 1. 清理工作日志（保留3个月）
echo "1. 清理工作日志（保留3个月）"
CURRENT_YEAR=$(date +%Y)
CURRENT_MONTH=$(date +%m)

# 计算3个月前的年月
THREE_MONTHS_AGO=$(date -d "3 months ago" +%Y-%m)
THREE_MONTHS_AGO_YEAR=$(echo $THREE_MONTHS_AGO | cut -d'-' -f1)
THREE_MONTHS_AGO_MONTH=$(echo $THREE_MONTHS_AGO | cut -d'-' -f2)

echo "当前年月: $CURRENT_YEAR-$CURRENT_MONTH"
echo "清理阈值: $THREE_MONTHS_AGO 之前的日志"

# 遍历日志目录
if [ -d "$LOGS_DIR" ]; then
    for year_dir in "$LOGS_DIR"/*; do
        if [ -d "$year_dir" ]; then
            year=$(basename "$year_dir")
            for month_dir in "$year_dir"/*; do
                if [ -d "$month_dir" ]; then
                    month=$(basename "$month_dir")
                    dir_date="$year-$month"
                    
                    # 比较日期
                    if [[ "$dir_date" < "$THREE_MONTHS_AGO" ]]; then
                        echo "删除过期日志目录: $dir_date"
                        rm -rf "$month_dir"
                    else
                        echo "保留日志目录: $dir_date"
                    fi
                fi
            done
            
            # 如果年份目录为空，删除它
            if [ -z "$(ls -A "$year_dir")" ]; then
                echo "删除空年份目录: $year"
                rmdir "$year_dir"
            fi
        fi
    done
else
    echo "日志目录不存在: $LOGS_DIR"
fi

echo

# 2. 清理知识库（保留6个月）
echo "2. 清理知识库（保留6个月）"
SIX_MONTHS_AGO=$(date -d "6 months ago" +%Y-%m)
SIX_MONTHS_AGO_YEAR=$(echo $SIX_MONTHS_AGO | cut -d'-' -f1)
SIX_MONTHS_AGO_MONTH=$(echo $SIX_MONTHS_AGO | cut -d'-' -f2)

echo "当前年月: $CURRENT_YEAR-$CURRENT_MONTH"
echo "清理阈值: $SIX_MONTHS_AGO 之前的知识"

# 知识库文件按最后修改时间清理
if [ -d "$KNOWLEDGE_DIR" ]; then
    echo "检查知识库文件..."
    find "$KNOWLEDGE_DIR" -type f -name "*.md" | while read file; do
        file_mtime=$(stat -c %Y "$file")
        six_months_ago_ts=$(date -d "6 months ago" +%s)
        
        if [ $file_mtime -lt $six_months_ago_ts ]; then
            echo "删除过期知识文件: $(basename "$file") (修改于: $(date -d @$file_mtime +%Y-%m-%d))"
            rm "$file"
        else
            echo "保留知识文件: $(basename "$file") (修改于: $(date -d @$file_mtime +%Y-%m-%d))"
        fi
    done
    
    # 清理空目录
    find "$KNOWLEDGE_DIR" -type d -empty -delete
else
    echo "知识库目录不存在: $KNOWLEDGE_DIR"
fi

echo

# 3. 清理闪念记录（保留1个月）
echo "3. 清理闪念记录（保留1个月）"
FLASH_NOTES_DIR="$DIARY_DIR/flash-notes"
ONE_MONTH_AGO=$(date -d "1 month ago" +%Y-%m-%d)

if [ -d "$FLASH_NOTES_DIR" ]; then
    echo "清理阈值: $ONE_MONTH_AGO 之前的闪念"
    
    find "$FLASH_NOTES_DIR" -type f -name "*.md" | while read file; do
        filename=$(basename "$file")
        # 从文件名提取日期：YYYY-MM-DD-flash.md
        file_date=$(echo "$filename" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
        
        if [ -n "$file_date" ]; then
            if [[ "$file_date" < "$ONE_MONTH_AGO" ]]; then
                echo "删除过期闪念: $filename"
                rm "$file"
            else
                echo "保留闪念: $filename"
            fi
        fi
    done
else
    echo "闪念目录不存在: $FLASH_NOTES_DIR"
fi

echo

# 4. 输出清理统计
echo "4. 清理完成统计"
echo "目录结构:"
find "$DIARY_DIR" -type d | sort | sed 's|.*/|    |g' | awk '{print "    " $0}'

echo
echo "各目录文件数量:"
for dir in "$DIARY_DIR"/*; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        file_count=$(find "$dir" -type f | wc -l)
        echo "    $dir_name: $file_count 个文件"
    fi
done

echo
echo "=== 日记系统清理完成 ==="
echo "下次清理时间: 下月1日凌晨3点"
echo "清理策略:"
echo "  - 工作日志: 保留3个月"
echo "  - 知识库: 保留6个月"
echo "  - 闪念记录: 保留1个月"
echo "  - 个人日记: 永久保留"