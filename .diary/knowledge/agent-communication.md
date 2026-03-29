# Agent间通信规范

> 创建时间：2026-03-28
> 过期时间：2026-09-28（6个月）

## 核心原则
**"收到即回，再做正事"**

就像人类工作场合的沟通礼仪：收到消息后先确认，让对方安心，然后再去执行。

## 发送方规范

### 消息格式
```
【来自XX - 角色】

[具体内容]

收到请回复～ [emoji]
```

### 技术实现
```javascript
await sessions_send({
  sessionKey: "agent:xxx:telegram:direct:8726379476",
  message: "小X好！我是小Y。\n\n[具体内容]\n\n收到请回复～",
  timeoutSeconds: 20  // 必须设置20秒超时
});
```

### 要求
- `timeoutSeconds: 20` — 给接收方足够响应时间
- 消息结尾加"收到请回复～"明确提醒
- 超时后重发一次，仍失败则通知上级

## 接收方规范

### 确认回复格式
```
收到！谢谢小Y提醒～ [emoji]
我这就去处理！
```

### 禁止行为
- ❌ 先干活，干完再回复
- ❌ 已读不回
- ❌ 延迟回复超过10秒

## 超时处理流程
```
发送消息 → 等待20秒
    ↓
收到回复？→ 是 → 完成
    ↓ 否
重发一次 → 等待20秒
    ↓
收到回复？→ 是 → 完成
    ↓ 否
通知Jarvis → 记录日志
```

## Session Key 映射表
| Agent | 名称 | Session Key |
|-------|------|-------------|
| main | Jarvis | `agent:main:telegram:direct:8726379476` |
| chief-editor | 小策 | `agent:chief-editor:telegram:direct:8726379476` |
| writer | 小科 | `agent:writer:telegram:direct:8726379476` |
| arteditor | 小美 | `agent:arteditor:telegram:direct:8726379476` |
| infocollecter | 小信 | `agent:infocollecter:telegram:direct:8726379476` |
| legal | 小法 | `agent:legal:feishu:direct:ou_efe6cdf735c0373e769c99746e9e85d1` |

## 相关文件
- `AGENTS.md` - 完整规范文档
- `.diary/logs/2026-03/2026-03-28-agent-communication-fix.md` - 问题解决记录