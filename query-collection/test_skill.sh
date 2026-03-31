#!/bin/bash
# 测试Query Collection Skill

echo "🧪 测试Query Collection Skill..."
echo "=" * 60

# 测试基础查询
echo "1. 测试基础查询 (JSON格式):"
./query-collection.sh 20260330 2 desc | head -5
echo

echo "2. 测试基础查询 (可读格式):"
./query-collection.sh 20260330 2 desc --human | head -10
echo

# 测试高级查询
echo "3. 测试高级查询 (JSON格式):"
./query-collection-advanced.sh --date 20260330 --limit 2 | head -5
echo

echo "4. 测试高级查询 (可读格式):"
./query-collection-advanced.sh --date 20260330 --limit 2 --human | head -10
echo

echo "5. 测试条件查询:"
./query-collection-advanced.sh --date 20260330 --has-summary --limit 1 --human | head -10
echo

echo "6. 测试安静模式:"
./query-collection-advanced.sh --date 20260330 --limit 1 --quiet | head -5
echo

echo "✅ Skill测试完成"
echo "=" * 60
echo "使用方法:"
echo "  ./query-collection.sh [日期] [条数] [排序] [--human]"
echo "  ./query-collection-advanced.sh [选项]"
echo
echo "详细帮助:"
echo "  ./query-collection.sh --help"
echo "  ./query-collection-advanced.sh --help"