# Query Collection Skill 安装说明

## 快速安装

### 1. 复制skill到目标agent的工作区
```bash
# 假设目标agent的工作区在 ~/.openclaw/workspace-writer
cp -r /home/zx/.openclaw/workspace-infocollecter/skills/query-collection \
      ~/.openclaw/workspace-writer/skills/
```

### 2. 测试安装
```bash
cd ~/.openclaw/workspace-writer/skills/query-collection
./query-collection.sh --help
```

### 3. 添加到PATH（可选）
```bash
# 创建符号链接
ln -s $(pwd)/query-collection.sh ~/.local/bin/query-collection
ln -s $(pwd)/query-collection-advanced.sh ~/.local/bin/query-collection-advanced

# 测试
query-collection --help
```

## 依赖检查

### 1. 必需依赖
```bash
# 检查Python3
python3 --version

# 检查SQLite
python3 -c "import sqlite3; print('SQLite版本:', sqlite3.sqlite_version)"
```

### 2. 可选依赖
```bash
# jq (用于JSON处理)
jq --version

# mail (用于邮件通知)
which mail
```

## 配置说明

### 1. 数据库路径配置
如果信息收集系统不在默认位置，需要修改脚本中的路径：
```bash
# 编辑query-collection.sh
vim skills/query-collection/query-collection.sh

# 修改WORKSPACE_DIR变量
WORKSPACE_DIR="/path/to/your/workspace-infocollecter"
```

### 2. 环境变量（可选）
```bash
# 可以在.bashrc或.zshrc中添加
export QUERY_COLLECTION_WORKSPACE="/path/to/workspace-infocollecter"
export QUERY_COLLECTION_DB="$QUERY_COLLECTION_WORKSPACE/data/history/history.db"
```

## 多agent部署

### 1. 团队部署
```bash
#!/bin/bash
# deploy_to_team.sh - 部署到团队所有agent

TEAM_AGENTS=(
    "~/.openclaw/workspace-writer"
    "~/.openclaw/workspace-chief-editor"
    "~/.openclaw/workspace-arteditor"
)

SOURCE_SKILL="/home/zx/.openclaw/workspace-infocollecter/skills/query-collection"

for agent_dir in "${TEAM_AGENTS[@]}"; do
    echo "部署到: $agent_dir"
    cp -r "$SOURCE_SKILL" "$agent_dir/skills/"
    chmod +x "$agent_dir/skills/query-collection/"*.sh
done

echo "✅ 已部署到 ${#TEAM_AGENTS[@]} 个agent"
```

### 2. 共享部署
```bash
# 部署到共享目录
SHARED_DIR="/shared/agent-skills"
cp -r skills/query-collection "$SHARED_DIR/"

# 各agent创建符号链接
ln -s "$SHARED_DIR/query-collection" ~/.openclaw/workspace-writer/skills/query-collection
```

## 权限设置

### 1. 脚本权限
```bash
# 确保脚本可执行
chmod +x query-collection.sh query-collection-advanced.sh test_skill.sh

# 检查权限
ls -la *.sh
```

### 2. 数据库权限
```bash
# 确保agent有读取权限
ls -la /home/zx/.openclaw/workspace-infocollecter/data/history/history.db

# 如果需要，调整权限
chmod 644 /home/zx/.openclaw/workspace-infocollecter/data/history/history.db
```

## 验证安装

### 1. 基本验证
```bash
# 运行测试脚本
./test_skill.sh

# 检查帮助文档
./query-collection.sh --help
./query-collection-advanced.sh --help
```

### 2. 功能验证
```bash
# 测试查询功能
./query-collection.sh $(date +%Y%m%d) 1

# 测试高级查询
./query-collection-advanced.sh --date $(date +%Y%m%d) --limit 1 --quiet
```

### 3. 集成验证
```bash
# 测试管道处理
./query-collection-advanced.sh --date $(date +%Y%m%d) --quiet | jq '.[0] | {title, source}'

# 测试文件输出
./query-collection-advanced.sh --date $(date +%Y%m%d) --output test.json
cat test.json | jq length
```

## 故障排除

### 1. 安装问题
```bash
# 问题：脚本不可执行
# 解决：添加执行权限
chmod +x *.sh

# 问题：Python找不到
# 解决：安装Python3
sudo apt-get install python3  # Ubuntu/Debian
brew install python3          # macOS
```

### 2. 路径问题
```bash
# 问题：数据库找不到
# 解决：检查路径配置
echo "当前工作区: $WORKSPACE_DIR"
ls -la "$WORKSPACE_DIR/data/history/"

# 问题：脚本找不到依赖
# 解决：检查Python路径
which python3
python3 -c "import sys; print(sys.path)"
```

### 3. 权限问题
```bash
# 问题：权限被拒绝
# 解决：检查文件权限
ls -la /home/zx/.openclaw/workspace-infocollecter/data/history/history.db

# 问题：无法写入输出文件
# 解决：检查目录权限
mkdir -p output
chmod 755 output
```

## 更新与维护

### 1. 更新skill
```bash
# 从源位置更新
cp -r /home/zx/.openclaw/workspace-infocollecter/skills/query-collection/* \
      skills/query-collection/

# 重新设置权限
chmod +x skills/query-collection/*.sh
```

### 2. 版本管理
```bash
# 查看当前版本
cat SKILL.md | grep -i version

# 备份旧版本
cp -r skills/query-collection skills/query-collection-backup-$(date +%Y%m%d)
```

## 卸载

### 1. 完全卸载
```bash
# 删除skill目录
rm -rf skills/query-collection

# 删除符号链接
rm -f ~/.local/bin/query-collection
rm -f ~/.local/bin/query-collection-advanced
```

### 2. 部分卸载
```bash
# 只删除脚本，保留文档
rm -f skills/query-collection/*.sh
```

## 支持与反馈

### 1. 获取帮助
- 查看SKILL.md获取详细文档
- 查看EXAMPLES.md获取使用示例
- 运行`./query-collection.sh --help`获取命令行帮助

### 2. 报告问题
```bash
# 收集诊断信息
./query-collection.sh --help > diagnostic.txt
python3 --version >> diagnostic.txt
ls -la /home/zx/.openclaw/workspace-infocollecter/data/history/ >> diagnostic.txt

# 报告问题时附上diagnostic.txt
```

### 3. 功能请求
- 在SKILL.md的"更新日志"部分查看计划功能
- 提交功能请求到项目issue tracker

---

**安装完成！现在可以开始使用Query Collection Skill了。** 🎉

参考文档：
- SKILL.md - 详细功能说明
- EXAMPLES.md - 使用示例
- 运行 `./query-collection.sh --help` - 命令行帮助