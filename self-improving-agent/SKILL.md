# Self-Improvement Agent Skill

Description: Logs learnings, errors, and corrections to OpenClaw workspace memory for continuous improvement. When using this skill, you create entries in the .learnings directory under your OpenClaw workspace to record learnings and improvements.

OpenClaw integration: This skill is designed to work across sessions and agents, sharing learnings via sessions_send, and promoting broadly applicable learnings to project memory.

### Quick Reference
- **Situation:** Command/operation fails
  **Action:** Log to .learnings/ERRORS.md with timestamp, input, error details, and environment
- **Situation:** User corrections or feedback
  **Action:** Log to .learnings/LEARNINGS.md with category "correction" and description
- **Situation:** Requested feature
  **Action:** Log to .learnings/FEATURE_REQUESTS.md
- **Promotion:** When learning is widely applicable, promote to CLAUDE.md, AGENTS.md, or COPILOT settings.

### Workspace setup
- Logs directory: ~/.openclaw/workspace/.learnings
- Leverage assets LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md

### Example Entry
## [LRN-YYYYMMDD-XXX] example

**Logged**: 2026-03-27T12:34:56Z
**Priority**: medium
**Status**: pending
**Area**: config | process | UI

### Summary
Brief description of the learning.

### Details
Full context, what happened, what was learned, and next steps.

### Suggested Action
Concrete improvement.

### Metadata
- Source: conversation
- Tags: example, testing
- Pattern-Key: (optional)

---

"} , 