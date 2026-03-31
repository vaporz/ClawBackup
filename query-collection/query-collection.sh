#!/bin/bash
# Query Collection Skill - 基础查询包装脚本

set -e

# 使用固定的工作区路径
WORKSPACE_DIR="/home/zx/.openclaw/workspace-infocollecter"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到python3"
    exit 1
fi

# 检查数据库文件
DB_FILE="$WORKSPACE_DIR/data/history/history.db"
if [ ! -f "$DB_FILE" ]; then
    echo "❌ 错误: 数据库文件不存在: $DB_FILE"
    echo "请先运行信息收集器创建数据库"
    exit 1
fi

# 执行查询
cd "$WORKSPACE_DIR"
exec python3 scripts/query_history.py "$@"