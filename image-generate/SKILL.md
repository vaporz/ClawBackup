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

## 图生图（使用单张参考图）

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

## 图生图（使用多张参考图）

火山引擎支持使用多张参考图生成单张图片，适用于需要融合多个IP形象或元素的场景。

```python
import requests
import os

url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'
payload = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': '基于两张参考图中的形象，生成儿童绘本风格图片',
    'image': [
        'http://images.kanxingkeji.com/flash.jpg',  # 第一张参考图
        'http://images.kanxingkeji.com/neo.jpg'     # 第二张参考图
    ],  # ✅ 使用数组格式传递多张参考图
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

**官方示例**：
```bash
curl -X POST https://ark.cn-beijing.volces.com/api/v3/images/generations \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $ARK_API_KEY" \
 -d '{
 "model": "doubao-seedream-5-0-260128",
 "prompt": "将图1的服装换为图2的服装",
 "image": ["https://example.com/image1.png", "https://example.com/image2.png"],
 "sequential_image_generation": "disabled",
 "response_format": "url",
 "size": "2K",
 "stream": false,
 "watermark": true
}'
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `model` | doubao-seedream-5-0-260128 |
| `prompt` | 图片描述，支持中文 |
| `image` | 参考图URL（仅图生图需要）<br>• 单张参考图：字符串格式 `"url"`<br>• 多张参考图：数组格式 `["url1", "url2"]` |
| `size` | 输出尺寸，如 1920x1920 |
| `response_format` | 返回格式，设为 url |
| `watermark` | 是否加水印，建议 false |

## 注意事项

- 图片尺寸至少 3686400 像素（如 1920x1920）
- 图生图必须提供公网可访问的参考图URL
- 文生图不需要 `image` 参数
- 参考图URL可使用七牛云CDN（如 `http://images.kanxingkeji.com/flash.jpg`）
- **多张参考图**：使用数组格式 `["url1", "url2"]`，适用于融合多个IP形象
- **提示词优化**：使用多张参考图时，提示词应明确描述各参考图的用途

## IP形象参考图URL

- 狸花猫Flash: `http://images.kanxingkeji.com/flash.jpg`
- 边牧Neo: `http://images.kanxingkeji.com/neo.jpg`

### 多张参考图使用示例

**生成包含Flash和Neo的封面图**：
```python
payload = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': '基于两张参考图中的狸花猫Flash和边牧Neo形象，生成儿童绘本风格封面图',
    'image': [
        'http://images.kanxingkeji.com/flash.jpg',
        'http://images.kanxingkeji.com/neo.jpg'
    ],
    'size': '1920x1920',
    'response_format': 'url',
    'stream': False,
    'watermark': False
}
```

**提示词要点**：
1. 明确说明参考图数量（"基于两张参考图"）
2. 描述每个参考图的角色（"狸花猫Flash"、"边牧Neo"）
3. 指定各形象在场景中的位置（"Flash在飞船里"、"Neo在飞船旁"）

## 💡 经验总结

### 关键发现（2026年4月3日）
1. **多张参考图支持**：火山引擎支持 `image: ["url1", "url2"]` 数组格式
2. **与单张参考图的区别**：
   - 单张：`image: "url"`（字符串）
   - 多张：`image: ["url1", "url2"]`（数组）
3. **官方示例确认**：多张参考图是官方支持功能

### 常见错误
1. ❌ 使用文生图生成IP形象（特征不准确）
2. ❌ 只提供单张参考图但期望多个IP形象
3. ❌ 混淆文生图和图生图API参数

### 正确流程
1. ✅ 确认需求：需要几个IP形象？
2. ✅ 选择API：单张参考图 vs 多张参考图
3. ✅ 准备参考图：确保所有参考图URL可访问
4. ✅ 编写提示词：明确描述各参考图的用途
5. ✅ 设置参数：正确使用数组格式

### 实际应用
- **封面图**：多张参考图（Flash + Neo + 场景）
- **单角色图**：单张参考图（Flash 或 Neo）
- **场景图**：文生图（无IP形象，纯场景）