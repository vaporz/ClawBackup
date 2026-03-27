---
name: image-preprocess
description: 使用 ffmpeg 压缩图片以供图像识别。使用场景：(1) 使用 volc-vision 识别图片前预处理，(2) 批量压缩图片节省存储空间。压缩后图片大小减少 90%+，识别效果几乎不变。
---

# 图片识别预处理

使用 ffmpeg 将图片压缩到合适的大小供图像识别使用。

## 使用方法

```bash
ffmpeg -i "<原图>" -vf "scale='if(gt(iw,ih),1000,-1)':'if(gt(iw,ih),-1,1000)'" -c:v libwebp -quality 80 "<输出.webp>" -y
```

## 参数说明

- 输入：任意格式图片（jpg, png, webp等）
- 输出：webp格式，分辨率长/宽 ≤ 1000像素
- `-quality 80`: 质量80%，平衡体积和画质
- `-y`: 覆盖已存在的输出文件

## 示例

```bash
# 压缩单张图片
ffmpeg -i "photo.jpg" -vf "scale='if(gt(iw,ih),1000,-1)':'if(gt(iw,ih),-1,1000)'" -c:v libwebp -quality 80 "photo_compressed.webp" -y

# 批量压缩（bash循环）
for f in *.jpg; do ffmpeg -i "$f" -vf "scale='if(gt(iw,ih),1000,-1)':'if(gt(iw,ih),-1,1000)'" -c:v libwebp -quality 80 "${f%.*}.webp" -y; done
```

## 原理

- 长边压缩到1000像素，短边按比例缩放
- 转webp格式比jpg/png体积小90%+
- 识别模型需要的像素数远小于原始图片