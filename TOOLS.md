# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### 图片识别预处理

使用 volc-vision 识别图片前，先用 ffmpeg 压缩：
1. 分辨率压到长/宽 ≤ 1000 像素
2. 转成 webp 格式

```bash
ffmpeg -i "<原图>" -vf "scale='if(gt(iw,ih),1000,-1)':'if(gt(iw,ih),-1,1000)'" -c:v libwebp -quality 80 "<输出.webp>" -y
```

可节省 90%+ 文件大小，识别效果几乎不变。

### 图片搜索（火山引擎）

使用火山引擎 `volcengine-web-search` 搜索网络：
```bash
cd /home/zx/.openclaw/workspace/skills/volcengine-web-search
VOLCENGINE_ACCESS_KEY=YOUR_ACCESS_KEY \
VOLCENGINE_SECRET_KEY=YOUR_SECRET_KEY \
python3 scripts/web_search_volc.py "搜索关键词"
```

搜索图片：
```bash
python3 scripts/web_search_volc.py "月球全景图 高清" image
```

返回 5 条搜索结果摘要或图片 URL。

### 图片库管理

图片库存放路径：`/home/zx/.openclaw/workspace-arteditor/image-library/`
- `raw/` - 原始下载图片
- `compressed/` - 压缩处理后图片 (用于识别)
- `descriptions/` - 图片描述文本文件

图片命名规范：`{序号}_{关键词}_{日期}.{ext}`

归档时在 `image-library/` 根目录创建 `{名称}.json` 记录元数据：
```json
{
  "name": "图片名称",
  "keywords": ["关键词1", "关键词2"],
  "date": "2026-03-25",
  "raw_file": "raw/xxx.jpg",
  "compressed_file": "compressed/xxx.webp",
  "description": "图片描述内容"
}
```

### 图片生成（火山引擎 Seedream 5.0 Lite）

**注意：图生图和文生图是同一个 API，但参数不同**

#### 1. 图生图 API（使用参考图）
```python
import requests

url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'
payload = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': '你的图片描述',
    'image': '参考图URL',  # 必填：公网可访问的参考图URL
    'sequential_image_generation': 'disabled',
    'response_format': 'url',
    'size': '1920x1920',
    'stream': False,
    'watermark': False
}
headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
resp = requests.post(url, json=payload, headers=headers)
print(resp.json()['data'][0]['url'])
```

#### 2. 文生图 API（不使用参考图）
```python
import requests

url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'
payload = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': '你的图片描述',  # 不需要 image 参数
    'sequential_image_generation': 'disabled',
    'response_format': 'url',
    'size': '1920x1920',
    'stream': False,
    'watermark': False
}
headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
resp = requests.post(url, json=payload, headers=headers)
print(resp.json()['data'][0]['url'])
```

### IP形象参考图URL（七牛云，国内可访问）
- 狸花猫Flash: `http://images.kanxingkeji.com/flash.jpg`
- 边牧Neo: `http://images.kanxingkeji.com/neo.jpg`

注意：
- 图片尺寸至少 3686400 像素 (如 1920x1920)
- **图生图** 需要加 `image` 参数 + 公网URL
- **文生图** 不需要 `image` 参数

---

Add whatever helps you do your job. This is your cheat sheet.