---
description: 规则索引：说明文件头如何加载，列出各规则的实际生效条件
alwaysApply: true
---

# 规则索引

这个 IDE 只读每个规则文件头顶上几行开关，不会去加载一个目录。像编译器先看 `#pragma once`。

## 何时给到对话里

- **每轮都给**：索引（本文件）、基线总纲。
- **打开这类文件才给**：见下表。
- **题目相关才给**：工作流、协作。

每轮都给的文件，头里不要再写「打开哪些文件才给」。两套写在一起，后一套无效。

领域规则覆盖基线规则。同一条约束只应出现在一层。

## 每轮都给

| 文件 | 作用 |
| :--- | :--- |
| `README.md`（本文件） | 索引 |
| `global_rules/00_global_instruction.md` | 基线总纲与优先级 |

## 打开这类文件才给

**基线**

| 文件 | 何时给 |
| :--- | :--- |
| `global_rules/coding-style.mdc` | `*.h / *.hpp / *.c / *.cpp / *.cc / *.py` |
| `global_rules/testing_standards.md` | 测试目录、`*_test.*`、`*Test.*` |
| `global_rules/documentation_standards.md` | `doc/**/*.md` |

**诊断（打开 `HD_*` 或 `platform` 下的文件时）**

| 文件 | 何时给 |
| :--- | :--- |
| `diagnostic_rules/00_diagnostic_instruction.mdc` | `HD_*/**/*`、`platform/**/*` |
| `diagnostic_rules/architecture.mdc` | 同上 |
| `diagnostic_rules/domain_standards.mdc` | 上述目录中的 `*.h / *.cpp` 等源码 |
| `diagnostic_rules/tech_stack.mdc` | 同上 |
| `diagnostic_rules/platform_interface_constraints.mdc` | 同上 |
| `diagnostic_rules/testing_specifics.mdc` | 测试目录 |
| `diagnostic_rules/reverse_engineering.mdc` | `reverse_engineering/**/*`、`*.idb`、`*.exe` |
| `diagnostic_rules/documentation_specifics.mdc` | `HD_*/doc/**/*`、`HD_*/**/*.md` |

**题目相关才给**

| 文件 | 何时给 |
| :--- | :--- |
| `global_rules/workflow.md` | 分支、提交、CI、发布相关问题 |
| `global_rules/collaboration.md` | 计划、拆任务、协作文档 |

平台短约束见 `diagnostic_rules/platform_interface_constraints.mdc`。完整手册在 `diagnostic_rules/platform_interface_constraints/`，没有文件头，需要时再打开。

## 改规则时怎么写文件头

开关写在文件头顶上，不要写进正文当主语。

- 每轮都给：`alwaysApply: true`，不要写 `globs`
- 打开匹配的文件才给：`alwaysApply: false`，并写 `globs`
- 题目相关才给：`alwaysApply: false`，不写 `globs`

## 维护

- **基线规则**：只放行业无关的通用标准。
- **领域规则**：新建目录（如 `web_rules/`）覆盖基线。不要把领域文件标成每轮都给。
