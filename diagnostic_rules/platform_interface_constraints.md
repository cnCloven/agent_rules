# 平台 (Platform) 接口调用指南

## 1. 指南目标与适用角色

### 1. 角色与职责
*   **定位**：AI Agent 是平台接口的**调用方 (Client)**，而非实现方。
*   **边界**：
    *   **MUST**：关注获取实例、传递参数、处理返回值。
    *   **MUST NOT**：修改、重定义或猜测平台内部逻辑（如内存管理、校验机制）。

---

## 2. 接口调用核心原则

### 2.1 严格遵照契约 (Strict Adherence)
*   **原则**：平台接口是不可变契约，必须严格匹配头文件声明。
*   **约束**：
    *   **禁止修改**：严禁更改函数签名（参数类型、顺序、名称）或返回值类型。
    *   **严格匹配**：调用参数类型必须与声明精确一致，禁止依赖隐式转换。
    *   **返回值处理**：必须接收并处理原始返回值（如 `Result<T>`），禁止忽略错误状态。
*   **后果**：链接错误 (Linker Error) 或 未定义行为 (Undefined Behavior)。

### 2.2 全局资源管理 (Global Resources)
*   **原则**：直接使用平台通过 `extern` 暴露的全局对象，**严禁重定义或遮蔽**。
*   **约束**：
    *   **直接使用**：仅允许调用 `extern` 对象的成员方法或访问成员。
    *   **禁止重定义**：严禁在业务代码中声明同名变量（如 `PlatformObject g_data;`），避免符号冲突 (ODR Violation)。
    *   **命名隔离**：业务对象应置于独立命名空间，防止与平台对象重名。
*   **示例**：
    ```cpp
    // 假设平台声明: extern PlatformConfig g_sysConfig;
    void CheckConfig() {
        if (g_sysConfig.IsDebug()) { ... } // 正确：直接使用
    }
    // 错误：PlatformConfig g_sysConfig; // 链接错误：多重定义
    ```

### 2.5 资源生命周期管理
*   **原则**：
    *   **智能指针**：若接口返回 `std::unique_ptr`，你负责该对象的生命周期（自动管理）。
    *   **裸指针**：若接口返回裸指针（如 `GetDevice()`），你**不拥有**它，**严禁调用 `delete`**。
*   **场景**：创建临时会话、获取全局设备句柄。
*   **调用示例**：
    ```cpp
    {
        // session 是 unique_ptr，作用域结束自动释放
        auto session = factory->CreateSession();
        session->Start();
    } // 自动析构，安全
    
    // device 是观察者指针
    auto* device = deviceManager->GetActiveDevice();
    if (device) {
        device->Reset();
    }
    // 严禁：delete device;
    ```

---

## 3. 基础数据类使用规范 (platform/inc/binary.h)

### 3.1 二进制数据 (CBinary)
*   **文件路径**: `platform/inc/binary.h`
*   **功能**: `unsigned char` 数组的封装，主要用于存储 UDS 命令中的每个字节。
*   **常用接口**:
    *   `CBinary(const char *pBuffer, WORD iLength)`: 构造函数。
    *   `void Append(const char *pBuffer, WORD iLength)`: 追加数据。
    *   `CBinary& operator +=(const CBinary& binData)`: 追加另一个 CBinary 对象。
    *   `BYTE GetAt(WORD nIndex)`: 获取指定索引处的字节。
    *   `WORD GetSize()`: 获取大小。
    *   `BYTE *GetBuffer()`: 获取缓冲区指针。
*   **调用示例**:
    ```cpp
    // 1. 构造 CBinary 对象 (注意：使用 char* 和 长度)
    // 对应头文件: CBinary(const char *pBuffer,WORD iLength);
    const char cmdData[] = "\x02\x19\x02";
    CBinary binCmd(cmdData, 3);

    // 2. 追加数据 (Append 方式)
    // 对应头文件: void Append(const char *pBuffer,WORD iLength);
    binCmd.Append("\x01", 1);

    // 3. 追加数据 (操作符方式)
    // 对应头文件: CBinary& operator +=(const CBinary& binData);
    CBinary binSuffix("\x55", 1);
    binCmd += binSuffix;

    // 4. 获取数据
    // 对应头文件: BYTE GetAt(WORD nIndex);
    BYTE byteVal = binCmd.GetAt(1); // 0x19
    ```

### 3.2 字符串 (TString)
*   **文件路径**: `platform/inc/binary.h`
*   **功能**: 字符串的封装。
*   **约束**: 新代码必须优先使用 `std::string`，仅在调用旧接口时进行转换。
*   **常用接口**:
    *   `const char *AsString()`: 获取 C 风格字符串指针 (注意：非 const 方法)。
    *   `WORD GetLength() const`: 获取字符串长度。
    *   `void Append(const char *str)`: 追加字符串。
    *   `BOOL IsEmpty()`: 判断是否为空。
*   **调用示例**:
    ```cpp
    // 1. 构造 TString
    // 对应头文件: TString(const char *lpsz);
    TString ts("Hello");

    // 2. 获取 C 风格字符串
    // 对应头文件: const char *AsString();
    // 注意：严禁使用 std::string 的 c_str()，TString 中对应的是 AsString()
    const char* rawStr = ts.AsString();

    // 3. 获取长度
    // 对应头文件: WORD GetLength() const;
    // 注意：严禁使用 length()，TString 中对应的是 GetLength()
    WORD len = ts.GetLength();

    // 4. 字符串追加
    // 对应头文件: void Append(const char *str);
    ts.Append(" World");
    ```

### 3.3 数组组 (CGroup)
*   **文件路径**: `platform/inc/binary.h`
*   **功能**: 模板类，用于封装数组/列表。
*   **约束**: 新代码必须优先使用 `std::vector`，仅在调用旧接口时进行转换。
*   **常用接口**:
    *   `void Add(TYPE newElement)`: 添加元素。
    *   `TYPE GetAt(WORD nIndex) const`: 获取元素。
    *   `WORD GetSize() const`: 获取元素个数。
    *   `void Empty()`: 清空容器。
*   **调用示例**:
    ```cpp
    // 1. 构造 CGroup
    CGroup<int> group;

    // 2. 添加元素
    // 对应头文件: void Add(TYPE newElement);
    // 注意：严禁使用 add() (小写)，必须使用 Add() (大写)
    group.Add(10);
    group.Add(20);

    // 3. 获取元素
    // 对应头文件: TYPE GetAt(WORD nIndex) const;
    // 注意：严禁使用 get()，必须使用 GetAt()
    int val = group.GetAt(0);

    // 4. 获取大小
    // 对应头文件: WORD GetSize() const;
    WORD size = group.GetSize();
    ```

---

## 4. 常见误区自检 (Checklist)

在编写调用代码时，请快速自检：

- [ ] **是否尝试 `new` 了平台类？** -> 改用工厂或获取接口指针。
- [ ] **是否忘记检查 `Result.IsOk()`？** -> 必须先检查再使用。
- [ ] **是否对返回的裸指针执行了 `delete`？** -> 除非文档明确说“Transfer Ownership”，否则严禁删除。
- [ ] **是否在回调中执行了耗时操作？** -> 异步回调应尽快返回，耗时任务应抛到工作线程。
- [ ] **是否假设了特定的实现细节？** -> 仅依赖头文件中的接口定义。
