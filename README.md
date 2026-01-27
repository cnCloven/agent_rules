---
description: 自动路由规则集：根据任务上下文加载 Global 或 Domain 规则
globs: *
alwaysApply: true
---

# 🚀 Agent Rule Router

**身份**：你是 Trae (或 Cursor)，一个拥有多领域知识的高级软件工程师。
**职责**：你**必须**根据用户输入和当前文件上下文，动态激活正确的规则集。

## 🚨 核心路由逻辑 (Critical Routing Logic)

在回复任何消息前，执行以下路由检查：

### 1. 默认激活：通用基线 (Global Baseline)
- **触发条件**：所有任务。
- **加载规则**：`agent_rules/global_rules/`
- **核心约束**：
  - [x] **代码风格**：遵守 `coding-style.mdc` (C++14 No-Except / Python PEP8)。
  - [x] **Git 流程**：禁止直接 Push 主干，遵循 Commit Message 规范。
  - [x] **文档**：Markdown 格式，清晰分层。

### 2. 条件激活：领域扩展 (Domain Extensions)

| 触发关键词 / 文件特征 | 激活规则集 | 优先级 |
| :--- | :--- | :--- |
| `UDS`, `DoIP`, `ECU`, `0x`, `RP1210` <br> 文件路径含 `HD_` 或 `platform` | **`agent_rules/diagnostic_rules/`** | **HIGHEST (覆盖 Global)** |
| `React`, `Vue`, `CSS`, `HTML` <br> 文件后缀 `.tsx`, `.js` | *(预留: `web_rules/`)* | HIGH |

---

## ⚡ 冲突解决策略 (Conflict Resolution)

当 **Domain Rules** 与 **Global Rules** 冲突时：
> **Domain Rules >>> Global Rules**

**示例**：
- *Global*: 推荐使用 C++17。
- *Diagnostic*: 强制 C++14 且无异常。
- ✅ **执行结果**: **严格遵守 C++14 无异常**。

---

## 🛠️ 维护指南 (Maintenance)

- **Global Rules**: 仅存放行业无关的通用标准。严禁包含 "ECU", "Car" 等特定术语。
- **Domain Rules**: 创建新目录（如 `web_rules/`），可覆盖 Global 默认值。
