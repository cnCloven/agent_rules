## 1. 目的与适用范围

本文件定义开发时的**代码风格与错误处理规范**，以便：

- 统一 C++14 代码风格（重点）；
- 辅助规范项目中可能使用到的 Python / TypeScript / Rust 脚本代码；
- 降低维护成本、提高可读性。

文中使用约定术语：**MUST（必须）/ MUST NOT（禁止）/ SHOULD（应该）/ MAY（可选）**。

---

## 2. 通用原则（所有语言）

1. **可读性优先**  
   - 代码写给“未来的维护者”（包括 AI Agent 和人类开发者）。  
   - 宁可多几行清晰代码，也不要追求晦涩的“一行流”。

2. **一致性优先于个人喜好**  
   - 一旦在项目内确定格式与命名习惯，即使个人习惯不同也必须遵循。

3. **最小知识原则**  
   - 模块仅暴露必要接口，内部实现细节不泄漏到其他层和模块。

4. **注释关注“为什么”而不是“做什么”**  
   - **代码本身**负责表达“做什么”（what），  
   - **注释**负责解释“为什么这样做”（why）以及“有哪些隐含约束”。

---

## 3. C++14 代码规范（核心）

### 3.1 文件与组织结构

1. **文件命名**
   - 源文件：`lower_snake_case.cpp`
   - 头文件：`lower_snake_case.h`
   - 文件名应体现主要类/模块职责：  
     - 例如：`diagnostic_session_manager.h/.cpp`，`rp1210_loader.h/.cpp`。

2. **每个文件的内容**
   - 一个文件 **MUST** 只包含一个主要类/模块，且名称与文件名一致或高度相关。
   - 头文件 **MUST NOT** 包含实现细节（如大段函数实现、匿名命名空间逻辑）。

3. **包含顺序**
   ```cpp
   #include "this_module.h"          // 对应头文件（若存在）
   #include "project_other_header.h" // 本项目其他头文件
   #include "platform/inc/..."       // platform 相关头文件
   #include <...>                    // 标准库头文件
   ```
   - 禁止使用相对路径穿越上级目录（如 `../platform/inc`），统一由构建系统控制 include path。

4. **头文件保护**
   - 使用 `#pragma once` 或传统 include guard，二选一，项目内必须统一：
     ```cpp
     #pragma once
     ```

### 3.2 命名约定

1. **总体规则**

| 元素          | 风格             | 示例                                  | 备注                    |
| :---------- | :------------- | :---------------------------------- | :-------------------- |
| **类/结构体**   | PascalCase     | `DiagnosticSession`, `EcuConfig`    | 名词或名词短语               |
| **函数/方法**   | PascalCase     | `StartRoutine`, `ReadData`          | 动词开头，区分于 stl/boost 风格 |
| **变量 (局部)** | camelCase      | `retryCount`, `bufferIndex`         |                       |
| **变量 (成员)** | m_ + camelCase | `m_timeoutMs`, `m_isConnected`      | 明确成员作用域               |
| **常量/枚举值**  | kPascalCase    | `kMaxRetryTimes`, `kDefaultSession` | Google 风格，避免全大写宏冲突    |
| **命名空间**    | PascalCase     | `BeiqiLogic`, `UdsProtocol`         | 避免全局污染                |
| **接口类**     | I + PascalCase | `IDiagTransport`, `ILogger`         | 纯虚基类                  |
| 宏           | PASCAL_CASE    | UPPER_SNAKE_CASE                    | 纯大写，少用                |

1. **示例**
   ```cpp
   class DiagnosticSessionManager {
   public:
       bool StartSession();
       bool StopSession();

   private:
       uint32_t m_currentSessionId;
       static constexpr uint32_t kDefaultSessionId = 0x01;
   };

   class IDiagTransport {
   public:
       virtual ~IDiagTransport() = default;
       virtual Result<void> Send(const ByteBuffer& data) = 0;
   };
   ```

2. **命名语义要求**
   - 名称 **MUST** 体现业务含义，不使用 `tmp`, `data1`, `flag2` 等模糊命名。
   - 布尔变量使用肯定语气：`isConnected`, `hasPendingRequest`。

### 3.3 格式与排版

1. **缩进与空格**
   - 缩进：**4 空格**，禁止使用制表符（Tab）。
   - 控制语句与括号之间留空格：
     ```cpp
     if (condition) {
         // ...
     }
     ```
   - 二元运算符两侧加空格：`a + b`, `x == y`。

2. **大括号风格**
   - 函数与控制结构均采用 K&R 风格：
     ```cpp
     void foo() {
         if (condition) {
             doSomething();
         } else {
             doSomethingElse();
         }
     }
     ```

3. **行长度**
   - 单行长度 **SHOULD NOT** 超过 120 字符；过长时应合理换行。

4. **`using namespace` 规则**
   - 头文件中 **MUST NOT** 使用 `using namespace ...;`。
   - 源文件中也 **SHOULD AVOID** 使用，推荐显式 `std::` 前缀。

### 3.4 注释与文档

1. **单行注释**
   - 使用 `//`，注释内容保持简洁，紧贴所注释代码行：
     ```cpp
     // Start default diagnostic session before any operation.
     Result<void> DiagnosticSessionManager::startDefaultSession() { ... }
     ```

2. **块注释**
   - 用于说明复杂算法或状态机：
     ```cpp
     /*
      * State machine for UDS 0x27 SecurityAccess:
      *   1. RequestSeed
      *   2. ComputeKey
      *   3. SendKey
      *   4. Handle NRC or success
      */
     ```

3. **接口文档（建议采用 Doxygen 风格）**
   ```cpp
   /// Start a diagnostic session with given type.
   /// @param sessionType UDS session type as defined in ISO 14229.
   /// @return Result<void> indicating success or error code.
   Result<void> startSession(UdsSessionType sessionType);
   ```

4. **禁止事项**
   - 禁止写无意义注释，如 `// increment i`。
   - 禁止注释大块废弃代码，若代码废弃应删除或移入版本控制历史。

### 3.5 错误处理机制（无异常环境）

> 受限于平台约束，C++ 代码 **MUST NOT** 使用异常。

1. **禁止**
   - 禁止使用：
     ```cpp
     try { ... } catch (...) { ... }
     throw SomeError();
     ```
   - 若外部库内部抛异常，应在调用边界用库自带机制转化为返回值或错误码，不能在本项目内部传播异常。

2. **统一错误返回模式**
   - 推荐使用统一 `Result<T>` 或状态码 + 输出参数模式：
     ```cpp
     enum class ErrorCode {
         Ok,
         Timeout,
         InvalidParameter,
         TransportError,
         InternalError,
         // ...
     };

     template <typename T>
     struct Result {
         T value;
         ErrorCode error;
         bool isOk() const { return error == ErrorCode::Ok; }
     };
     ```
   - 函数 **MUST** 明确说明失败条件与返回的 `ErrorCode`。

3. **错误检查**
   - 凡是返回 `ErrorCode` / `Result` 的函数调用，**MUST** 进行检查，禁止无视返回值：
     ```cpp
     auto result = transport->send(request);
     if (!result.isOk()) {
         logError(result.error);
         return result.error;
     }
     ```

4. **资源安全与 RAII**
   - 必须优先使用 RAII 管理资源：
     - `std::unique_ptr` 管理动态内存；
     - 自定义 RAII 类型管理句柄、文件描述符等。
   - 析构函数 **MUST NOT** 抛异常。

### 3.6 内存与性能

1. **内存管理**
   - 禁止裸 `new/delete` 作为长期持有的对象管理方式，优先使用：
     - 栈对象；
     - `std::unique_ptr<T>`；
     - 容器 `std::vector<T>` / `std::array<T, N>`。
   - 对外暴露接口时，尽量采用值语义或智能指针，避免转移所有权模糊。

2. **`auto` 使用**
   - 对明显类型（如基本类型、简单容器迭代）可使用 `auto` 提高可读性。
   - 对复杂模板类型，使用 `auto` 前确保右值表达式语义清晰，避免隐藏关键类型信息。

### 3.7 并发与多线程

1. **线程创建**
   - 推荐使用 `std::thread`、`std::mutex`、`std::lock_guard`。
   - 不允许在业务代码中直接使用系统级线程 API（如 `CreateThread`、`pthread_create`），统一通过 C++ 标准库或 `platform` 线程封装。

2. **共享数据**
   - 共享可变数据必须用互斥锁保护；  
   - 尽量使用不可变数据结构或线程间消息队列，减少共享状态。

---

## 4. Python 代码规范（工具 / 脚本）

仅适用于项目内可能存在的自动生成脚本、数据预处理工具等。

1. **风格基线**
   - 遵循 **PEP 8**。
   - 缩进：4 空格。
   - 文件编码：UTF-8。

2. **命名**
   - 模块名 / 函数 / 变量：`snake_case`
   - 类名：`PascalCase`
   - 常量：`UPPER_SNAKE_CASE`

3. **异常处理**
   - 使用 Python 标准异常机制；
   - 在脚本入口处捕获顶层异常并友好输出错误信息，而不是让脚本直接崩溃打印追踪栈给终端用户。

---

## 5. TypeScript 代码规范（前端 / 工具）

若存在前端辅助工具或可视化脚本，遵循以下规范：

1. **风格基线**
   - 使用 ESLint + Prettier（或等效规则）；
   - 缩进：2 空格；
   - 强制使用分号。

2. **命名**
   - 变量 / 函数：`camelCase`
   - 类型 / 接口 / 类：`PascalCase`
   - 枚举：`PascalCase`，枚举成员 `PascalCase` 或 `UPPER_SNAKE_CASE`（项目统一）。

3. **类型要求**
   - 所有导出函数与公共 API **MUST** 显式标注类型；
   - 禁止使用 `any` 作为通用逃生口（可通过 `unknown` + 明确类型缩小替代）。

---

## 6. Rust 代码规范（若有工具使用）

Rust 主要用于高可靠工具链场景（例如数据生成工具），不用于车系业务逻辑主代码路径。

1. **风格基线**
   - 必须使用 `rustfmt` 自动格式化；
   - 建议开启 `clippy` 静态检查。

2. **命名**
   - 模块 / 函数 / 变量：`snake_case`
   - 类型 / 枚举 / Trait：`CamelCase`
   - 常量：`UPPER_SNAKE_CASE`

3. **错误处理**
   - 使用 `Result<T, E>` + `?` 运算符；
   - 顶层入口（如 `main`）需要统一错误打印并合理退出码。

---

## 7. 禁止及高风险做法清单

1. C++ 中使用 `try/catch/throw`（**禁止**）。
2. 在头文件中使用 `using namespace std;`（**禁止**）。
3. 大量使用宏替代常量和内联函数（**不推荐**，除非必要）。
4. 将业务逻辑散落在 UI 回调中（**禁止**，破坏架构）。
5. 忽略任何错误返回值（**禁止**）。
6. 通过全局变量传递关键业务状态（**不推荐**，应封装为类成员或上下文对象）。

---

本规范是对架构原则与技术栈约束的**具体落地**：  
在编写任何新代码或修改既有代码前，AI Agent 应先对照本文件进行自检，确保风格与错误处理方式满足项目整体要求。
