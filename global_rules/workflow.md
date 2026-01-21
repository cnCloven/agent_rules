## 1. 文档目标与适用范围

本文件定义开发的**项目工作流与协作规范**，包括：
- Git 仓库与分支策略；
- 提交流程与 Code Review 标准；
- CI/CD 流水线基本要求；
- 版本号与发布规范。

AI Agent 在输出与“流程、协作相关”的建议、脚本或文档时，**必须默认遵守本规范**。

---

## 2. Git 分支策略 (Branching Strategy)

### 2.1 仓库结构

- 建议整体采用**单一仓库（monorepo）或多模块仓库**。
- AI Agent 在涉及 Git 操作/建议时，只针对业务逻辑相关内容。

采用简化版 **Git Flow**，适应快速迭代与多版本维护需求。

### 2.2 分支定义
采用**简化 GitFlow**，适合约 10 人规模团队。

必备分支：

- `main`  
  - 永远代表**已发布/可发布**的稳定版本。
- `develop`  
  - 日常开发主干，集成已通过初步验证的功能。

临时分支（短生命周期）：

- 功能分支：`feature/<short-name>`  
  - 用于新功能开发或重构；
  - 从 `develop` 拉出，完成后合并回 `develop`。
- 修复分支：`bugfix/<issue-id>`  
  - 用于修复尚未发布的缺陷；
  - 从 `develop` 拉出，合并回 `develop`。
- 发布分支：`release/<version>`  
  - 从 `develop` 拉出，用于版本冻结、回归测试与缺陷修复；
  - 测试完成后合并到 `main` 和 `develop`。
- 热修分支：`hotfix/<version>`  
  - 从 `main` 拉出，用于紧急修复线上版本缺陷；
  - 修复完成后合并到 `main` 和 `develop`。

### 2.3 分支命名规则

- 仅使用小写字母、数字与短横线 `-`：
  - `feature/dtc-service-improvement`
  - `bugfix/1234-timeout-handling`
  - `release/1.3.0`
  - `hotfix/1.3.1`

### 2.4 工作流规则
1.  **禁止直接提交**：`main` 和 `develop` 分支受保护，**禁止直接 Push**，必须通过 Pull Request (PR) / Merge Request (MR) 合并。
2.  **分支同步**：
    - 开始新功能前，必须从 `develop` 拉取最新代码。
    - 提交 PR 前，必须先 Rebase `develop`，解决本地冲突，保持提交历史整洁。

---

## 3. 提交流程与提交信息

### 3.1 提交流程要求

1. **本地自检（必需）**
   - 本地构建通过；
   - 关键单元测试/集成测试通过（如存在）；
   - 自我代码检查：风格、架构、无异常。

2. **小步提交**
   - 每次提交尽量聚焦单一变更（例如一个功能点、一类重构或一个缺陷修复）。

### 3.2 Commit Message 规范

建议格式：

```text
<type>: <short summary>

[optional body explaining what/why]
[optional footer: issue references]
```

- `<type>` 取值示例：
  - `feat`：新增功能
  - `fix`：缺陷修复
  - `refactor`：重构（无功能变化）
  - `docs`：文档变更
  - `test`：测试相关变更
- 示例：
  - `feat: add basic DTC read/clear service`
  - `fix: handle 0x78 pending NRC in security access flow`

---

## 4. Code Review 标准

### 4.1 何时需要 Review

- 合并到 `develop`、`release/*`、`main` 的所有变更 **必须** 经过 Code Review。
- 小型实验性分支可以自测，但合入主干前仍需要 Review。

### 4.2 审查人要求

- 至少 1 名具有该模块经验的开发者进行 Review；
- 对安全相关（刷写、编码、安全访问等）变更，建议由资深开发者/架构师复审。

### 4.3 Review 内容 Checklist（AI Agent 输出时需内隐遵守）

**架构与分层**

- [ ] 是否遵守分层架构？
- [ ] 业务逻辑是否避免直接依赖外部细节，而通过适配层接口访问？
- [ ] 差异是否尽可能通过配置，而非硬编码？

**C++ 规范**

- [ ] 是否遵循 C++14，无使用 C++17+ 特性？
- [ ] 无 `try/catch/throw` 异常使用？
- [ ] 错误通过返回值/Result 传递，上层是否有检查？
- [ ] 命名、格式是否符合《Coding Style》？

**安全与健壮性**

- [ ] 外部数据（文件/响应）是否做了边界检查？
- [ ] 是否使用 RAII 管理资源，避免泄露？
- [ ] 是否考虑中断、超时和重试策略？

**测试**

- [ ] 是否为新增/修改的关键逻辑添加或更新了单元测试/集成测试？
- [ ] 测试是否覆盖典型的正常路径与错误路径？

---

## 5. CI/CD 流程

### 5.1 CI（持续集成）基本阶段

典型流水线阶段（工具可为 Jenkins / GitLab CI / GitHub Actions 等）：

1. **Checkout & 环境准备**
   - 拉取代码；
   - 配置编译工具链、CMake、必要 SDK。

2. **构建（Build）**
   - 构建相关目标；
   - 编译时启用尽可能多的警告（例如 `-Wall -Wextra`）并视警告为错误（`-Werror`），如可行。

3. **静态检查（可选但推荐）**
   - 运行 clang-tidy / cppcheck 等工具；
   - 检查典型问题：未使用变量、潜在空指针、越界访问等。

4. **测试执行**
   - 运行自动化测试：
     - 单元测试；
     - 集成/接口测试。
   - 收集测试结果与覆盖率指标。

5. **工件生成**
   - 构建产物（如 DLL/EXE/静态库、数据包）；
   - 将构建结果存入制品仓库（artifact repository），与版本号/提交哈希关联。

### 5.2 Gate 规则

- 合并到 `develop` 或更高分支前，CI **必须** 通过：
  - 编译成功；
  - 关键测试通过。
- 对 `release/*` 分支：
  - 推荐增加更多测试（回归用例、性能测试、兼容性测试）。

### 5.3 CD（持续交付/部署）

- 在 CI 构建产出基础上：
  - 生成带版本号的安装包/压缩包；
  - 附带 release notes（变更说明）。

---

## 6. 版本号与发布规范

### 6.1 版本号策略（建议 SemVer 变体）

采用 `MAJOR.MINOR.PATCH` 形式：

- `MAJOR`：不兼容的接口变更，或重大架构调整；
- `MINOR`：向后兼容的新功能；
- `PATCH`：向后兼容的缺陷修复。

可选扩展标记：

- `MAJOR.MINOR.PATCH-<suffix>`（如 `1.3.0-rc1`）；

### 6.2 Tag 与分支关系

- 每次发布时：
  - 在 `main` 对应提交上打 Git Tag：`vMAJOR.MINOR.PATCH`；
  - 若存在特定变体，可在 tag 注释中说明关键变更。

- `release/<version>` 分支：
  - 用于集成测试与最终修复；
  - 完成后：
    - 合并到 `main`；
    - 打 Tag；
    - 再将变更合并回 `develop`。

### 6.3 发布流程摘要

1. 从 `develop` 创建 `release/x.y.z`；
2. 冻结新功能，只允许修复缺陷和完善文档；
3. 通过完整回归测试；
4. 将 `release/x.y.z` 合并到 `main`；
5. 在 `main` HEAD 打 `vx.y.z` Tag；
6. 将 `release/x.y.z` 合并回 `develop`（避免分支分叉）；
7. 将构建产物与版本说明交付。

---

## 7. 缺陷管理与热修流程

### 7.1 缺陷登记

- 所有缺陷必须在跟踪系统中登记（如 JIRA / Redmine / GitLab Issues）；
- 登记信息包含：
  - 版本号；
  - 场景描述；
  - 重现步骤；
  - 预期结果 / 实际结果；
  - 相关日志与数据。

### 7.2 热修（Hotfix）流程

1. 从 `main` 创建 `hotfix/x.y.z` 分支；
2. 修复缺陷 + 添加/更新对应测试；
3. 走 Code Review + CI 流程；
4. 合并回 `main` 和 `develop`；
5. 在 `main` 打新 Tag（如 `vx.y.(z+1)`），构建与交付新版本。

---

## 8. AI Agent 使用要求

在回答与下列主题相关的问题时，AI Agent 应默认遵守本文件约定：

- 任务拆分与排期建议；
- “如何提交代码/如何开分支” 类问题；
- Code Review 检查点与改进建议；
- CI/CD 脚本示例与流水线设计；
- 版本策略、发布流程与变更记录模板。

如用户明确指定与本规范不同的流程，Agent 应：

- 在不违反上位规则的前提下，优先遵循用户指定；
- 并在内部自检时标记“与默认项目工作流不一致”，但无需强制纠正用户。
