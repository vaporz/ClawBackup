---
name: image-recognition
description: 使用火山引擎 volc-vision API 识别图片内容。支持通用物体检测、文字识别(OCR)、场景分类等。触发场景：(1) 用户要求识别图片内容，(2) 需要描述图片，(3) 提取图片中的文字，(4) 分析图片元素。
---

# 图片识别 (volc-vision)

快速识别图片内容，提取文字，分析图像元素。

## 识别流程

### 1. 预处理图片（推荐）

使用 ffmpeg 压缩图片，减少体积提高识别速度：

```bash
ffmpeg -i "<原图>" -vf "scale='if(gt(iw,ih),1000,-1)':'if(gt(iw,ih),-1,1000)'" -c:v libwebp -quality 80 "<输出.webp>" -y
```

**说明**：
- 分辨率压到长/宽 ≤ 1000 像素
- 转成 webp 格式可节省 90%+ 文件大小
- 识别效果几乎不变

### 2. 调用 API 识别

#### Python 示例

```python
import requests

url = 'https://visual.volcengineapi.com/v1/visual/recognition'
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
payload = {
    'image_url': 'https://example.com/image.webp',  # 公网URL或base64
    'model': 'general_object_detection',  # 模型选择
}

resp = requests.post(url, json=payload, headers=headers)
result = resp.json()
print(result)
```

### 使用火山引擎视觉模型（推荐）

火山引擎的视觉理解模型支持直接识别图片内容，比 volc-vision API 更简单：

```python
import requests
import base64

# 读取图片并转为 base64
with open('image.webp', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()

url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
headers = {
    'Authorization': f'Bearer {os.environ.get("VOLCENGINE_API_TOKEN")}',
    'Content-Type': 'application/json'
}
payload = {
    'model': 'doubao-1-5-vision-pro-32k-250115',  # 视觉模型
    'messages': [
        {
            'role': 'user',
            'content': [
                {'type': 'image_url', 'image_url': {'url': f'data:image/webp;base64,{img_data}'}},
                {'type': 'text', 'text': '请详细描述这张图片'}
            ]
        }
    ],
    'max_tokens': 500
}

resp = requests.post(url, json=payload, headers=headers, timeout=60)
result = resp.json()
print(result['choices'][0]['message']['content'])
```

**可用视觉模型**：
- `doubao-1-5-vision-pro-32k-250115` - 推荐，效果好
- `doubao-1-5-vision-lite-250315` - 轻量版

### volc-vision API（备用）

| 模型 | 用途 |
|------|------|
| `general_object_detection` | 通用物体检测 |
| `ocr` | 文字识别 |
| `scene_classification` | 场景分类 |
| `face_detection` | 人脸检测 |

### 3. 解析结果

识别结果为 JSON，提取需要的字段：

```python
# 物体检测结果
objects = result['data']['detection']['objects']
for obj in objects:
    print(f"{obj['label']}: {obj['confidence']:.2f}")

# OCR 结果
texts = result['data']['ocr']['texts']
for text in texts:
    print(text['content'])
```

## 环境变量

```bash
export VOLCENGINE_ACCESS_KEY="your_access_key"
export VOLCENGINE_SECRET_KEY="your_secret_key"
```

或使用 API Token：

```bash
export VOLCENGINE_API_TOKEN="your_api_token"
```

## 常见场景

### 配图前了解图片内容

1. 用户需要为文章配图
2. 用这个 skill 识别候选图片
3. 提取关键词用于 alt 文本或描述

### 提取图片中的文字

使用 `ocr` 模型提取文字，用于：
- 截图转文字
- 名片信息提取
- 文档数字化

## 注意事项

- 图片需要公网可访问，或转成 base64
- 大图片建议先压缩
- 批量识别注意 API 限流

## 相关 Skills

- [image-preprocess](../image-preprocess/) - 图片压缩预处理
- [image-search](../image-search/) - 网络图片搜索
- [image-library](../image-library/) - 图片素材管理