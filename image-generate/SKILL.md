---
name: image-generate
description: 使用火山引擎 Seedream 5.0 Lite API 生成图片。支持文生图和图生图两种模式。使用场景：(1) 为文章创作插图，(2) 基于参考图生成变体，(3) 创建IP形象的配图。
metadata: {"requires":{"env":["VOLCENGINE_API_TOKEN"]}}
---

# 图片生成（火山引擎 Seedream 5.0 Lite）

使用火山引擎豆包·视觉生成大模型生成图片。

## API 端点

```
https://ark.cn-beijing.volces.com/api/v3/images/generations
```

## 环境变量

```bash
export VOLCENGINE_API_TOKEN="your_api_token"
```

## 文生图（不使用参考图）

```python
import requests
import os

url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'
payload = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': '你的图片描述',
    'sequential_image_generation': 'disabled',
    'response_format': 'url',
    'size': '1920x1920',
    'stream': False,
    'watermark': False
}
headers = {'Authorization': 'Bearer ' + os.environ.get('VOLCENGINE_API_TOKEN')}
resp = requests.post(url, json=payload, headers=headers)
print(resp.json()['data'][0]['url'])
```

## 图生图（使用参考图）

```python
import requests
import os

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
headers = {'Authorization': 'Bearer ' + os.environ.get('VOLCENGINE_API_TOKEN')}
resp = requests.post(url, json=payload, headers=headers)
print(resp.json()['data'][0]['url'])
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `model` | doubao-seedream-5-0-260128 |
| `prompt` | 图片描述，支持中文 |
| `image` | 参考图URL（仅图生图需要） |
| `size` | 输出尺寸，如 1920x1920 |
| `response_format` | 返回格式，设为 url |
| `watermark` | 是否加水印，建议 false |

## 注意事项

- 图片尺寸至少 3686400 像素（如 1920x1920）
- 图生图必须提供公网可访问的参考图URL
- 文生图不需要 `image` 参数
- 参考图URL可使用七牛云CDN（如 `http://images.kanxingkeji.com/flash.jpg`）

## IP形象参考图URL

- 狸花猫Flash: `http://images.kanxingkeji.com/flash.jpg`
- 边牧Neo: `http://images.kanxingkeji.com/neo.jpg`