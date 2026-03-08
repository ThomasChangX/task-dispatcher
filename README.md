# Task Dispatcher

智能任务分发与子代理协调中枢 - OpenClaw Skill

## 简介

Task Dispatcher 是一个用于 OpenClaw 框架的智能任务分发 skill。它能够分析用户需求、智能拆解任务、自动选择合适的 Agent 执行，并提供完善的风险管理和审核机制。

## 功能特性

- 🎯 **智能任务分析** - 自动分析任务目标、约束条件、复杂度
- 🔄 **自动任务拆解** - 将复杂任务拆分为可执行的子任务
- 👥 **多 Agent 协作** - 支持 10 种专业 Agent（architect, coder, critic, devops, docs_writer, researcher, retrospective, reviewer, scheduler, tester）
- 🛡️ **风险管理** - 4 级风险分类（LOW/MEDIUM/HIGH/CRITICAL）
- ✅ **审核机制** - 并行审核、智能汇总、冲突解决
- 🔁 **防死循环** - 成本/时间/进度三保险机制
- 🧹 **自动清理** - 任务完成后自动清理临时文件

## 依赖

- **OpenClaw** 框架
- **MiniMax M2.5** 或其他大语言模型

## 快速开始

1. 安装 OpenClaw 框架
2. 将此 skill 复制到 OpenClaw 的 skills 目录
3. 在任务中使用 task-dispatcher skill

## 目录结构

```
task-dispatcher/
├── SKILL.md                   # 核心 skill 定义
├── LICENSE                    # MIT 许可证
├── README.md                  # 项目说明
└── references/
    ├── SUPPLEMENTARY_DESIGN.md  # 补充设计文档
    └── config/                  # 配置参考
        ├── agents.yaml
        ├── pipelines.yaml
        ├── review.yaml
        ├── cleanup.yaml
        └── budget.yaml
```

## 工作流程

1. **需求分析** - 分析任务目标、约束、复杂度
2. **任务拆解** - 生成结构化任务列表
3. **确认执行** - 展示计划并等待确认
4. **分发执行** - 自动选择 Agent 并分发任务
5. **进度监控** - 实时监控任务状态
6. **阶段汇报** - 关键节点向用户汇报
7. **清理处理** - 自动清理临时文件

## 配置

阈值配置（可在 SKILL.md 中调整）：

```yaml
max_token: 80000        # 最大 token 消耗
max_time_minutes: 30   # 超时时间
max_retries: 2         # 最大重试次数
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者

Thomas Chang
