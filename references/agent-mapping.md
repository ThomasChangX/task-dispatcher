# Agent 映射与任务分发

## Agent 层级结构

```
           ┌─────────────────┐
           │     main        │ ← 管理中枢
           └────────┬────────┘
                    │ 分发
      ┌────────────┼────────────┐
      ▼            ▼            ▼
  ┌───────┐   ┌───────┐   ┌──────────┐
  │执行层  │   │评估层  │   │  支持层   │
  └───────┘   └───────┘   └──────────┘
```

### 层级说明

| 层级 | Agent | 职责 |
|------|-------|------|
| 管理层 | main | 需求分析、任务拆解、结果汇总 |
| 执行层 | coder, researcher, docs_writer, devops, tester | 具体任务执行 |
| 评估层 | reviewer, critic | 质量评估、风险审查 |
| 支持层 | inspector, scheduler, retrospective | 诊断、提醒、复盘 |

---

## 任务类型 → Agent 映射

### 修复类任务

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 诊断 | inspector | 定位问题根因 |
| 执行 | coder | 修复代码 |
| 审查 | critic | 安全/规范检查 |
| 验证 | tester | 功能验证 |
| 评审 | reviewer | 整体质量评估 |
| 文档 | docs_writer | 更新文档 |
| 复盘 | retrospective | 经验总结 |

### 新功能开发

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 调研 | researcher | 技术调研 |
| 执行 | coder | 编写代码 |
| 审查 | reviewer | 代码审查 |
| 验证 | tester | 测试验证 |
| 文档 | docs_writer | 编写文档 |

### 架构设计

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 调研 | researcher | 背景研究 |
| 设计 | architect | 架构设计 |
| 评审 | critic | 方案评审 |
| 评审 | reviewer | 质量评审 |

### 调研任务

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 执行 | researcher | 信息收集 |
| 评估 | reviewer | 报告质量评估 |

### 文档任务

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 执行 | docs_writer | 编写文档 |
| 评审 | reviewer | 质量评估 |

### 部署运维

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 执行 | devops | 部署执行 |
| 验证 | tester | 验证部署 |
| 监控 | devops | 监控检查 |

### 其他/兜底

| 阶段 | Agent 序列 | 说明 |
|------|------------|------|
| 执行 | worker | 通用执行 |

---

## Agent 能力说明

| Agent | 核心能力 | 适用场景 |
|-------|----------|----------|
| **architect** | 系统设计、技术选型、架构评审 | 架构设计任务 |
| **coder** | 编码实现、代码修改、Bug 修复 | 任何代码相关 |
| **critic** | 风险评估、方案评审、代码批评 | 需要评审的场景 |
| **devops** | 部署、运维、监控、CI/CD | 部署运维任务 |
| **docs_writer** | 文档写作、技术说明、教程 | 文档相关 |
| **inspector** | 问题定位、根因分析、日志诊断 | 问题诊断 |
| **researcher** | 信息收集、调研分析、技术研究 | 调研任务 |
| **reviewer** | 代码审查、质量评估、PR 评审 | 质量把关 |
| **scheduler** | 定时任务、Cron 配置 | 定时提醒 |
| **tester** | 测试编写、功能验证、覆盖率 | 测试验证 |
| **retrospective** | 复盘总结、经验提取 | 项目复盘 |
| **worker** | 通用执行、无特定专长 | 兜底选择 |

---

## 分发策略

### 串行分发
任务有明确依赖，必须按顺序执行

```
Task A → Task B → Task C
```

### 并行分发
任务无依赖，可同时执行

```
Task A
Task B  → Result
Task C
```

### 混合分发
部分串行，部分并行

```
Task A → Task B
      ↘ Task C → Task D
```

---

## 选择 Agent 的决策树

```
收到任务
    │
    ▼
判断任务类型
    │
    ├─ 修复 → inspector → coder → critic → tester → reviewer → docs_writer → retrospective
    │
    ├─ 新功能 → researcher → coder → reviewer → tester → docs_writer
    │
    ├─ 架构设计 → architect → critic → reviewer
    │
    ├─ 调研 → researcher
    │
    ├─ 文档 → docs_writer → reviewer
    │
    ├─ 部署 → devops → tester
    │
    └─ 其他 → worker
```

---

## 超时设置

| 任务类型 | 推荐超时 |
|----------|----------|
| 调研/查询 | 300s (5min) |
| 一般任务 | 300s (5min) |
| 复杂任务 | 600s (10min) |
| 超大任务 | 1200s (20min) |

---

## 复用现有 AGENTS.md 的 Agent 列表

本 skill 复用 workspace 的 AGENTS.md 中定义的 agent 列表：

| Agent ID | 用途 |
|----------|------|
| architect | 架构设计 |
| coder | 编码实现 |
| critic | 批评审查 |
| devops | 运维部署 |
| docs_writer | 文档写作 |
| inspector | 诊断分析 |
| researcher | 调研搜索 |
| retrospective | 复盘总结 |
| reviewer | 代码审查 |
| scheduler | 定时任务 |
| tester | 测试验证 |
| worker | 通用执行 |
