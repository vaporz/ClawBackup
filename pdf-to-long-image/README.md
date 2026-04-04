# 📄 PDF转长图片 Skill

一个强大的PDF转长图片工具，专为社交媒体分享和文档展示优化。

## ✨ 特性

- ✅ **智能空白裁剪**：自动移除页面间空白，实现无缝拼接
- ✅ **文字完整性保护**：保守裁剪策略，确保不丢失文字
- ✅ **多平台优化**：微信、微博、网页专用版本
- ✅ **高质量输出**：支持150-300 DPI高清转换
- ✅ **多格式支持**：PNG、JPEG、WebP格式
- ✅ **易于使用**：命令行和Python API两种方式

## 🚀 快速开始

### 安装依赖
```bash
# 系统依赖
sudo apt-get install poppler-utils

# Python依赖
pip install pdf2image pillow numpy
```

### 基础使用
```bash
# 命令行
python scripts/pdf_to_long_image.py input.pdf output.png

# Python代码
from scripts.pdf_to_long_image import pdf_to_long_image
pdf_to_long_image("input.pdf", "output.png", dpi=150)
```

## 📋 使用场景

### 1. 社交媒体分享
```python
# 微信优化版
from scripts.create_social_media_version import optimize_for_wechat
optimize_for_wechat("input.pdf", "wechat_version.jpg")

# 微博优化版
from scripts.create_social_media_version import optimize_for_weibo
optimize_for_weibo("input.pdf", "weibo_version.png")
```

### 2. 文档展示
```python
# 高质量长图（适合打印）
from scripts.pdf_to_long_image_optimized import pdf_to_high_quality_long_image
pdf_to_high_quality_long_image("document.pdf", "high_quality.png", dpi=200)
```

### 3. 网页优化
```python
# WebP格式，加载更快
from scripts.pdf_to_long_image import pdf_to_long_image
pdf_to_long_image("document.pdf", "web_version.webp", dpi=150)
```

## 🔧 参数调优

### 分辨率选择
- **150 DPI**：社交媒体分享（平衡质量与大小）
- **200 DPI**：高清展示（网页、演示）
- **300 DPI**：打印输出（最高质量）

### 空白检测
- **默认阈值 0.95**：适合大多数文档
- **保守阈值 0.99**：确保文字不丢失
- **激进阈值 0.90**：最大化空白移除

### 输出格式
- **PNG**：无损质量，文件较大
- **JPEG**：有损压缩，文件较小
- **WebP**：现代格式，质量好文件小

## ⚡ 性能优化

### 大文件处理
```python
# 分页处理，避免内存溢出
from scripts.pdf_to_long_image import pdf_to_long_image
pdf_to_long_image("large.pdf", "output.png", dpi=120)  # 降低DPI
```

### 批量处理
```bash
# 批量转换文件夹内所有PDF
for pdf in *.pdf; do
  python scripts/pdf_to_long_image.py "$pdf" "${pdf%.pdf}_long.png"
done
```

## 🎯 最佳实践

### 1. 预处理PDF
- 确保PDF文字可选中（非扫描件）
- 统一页面尺寸
- 移除不必要的空白页

### 2. 转换后检查
- 验证关键文字是否完整
- 检查拼接处是否自然
- 确认文件大小符合平台要求

### 3. 平台适配
- **微信**：JPG格式，宽度1080px，<10MB
- **微博**：PNG格式，宽度1000px
- **网页**：WebP格式，自动缩放

## 🔍 故障排除

### 常见问题
1. **文字丢失**：使用`pdf_to_long_image_fixed.py`或提高阈值
2. **文件过大**：降低DPI或使用JPEG格式
3. **颜色失真**：使用PNG格式，检查PDF渲染
4. **内存不足**：分页处理或降低分辨率

### 调试模式
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 保存中间结果
save_intermediate = True
```

## 📚 脚本说明

### 核心脚本
- `pdf_to_long_image.py`：基础转换脚本
- `pdf_to_long_image_optimized.py`：高质量优化版
- `pdf_to_long_image_fixed.py`：文字完整修复版
- `create_social_media_version.py`：社交媒体优化

### 示例代码
- `examples/example_usage.py`：使用示例

## 🏆 从实践中学到的

### 重要经验
1. **保守裁剪**：宁可多留空白，不可裁掉内容
2. **平台差异**：不同平台有不同格式要求
3. **验证必要**：转换后必须检查关键内容
4. **参数调优**：根据文档类型调整参数

### 技术要点
- PDF文字层可能独立，需要特殊处理
- 空白检测阈值需要根据文档调整
- 内存管理对大文件很重要
- 多格式输出满足不同需求

## 🤝 贡献与反馈

欢迎提交问题、建议或代码贡献！

1. 报告问题时请提供：
   - PDF文件信息
   - 错误信息
   - 使用的参数
   - 期望的输出

2. 贡献代码：
   - Fork项目
   - 创建功能分支
   - 提交Pull Request

## 📄 许可证

MIT License

## 📞 支持

如有问题，请查看：
- [SKILL.md](SKILL.md)：详细技能文档
- [examples/](examples/)：使用示例
- 或提交Issue

---

**创建时间**：2026年4月3日  
**最后更新**：2026年4月3日  
**版本**：1.0.0  
**创建者**：小美 🎨  

*让每一份文档都能完美呈现* ✨