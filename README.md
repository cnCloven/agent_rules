---
description: 规则索引：说明文件头如何加载，列出各规则的实际生效条件
alwaysApply: true
---

# 规则索引

这个 IDE 只读各规则文件头顶上的开关，不会去加载一个目录。

## 开关怎么读

- **常开**（`alwaysApply: true`，不要写 `globs`）：每轮都注入。
- **按后缀打开**（`alwaysApply: false` + `globs`）：打开匹配的文件才注入。
- **按描述调用**（`alwaysApply: false`，不写 `globs`）：题目相关才注入。

常开和按后缀不能写在同一份头里。

## 冲突

领域规则覆盖基线规则。同一条约束只应出现在一层。

## 生效表

**常开**

| 文件 | 作用 |
| :--- | :--- |
| `README.md`（本文件） | 索引 |
| `global_rules/00_global_instruction.md` | 基线总纲与优先级 |

**基线：按后缀或按描述**

| 文件 | 何时注入 |
| :--- | :--- |
| `global_rules/coding-style.mdc` | `*.h / *.hpp / *.c / *.cpp / *.cc / *.py` |
| `global_rules/testing_standards.md` | 测试目录、`*_test.*`、`*Test.*` |
| `global_rules/documentation_standards.md` | `doc/**/*.md` |
| `global_rules/workflow.md` | 分支、提交、CI、发布相关问题 |
| `global_rules/collaboration.md` | 计划、拆任务、协作文档 |

**诊断：按后缀（打开 `HD_*` 或 `platform` 下的文件时）**

| 文件 | 何时注入 |
| :--- | :--- |
| `diagnostic_rules/00_diagnostic_instruction.mdc` | `HD_*/**/*`、`platform/**/*` |
| `diagnostic_rules/architecture.mdc` | 同上 |
| `diagnostic_rules/domain_standards.mdc` | 上述目录中的 `*.h / *.cpp` 等源码 |
| `diagnostic_rules/tech_stack.mdc` | 同上 |
| `diagnostic_rules/testing_specifics.mdc` | 测试目录 |
| `diagnostic_rules/reverse_engineering.mdc` | `reverse_engineering/**/*`、`*.idb`、`*.exe` |
| `diagnostic_rules/documentation_specifics.mdc` | `HD_*/doc/**/*`、`HD_*/**/*.md` |

平台 API 手册在 `diagnostic_rules/platform_interface_constraints/`，无文件头，需要时再打开。

## 维护

- **基线规则**：只放行业无关的通用标准。
- **领域规则**：新建目录（如 `web_rules/`）覆盖基线。不要把领域文件标成常开。
