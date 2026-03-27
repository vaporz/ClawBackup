---
name: image-search
description: 使用火山引擎 volcengine-web-search 搜索网络图片。使用场景：(1) 为文章搜索配图，(2) 搜索特定主题的高清图片，(3) 查找IP形象的参考图。
---

# 图片搜索（火山引擎）

使用火山引擎 `volcengine-web-search` 搜索网络图片。

## 搜索配置

需要设置环境变量：
```bash
export VOLCENGINE_ACCESS_KEY="your_access_key"
export VOLCENGINE_SECRET_KEY="your_secret_key"
```

## 使用方法

```bash
cd ~/.openclaw/workspace/skills/volcengine-web-search
python3 scripts/web_search_volc.py "搜索关键词"
```

搜索图片（带图片模式）：
```bash
python3 scripts/web_search_volc.py "月球全景图 高清" image
```

返回5条搜索结果摘要或图片URL。

## 工作目录

脚本位于：`~/.openclaw/workspace/skills/volcengine-web-search/scripts/web_search_volc.py`

## 返回格式

- 文本搜索：返回5条搜索结果摘要
- 图片搜索：返回5条图片URL

## 常见搜索

- 文章配图：关键词 + "高清图片" / "壁纸"
- IP参考图：角色名 + "表情包" / "Q版"
- 航天主题："星空" / "月球" / "火箭发射"