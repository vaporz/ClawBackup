---
name: image-library
description: 管理本地图片素材库，包括图片存储路径、命名规范和元数据归档。使用场景：(1) 下载和整理图片素材，(2) 建立图片索引方便查找，(3) 记录图片描述信息。
---

# 图片库管理

规范化的本地图片素材管理方案。

## 目录结构

```
~/.openclaw/workspace-arteditor/image-library/
├── raw/          # 原始下载图片
├── compressed/   # 压缩处理后图片（用于识别）
└── descriptions/ # 图片描述文本文件
```

## 命名规范

图片命名格式：`{序号}_{关键词}_{日期}.{ext}`

示例：
- `001_月球表面_2026-03-26.jpg`
- `002_火箭发射_2026-03-26.png`

## 元数据归档

每批图片归档时，在 `image-library/` 根目录创建 JSON 文件记录元数据：

```json
{
  "name": "图片名称",
  "keywords": ["关键词1", "关键词2"],
  "date": "2026-03-26",
  "raw_file": "raw/xxx.jpg",
  "compressed_file": "compressed/xxx.webp",
  "description": "图片描述内容"
}
```

## 工作流程

1. 下载原始图片 → 存入 `raw/`
2. 使用 image-preprocess 压缩 → 存入 `compressed/`
3. 用 volc-vision 识别图片 → 描述存入 `descriptions/`
4. 创建JSON元数据文件

## 查找图片

搜索图片库：
```bash
# 查找包含关键词的图片描述
grep -r "关键词" ~/.openclaw/workspace-arteditor/image-library/descriptions/
```