# Workspace Cleaner 基础使用示例

## 场景1：手动清理工作区

### 最简单的方式
```bash
# 在工作区根目录执行
python cleanup.py
```

输出示例：
```
开始清理工作区: /home/user/workspace
策略: balanced
--------------------------------------------------
找到 156 个待处理文件
保留: IDENTITY.md (core)
归档: temp_file.tmp -> 归档/2024-03/temp/temp_file_20240329_143022.tmp
归档: report-v1.md -> 归档/2024-03/versions/report_20240329_143022.md
删除到回收站: old_cache.log
...
==================================================
清理完成报告
==================================================
总文件数: 156
处理文件: 156
保留文件: 42
归档文件: 89
删除文件: 25
节省空间: 15.32 MB
```

### 模拟运行（不实际执行）
```bash
python cleanup.py --dry-run
```

### 指定工作区路径
```bash
python cleanup.py --workspace /path/to/your/workspace
```

## 场景2：配置清理策略

### 查看当前配置
```bash
cat .cleanup/config.yaml
```

### 使用严格策略
```bash
python cleanup.py --strategy strict
```
- 只保留核心文件
- 其他文件全部归档或删除

### 使用宽松策略
```bash
python cleanup.py --strategy loose
```
- 保留较多文件
- 只清理明显临时文件

## 场景3：管理回收站

### 查看回收站内容
```bash
python cleanup.py --list-recycle
```

输出示例：
```
回收站内容:
 1. temp_file_20240328.tmp         原路径: /workspace/temp_file.tmp
 2. old_report_20240327.md         原路径: /workspace/reports/old.md
 3. debug_log_20240326.log         原路径: /workspace/logs/debug.log
```

### 恢复特定文件
```bash
# 恢复包含"report"的文件
python cleanup.py --restore report

# 恢复所有文件
python cleanup.py --restore all
```

### 交互式恢复
```bash
python cleanup.py --list-recycle
# 然后根据提示输入文件编号
```

## 场景4：集成到工作流

### 任务完成后清理
```bash
# 完成报告撰写后
完成报告撰写任务
python cleanup.py --strategy balanced
```

### 每日清理脚本
```bash
#!/bin/bash
# daily_cleanup.sh

WORKSPACE="/home/user/workspace"
LOG_FILE="$WORKSPACE/清理日志.txt"

echo "=== 每日清理 $(date) ===" >> "$LOG_FILE"
cd "$WORKSPACE" && python cleanup.py >> "$LOG_FILE" 2>&1
echo "清理完成" >> "$LOG_FILE"
```

### 每周深度清理
```bash
#!/bin/bash
# weekly_deep_clean.sh

WORKSPACE="/home/user/workspace"
echo "开始每周深度清理..."
cd "$WORKSPACE" && python cleanup.py --strategy strict
echo "深度清理完成"
```

## 场景5：问题诊断

### 检查工作区状态
```bash
# 模拟运行查看文件分类
python cleanup.py --dry-run | head -20
```

### 查看详细日志
```bash
# 启用调试输出
python cleanup.py 2>&1 | tee cleanup.log
```

### 检查归档目录
```bash
ls -la 归档/
# 查看按月组织的归档
ls -la 归档/2024-03/
```

## 场景6：自定义配置

### 修改配置文件
```yaml
# .cleanup/config.yaml
strategy: "balanced"
retention:
  temp_files: "archive_14d"  # 临时文件只保留14天
  cache_files: "delete_3d"   # 缓存文件3天后删除
```

### 添加自定义文件规则
```bash
# 创建自定义规则文件
cat > .cleanup/custom_rules.yaml << EOF
rules:
  - name: "项目文件"
    patterns: ["*.prj", "*.project"]
    action: "keep"
    priority: 90
    
  - name: "数据文件"
    patterns: ["*.data", "*.dataset"]
    action: "archive_90d"
EOF
```

## 实用技巧

### 技巧1：定期检查
```bash
# 每月检查一次配置
python setup.py --configure
```

### 技巧2：备份重要文件
```bash
# 清理前备份核心文件
cp IDENTITY.md IDENTITY.md.backup
cp AGENTS.md AGENTS.md.backup
```

### 技巧3：监控清理效果
```bash
# 查看清理历史
ls -la 归档/清理报告*.json

# 查看最新报告
cat 归档/清理报告.json | python -m json.tool
```

### 技巧4：与其他工具集成
```bash
# 与find命令结合，查找大文件
find . -type f -size +10M -exec ls -lh {} \;

# 清理前先查看
python cleanup.py --dry-run | grep -E "(归档|删除)"
```

## 常见问题解决

### 问题1：清理速度慢
```bash
# 调整性能设置
echo "performance:
  max_concurrent: 5
  max_depth: 3" >> .cleanup/config.yaml
```

### 问题2：误删重要文件
```bash
# 立即从回收站恢复
python cleanup.py --list-recycle
# 找到文件编号后
python cleanup.py --restore 文件编号
```

### 问题3：归档目录过大
```bash
# 清理过期归档
find 归档 -type f -mtime +90 -delete
find 归档 -type d -empty -delete
```

### 问题4：权限问题
```bash
# 确保有读写权限
chmod -R 755 .
chown -R user:user .
```

## 最佳实践

### 每日习惯
1. **任务后清理**：每个任务完成后简单整理
2. **下班前检查**：检查工作区，归档临时文件
3. **版本控制**：重要文件提交到版本控制

### 每周维护
1. **周日晚上清理**：设置定时任务自动清理
2. **检查回收站**：恢复误删文件，清理过期文件
3. **更新配置**：根据使用情况调整策略

### 每月整理
1. **深度清理**：使用strict策略深度清理
2. **归档整理**：整理归档目录，删除过期文件
3. **规则优化**：更新文件识别规则

---

**开始使用：**
```bash
# 最简单的开始
cd /your/workspace
python cleanup.py --dry-run  # 先模拟运行
python cleanup.py            # 实际执行
```

保持工作区整洁，让工作更高效！🧹