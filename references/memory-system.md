# 记忆系统维护规范

## 概述

本 skill 使用三层记忆系统，确保任务上下文在会话和会话之间正确传递。

| 层级 | 文件 | 用途 | 生命周期 |
|------|------|------|----------|
| 状态 | SESSION-STATE.md | 当前任务状态 | 当前会话 |
| 短期 | memory/YYYY-MM-DD.md | 当天工作日志 | 30 天 |
| 长期 | MEMORY.md | 重要经验沉淀 | 永久 |

---

## SESSION-STATE.md - 当前会话状态

### 存放位置
`~/.openclaw/workspace/SESSION-STATE.md`

### 创建时机
每次开始新任务时

### 内容结构

```markdown
# Session State - {日期}

## Current Task
- **Task**: [任务描述]
- **Started**: [ISO 时间]
- **Status**: In Progress | Completed | Failed | Blocked
- **Progress**: [0-100%]

## Task Breakdown
- [ ] Step 1: xxx
- [ ] Step 2: xxx
- [ ] Step 3: xxx

## Critical Context
- [关键信息 - 上下文丢失后需要恢复的内容]

## Recent History
- [最后 3-5 个关键动作]

## Next Steps
- [ ] 立即要做的事情
- [ ] 待用户确认的事情

## Blocker
- [如有阻塞项]
```

### 状态流转

```
Created → In Progress → (Completed | Failed | Blocked)
```

### 更新时机

| 事件 | 更新内容 |
|------|----------|
| 开始新任务 | 初始化全部字段 |
| 阶段完成 | 更新 Progress、Recent History |
| 遇到问题 | 更新 Status 为 Blocked，填写 Blocker |
| 任务完成 | 更新 Status 为 Completed |

---

## memory/YYYY-MM-DD.md - 每日工作日志

### 存放位置
`~/.openclaw/workspace/memory/YYYY-MM-DD.md`

### 创建时机
首次写入当天日志时自动创建

### 内容结构

```markdown
# {日期} 工作日志

## 完成任务
- [时间] 任务A - 结果
- [时间] 任务B - 结果

## 进行中任务
- 任务C (进度: 50%)
- 任务D (进度: 30%)

## 经验记录
- [如有新经验]

## 待处理
- [待处理事项]
```

### 写入时机

| 时机 | 写入内容 |
|------|----------|
| 任务开始 | 任务描述和目标 |
| 任务完成 | 完成结果和产出 |
| 关键进展 | 重要里程碑 |
| 经验教训 | 值得记录的心得 |

### 保留策略
保留最近 30 天的日志，之后可归档或清理

---

## MEMORY.md - 长期经验沉淀

### 存放位置
`~/.openclaw/workspace/MEMORY.md`

### 加载规则

| 会话类型 | 是否加载 |
|----------|----------|
| 主会话 (webchat) | ✅ 加载 |
| 共享上下文 | ❌ 不加载 |
| 群聊 | ❌ 不加载 |

### 内容结构

```markdown
# 长期记忆

## 核心原则
- [经过验证的核心原则]

## 常用模式
- [常见任务的处理模式]

## 用户偏好
- [啸天的偏好和习惯]

## 技术经验
- [技术相关的重要经验]

## 协作经验
- [与 agent 协作的经验]
```

### 更新时机

| 场景 | 更新内容 |
|------|----------|
| 完成重要任务 | 提取经验教训 |
| 发现新模式 | 记录有效方法 |
| 用户纠正 | 记录正确做法 |
| 知识更新 | 修正过时信息 |

### 维护原则

1. **定期回顾**：每周 review 一次
2. **提炼精华**：只记录最有价值的内容
3. **及时更新**：新经验立即记录
4. **保持准确**：过时内容及时清理

---

## 任务与记忆的联动

### 任务开始

```
1. 读取 SESSION-STATE.md（如有）
2. 读取 memory/今日.md
3. 读取 MEMORY.md（如在主会话）
4. 创建/更新 SESSION-STATE.md
5. 记录到 memory/今日.md
```

### 任务进行中

```
1. 每次阶段完成后更新 SESSION-STATE.md
2. 关键进展记录到 memory/今日.md
3. 遇到问题记录到 SESSION-STATE.md Blocker
```

### 任务完成

```
1. 更新 SESSION-STATE.md 为 Completed
2. 记录到 memory/今日.md 完成情况
3. 如有重要经验，提取到 MEMORY.md
4. 汇总结果向用户汇报
```

---

## 上下文传递规范

确保 sub-agent 获得足够上下文：

| 内容 | 必须传递 | 传递方式 |
|------|----------|----------|
| 任务目标 | ✅ | prompt 开头 |
| 已完成步骤 | ✅ | prompt Recent History |
| 当前状态 | ✅ | SESSION-STATE.md |
| 约束条件 | ✅ | prompt 明确列出 |
| 关键上下文 | ✅ | Critical Context |

---

## 与 AGENTS.md 的一致性

本记忆系统与 AGENTS.md 中的 Memory System 保持一致：

> ### 短期记忆（Daily Notes）
> - **Daily notes:** `memory/YYYY-MM-DD.md`
> - **Text > Brain** — 如果想记住什么，写到文件里

> ### 长期记忆（MEMORY.md）
> - **ONLY load in main session**
> - 记录重要事件、想法、决定、经验教训

> ### SESSION-STATE.md - 状态持久化
> - 记录当前任务状态、进度、关键上下文
