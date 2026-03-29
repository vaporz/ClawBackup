# Obsidian 阅读优化配置

> 记录时间：2026-03-28
> 用途：打造舒适的Markdown阅读环境

---

## 安装清单

| 项目 | 说明 |
|------|------|
| **主题** | Primary |
| **字体** | LXGW WenKai（霞鹜文楷）|
| **插件** | Style Settings |
| **插件** | Export Image |

---

## CSS 片段配置

保存到 `.obsidian/snippets/reading-optimized.css`：

```css
/* 1. 设置柔和的背景色和文字颜色 */
.theme-light {
  --background-primary: #f5f2e9 !important;
  --background-secondary: #ede9dc !important;
  --text-normal: #3c3c3c !important;
  --text-muted: #767676 !important;
}

/* 2. 优化正文排版 - 使用更高优先级的选择器 */
body .markdown-source-view.mod-cm6 .cm-content,
body .markdown-rendered,
body .markdown-preview-view,
body .view-content .markdown-source-view .cm-content {
  font-family: "LXGW WenKai", "霞鹜文楷", "PingFang SC", "Microsoft YaHei", sans-serif !important;
  font-size: 18px !important;
  line-height: 1.85 !important;
  letter-spacing: 0.03em !important;
  max-width: 750px !important;
  margin: 0 auto !important;
}

/* 编辑模式也强制应用 */
body .cm-editor .cm-content {
  font-family: "LXGW WenKai", "霞鹜文楷", "PingFang SC", "Microsoft YaHei", sans-serif !important;
}

/* 3. 隐藏行号 */
.cm-lineNumbers, .cm-gutter {
  display: none !important;
}

/* 4. 标题样式 */
body h1, body h2, body h3,
.markdown-rendered h1, .markdown-rendered h2, .markdown-rendered h3 {
  color: #5a4a42 !important;
  font-family: "LXGW WenKai", "霞鹜文楷", "PingFang SC", sans-serif !important;
  font-weight: 500 !important;
}
```

---

## 效果特点

- 🎨 **柔和背景**：米黄色护眼背景 `#f5f2e9`
- ✍️ **优雅字体**：霞鹜文楷，中文阅读体验极佳
- 📏 **舒适排版**：18px字号，1.85行高，750px最大宽度
- 🧹 **简洁界面**：隐藏行号，专注内容
- 🎯 **统一风格**：标题、正文风格一致

---

## 使用场景

- 阅读 `.md` 文档
- 查看工作笔记
- 审阅文档内容
- 导出为图片分享

---

*效果评价：非常好！* ⭐⭐⭐⭐⭐
