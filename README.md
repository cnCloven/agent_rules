# AI Agent 规则库 (Rule Repository)

本仓库存储了 AI Agent 在开发过程中必须遵循的规则与规范。
规则体系分为两层：**通用层 (Global)** 与 **特定领域层 (Domain Specific)**。

## 1. 目录结构

```text
root/
├── global_rules/        # 通用软件开发规则（行业无关）
│   ├── 00_global_instruction.md  # [入口] 通用规则总纲
│   ├── coding_style.md
│   ├── workflow.md
│   ├── ...
│
└── diagnostic_rules/    # 汽车诊断行业特定规则（High Priority）
    ├── 00_diagnostic_instruction.md  # [入口] 诊断规则总纲与角色定义
    ├── architecture.md
    ├── domain_standards.md
    ├── ...
```

## 2. 规则加载与应用顺序 (Loading Order)

Agent 在启动或执行任务时，必须严格按照以下顺序解析规则：

1.  **第一阶段：加载 `global_rules`**
    *   建立软件工程的基础基线（如代码可读性、Git 流程、文档结构）。
    *   **注意**：此时 Agent 不应假设任何特定角色，保持通用工程师身份。

2.  **第二阶段：加载 `diagnostic_rules`**
    *   加载特定领域的约束（如 UDS 协议、无异常 C++、RP1210 架构）。
    *   **角色激活**：此时 Agent 正式激活“汽车诊断架构师”角色。

## 3. 优先级与冲突解决 (Priority)

当 `diagnostic_rules` 中的规则与 `global_rules` 发生冲突时：

> **`diagnostic_rules` >>> `global_rules`**

*   **特定领域规则具有最高优先级**。
*   **示例**：
    *   Global: "推荐使用 C++17 或更新标准"
    *   Diagnostic: "必须使用 C++14，且禁止异常"
    *   **结果**：执行 C++14 且无异常标准。

## 4. 维护指南

*   **新增通用规则**：放入 `global_rules`，确保不包含任何 "Car", "ECU", "UDS" 等特定术语。
*   **新增业务规则**：放入 `diagnostic_rules`，可以覆盖 Global 中的默认设定。
