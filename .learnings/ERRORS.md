# ERRORS.md

Command failures, exceptions, and unexpected errors go here.

## Usage

Append entries using this format:

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description

### Error
```
Actual error message
```

### Context
- Command attempted
- Parameters used
- Environment details

### Suggested Fix
If identifiable

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext

---
```

---

*Auto-created for self-improvement skill*

---

## [ERR-20260326-001] volc-vision image recognition

**Logged**: 2026-03-26T12:46:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
使用 volc-vision API 识别图片时遇到认证错误

### Error
```
Invalid credential in 'Authorization'
```

### Context
- 尝试调用 `https://visual.volcengineapi.com/v1/visual/recognition`
- 使用 HMAC-SHA256 签名
- AK/SK 来自 ~/.bashrc

### Suggested Fix
- 已解决！使用火山引擎的视觉模型 `doubao-1-5-vision-pro-32k-250115`（注意是横杠 `-` 不是点 `.`）
- 不需要 volc-vision API，直接用 Ark 的 chat completion 接口即可

### Metadata
- Reproducible: yes
- Related Files: ~/.openclaw/skills/image-recognition/
- **Resolved**: 2026-03-26T12:54:00Z

---

*Auto-created for self-improvement skill*