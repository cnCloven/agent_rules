# 全局软件开发规则总纲

## 1. 适用范围
本规则集定义了适用于通用软件开发项目的标准与规范，涵盖代码风格、工作流、文档、测试及协作等方面。
本规则集设计为**行业无关**，旨在作为任何软件工程的通用基线。

## 2. 角色定义 (Role Definition)

> **[MANDATORY PLACEHOLDER]**
> 
> 本通用规则集**不定义**具体的 Agent 角色。
> 具体的角色定义（如“资深架构师”、“领域专家”等）**必须**由加载此规则集的特定领域规则（如 `diagnostic_rules`）提供。
> 
> 在未加载特定领域规则前，Agent 应保持中立的“资深软件工程师”人设，仅关注通用软件工程质量。

## 3. 规则应用优先级

在实际项目中，规则的应用顺序如下：

1.  **加载 Global Rules**：作为底层基线。
2.  **加载 Domain Specific Rules**（如 `diagnostic_rules`）：作为上层约束。

**冲突解决原则**：
当特定领域规则（Domain Rules）与本通用规则（Global Rules）发生冲突时，**特定领域规则具有更高优先级**，应覆盖通用规则。

## 4. 规则索引

| 规则文件 | 描述 |
| :--- | :--- |
| `coding_style.md` | 通用代码风格与编程规范 |
| `workflow.md` | Git 工作流与版本控制策略 |
| `documentation_standards.md` | 通用文档编写标准 |
| `testing_standards.md` | 软件测试策略与质量基线 |
| `collaboration.md` | 团队协作与任务管理规范 |
