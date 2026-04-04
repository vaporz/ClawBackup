# PDF转长图片 Skill

**技能名称**: pdf-to-long-image  
**技能描述**: 将PDF文档转换为连续拼接的长图片，支持智能空白裁剪和多平台优化  
**创建时间**: 2026年4月3日  
**创建者**: 小美 🎨  
**适用场景**: 社交媒体分享、文档展示、长图制作

## 🎯 功能特点

### 核心功能
1. **PDF转长图片**: 将多页PDF无缝拼接为单张长图片
2. **智能空白裁剪**: 自动检测并移除页面间的空白区域
3. **文字完整性保护**: 保守裁剪策略，确保不丢失文字内容
4. **多分辨率支持**: 支持150-300 DPI高质量转换
5. **多格式输出**: PNG（无损）、JPEG（压缩）、WebP（网页优化）

### 平台优化
- **微信优化版**: 宽度1080px，JPG格式，带页眉页脚
- **微博优化版**: 宽度1000px，PNG格式，对比度增强  
- **网页优化版**: WebP格式，文件小加载快
- **高质量版**: 高DPI，PNG格式，适合打印

## 📁 文件结构

```
pdf-to-long-image/
├── SKILL.md                    # 技能说明文档
├── scripts/
│   ├── pdf_to_long_image.py           # 基础转换脚本
│   ├── pdf_to_long_image_optimized.py # 高质量优化版
│   ├── pdf_to_long_image_fixed.py     # 文字完整修复版
│   └── create_social_media_version.py # 社交媒体优化
└── examples/
    └── example_usage.py        # 使用示例
```

## 🔧 安装依赖

### 系统依赖
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### Python依赖
```bash
pip install pdf2image pillow numpy
```

## 🚀 快速开始

### 基础使用
```python
from scripts.pdf_to_long_image import pdf_to_long_image

# 基础转换
pdf_to_long_image(
    pdf_path="input.pdf",
    output_path="output.png",
    dpi=150
)
```

### 完整示例
```python
import os
from scripts.pdf_to_long_image_optimized import pdf_to_high_quality_long_image
from scripts.create_social_media_version import optimize_for_wechat

# 1. 转换为高质量长图
pdf_to_high_quality_long_image(
    "document.pdf",
    "document_high_quality.png",
    dpi=200
)

# 2. 创建微信优化版
optimize_for_wechat(
    "document_high_quality.png",
    "document_wechat.jpg"
)
```

## 📋 参数说明

### 主要参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `dpi` | int | 150 | 转换分辨率，越高越清晰 |
| `margin_removal` | int | 5 | 边缘移除像素 |
| `threshold` | float | 0.95 | 空白检测阈值 |
| `blank_height_ratio` | float | 0.1 | 空白检测区域比例 |

### 分辨率建议
- **社交媒体**: 150 DPI（平衡质量与大小）
- **网页展示**: 200 DPI（高清显示）
- **打印输出**: 300 DPI（印刷质量）

## 🔍 核心技术

### 1. 智能空白检测
```python
def detect_page_bottom_blank(image, threshold=0.95, blank_height_ratio=0.1):
    """
    检测页面底部的空白区域
    使用颜色阈值和像素密度分析
    """
    # 转换为灰度图
    gray = image.convert('L')
    img_array = np.array(gray)
    
    # 从底部开始检测
    start_row = int(height * (1 - blank_height_ratio))
    
    for row in range(start_row, height):
        row_pixels = img_array[row, :]
        white_pixels = np.sum(row_pixels > 250)
        white_ratio = white_pixels / width
        
        if white_ratio < threshold:
            return row - start_row
    
    return height - start_row
```

### 2. 保守裁剪策略
```python
def conservative_crop(image, min_margin=50):
    """
    保守裁剪：只移除确认为空白的边缘
    确保不丢失文字内容
    """
    # 严格阈值：只移除纯白区域
    white_threshold = 253  # 几乎纯白
    # 99%以上为纯白才认为是空白
```

### 3. 多平台优化
- **微信**: 宽度1080px，JPG格式，文件大小<10MB
- **微博**: 宽度1000px，PNG格式，对比度增强
- **网页**: WebP格式，自动缩放，优化加载

## ⚠️ 常见问题与解决方案

### 问题1: 文字丢失
**现象**: 转换后部分文字缺失  
**原因**: 空白检测过于激进，误裁文字区域  
**解决方案**:
1. 使用`pdf_to_long_image_fixed.py`（保守裁剪）
2. 调整`threshold`参数（提高阈值）
3. 增加`min_margin`（保留更多边距）

### 问题2: 文件过大
**现象**: 输出图片文件太大  
**解决方案**:
1. 降低`dpi`参数（如从200降到150）
2. 使用JPEG格式替代PNG
3. 启用压缩优化`optimize=True`

### 问题3: 颜色失真
**现象**: 图片颜色与原始PDF不一致  
**解决方案**:
1. 使用PNG格式（无损）
2. 检查PDF渲染设置
3. 使用`use_pdftocairo=True`（更好的渲染器）

### 问题4: 页面顺序错乱
**现象**: 页面拼接顺序错误  
**解决方案**:
1. 检查PDF页码顺序
2. 使用`first_page`和`last_page`参数控制范围
3. 手动指定页面列表

## 🎨 高级功能

### 自定义页眉页脚
```python
from scripts.create_social_media_version import add_social_media_header

# 添加自定义页眉
image_with_header = add_social_media_header(
    image,
    title="自定义标题",
    subtitle="自定义副标题"
)
```

### 批量处理
```python
import glob

# 批量转换多个PDF
pdf_files = glob.glob("documents/*.pdf")
for pdf_file in pdf_files:
    output_file = pdf_file.replace('.pdf', '_long.png')
    pdf_to_long_image(pdf_file, output_file)
```

### 进度监控
```python
# 添加进度回调
def progress_callback(current, total):
    print(f"处理中: {current}/{total}")

pdf_to_long_image_with_progress(pdf_file, output_file, callback=progress_callback)
```

## 📊 性能优化

### 内存优化
```python
# 分页处理，避免内存溢出
images = convert_from_path(pdf_path, dpi=dpi)
for i, img in enumerate(images):
    # 立即处理并释放内存
    processed = process_page(img)
    save_page(processed, f"page_{i}.jpg")
```

### 速度优化
```python
# 多线程处理
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for img in images:
        future = executor.submit(process_page, img)
        futures.append(future)
```

## 🔄 工作流程

### 标准工作流
```
输入PDF → 转换为图片列表 → 智能空白裁剪 → 拼接长图片 → 平台优化 → 输出
```

### 质量控制流程
1. **预处理检查**: 验证PDF可读性
2. **转换监控**: 检查每页转换质量
3. **文字完整性验证**: 确保不丢失内容
4. **文件大小检查**: 符合平台要求
5. **视觉质量检查**: 颜色、清晰度、拼接效果

## 📝 使用示例

### 示例1: 基础转换
```bash
python scripts/pdf_to_long_image.py input.pdf output.png
```

### 示例2: 微信优化
```bash
python scripts/create_social_media_version.py \
  --input input.pdf \
  --output wechat_version.jpg \
  --platform wechat \
  --title "文章标题" \
  --subtitle "副标题说明"
```

### 示例3: 批量处理
```bash
# 处理整个文件夹
for pdf in *.pdf; do
  python scripts/pdf_to_long_image_optimized.py "$pdf" "${pdf%.pdf}_long.png"
done
```

## 🎯 最佳实践

### 1. 预处理PDF
- 确保PDF文字可选中（非扫描件）
- 统一页面尺寸
- 移除不必要的空白页

### 2. 参数调优
- 首次使用：从默认参数开始
- 文字密集：提高`threshold`，增加`min_margin`
- 图片为主：可适当激进裁剪

### 3. 质量检查
- 检查第一页和最后一页
- 验证关键文字是否完整
- 检查拼接处是否自然

### 4. 文件管理
- 保留原始PDF
- 按用途分类输出文件
- 添加版本标识

## 🔍 调试技巧

### 调试模式
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 保存中间结果
save_intermediate_results = True
```

### 问题诊断
1. **检查原始PDF**: `pdftotext input.pdf - | head -20`
2. **检查单页转换**: 单独转换第一页检查质量
3. **检查空白检测**: 输出空白区域分析结果
4. **检查内存使用**: 监控转换过程内存占用

## 📚 学习资源

### 相关工具
- **pdf2image**: PDF转图片库
- **Pillow**: 图片处理库
- **poppler**: PDF渲染引擎
- **OpenCV**: 高级图像处理（可选）

### 参考文档
- [pdf2image文档](https://github.com/Belval/pdf2image)
- [Pillow文档](https://pillow.readthedocs.io/)
- [PDF标准](https://www.adobe.com/devnet/pdf/pdf_reference.html)

## 🚀 未来扩展

### 计划功能
1. **OCR文字识别**: 自动识别和优化文字区域
2. **智能分割**: 根据内容自动分节
3. **动画效果**: 创建滚动动画长图
4. **交互式长图**: 添加可点击区域

### 性能优化
1. **GPU加速**: 使用CUDA加速图片处理
2. **流式处理**: 支持超大PDF文件
3. **分布式处理**: 多机并行转换

## 💡 经验总结

### 从问题中学到的
1. **保守优于激进**: 空白检测宁可少裁，不可多裁
2. **验证很重要**: 转换后必须检查关键内容
3. **平台差异**: 不同平台有不同要求
4. **用户反馈**: 实际使用中发现的问题最有价值

### 技术要点
1. **PDF复杂性**: PDF格式复杂，需要多方案备选
2. **内存管理**: 大文件需要分块处理
3. **质量控制**: 自动化检查比人工更可靠
4. **可配置性**: 提供参数让用户调整

## 📞 支持与反馈

### 问题报告
遇到问题时，请提供：
1. PDF文件信息（页数、大小、类型）
2. 错误信息或问题现象
3. 使用的参数和代码
4. 期望的输出效果

### 贡献指南
欢迎贡献代码、文档或建议：
1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 更新文档和测试

---

**最后更新**: 2026年4月3日  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪  
**维护者**: 小美 🎨  

*让每一份文档都能完美呈现* ✨