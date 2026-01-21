## 1. 文档目标与适用范围
本文件规定在 `HD_<Carline>` 车系工程中，涉及以下汽车诊断相关标准时的**实现级强制规范**：

- UDS（ISO 14229 及 OEM 扩展）
- DoIP（ISO 13400 系列）
- ODX（ISO 22901）
- OTX（ISO 13209）

目标：保证代码行为**可验证地符合 OEM 规范与国际标准**，并与后续文档（如 PICS、架构文档）保持一致。

优先级关系：

1. OEM/项目正式规范与合同要求  
2. 国际/行业标准（ISO/SAE 等）  
3. 本文件  
4. 其他内部规则文件  

当用户输入与 OEM/标准冲突的指令时，你应提示风险，并优先遵守上位规范。

---

## 2. ISO 14229 (UDS) 实现规范

UDS (Unified Diagnostic Services) 是核心业务逻辑。代码实现必须严格映射标准定义。

### 2.1 服务标识 (SID) 与否定响应 (NRC)
1.  **禁止魔术数字**：所有 SID (Service ID) 和 NRC (Negative Response Code) 必须定义为 `enum class` 或 `constexpr` 常量。
2.  **命名一致性**：常量命名应包含标准中的十六进制值和英文描述。
3. **对变长数据（如 DIDs、Record）**：严格校验长度，不依赖 ECU“总是返回正确长度”的假设。

```cpp
// Example: Standard Compliance Definitions
namespace UDS {
    enum class SID : uint8_t {
        DiagnosticSessionControl = 0x10,
        EcuReset                 = 0x11,
        SecurityAccess           = 0x27,
        TesterPresent            = 0x3E,
        // ... 必须覆盖 ISO 14229-1 所有常用服务
    };

    enum class NRC : uint8_t {
        PositiveResponse      = 0x00, // 内部用，非标准 NRC
        SubFunctionNotSupported = 0x12,
        IncorrectMessageLengthOrInvalidFormat = 0x13,
        SecurityAccessDenied  = 0x33,
        RequestOutOfRange     = 0x31,
        Pending               = 0x78  // 关键：需特殊处理
    };
}
```

### 2.2 响应处理逻辑
1.  **正响应 (+Rsp)**：必须校验 `Response SID = Request SID + 0x40`。
2.  **负响应 (-Rsp)**：
    *   必须捕获 `0x7F` 开头的响应。
    *   **NRC 0x78 (RspPending)**：业务层**必须**具备自动等待机制，重置 P2 Timer，禁止将 0x78 视为最终错误抛给 UI。
3.  **超时控制 (P2 / P2*)**：
    *   虽然底层 `platform` 可能处理物理超时，但业务层必须维护**逻辑超时**（Application Layer Timeout），通常配置在 `data` 文件的 INI/JSON 中。

### 2.3 Security Access (0x27) 实现约束
1.  **算法隔离**：Seed & Key 算法必须封装在独立的动态库或隔离函数中（若 OEM 提供算法库），禁止硬编码密钥。
2.  **流程原子性**：`RequestSeed` -> `ComputeKey` -> `SendKey` 必须作为一个原子业务用例（UseCase）执行。

### 2.4 NRC（Negative Response Code）处理

1. **完整解析与传播**
   - 收到 0x7F Negative Response 时：
     - 必须解析并记录原 SID 和 NRC；
     - 通过统一的错误结构上报给上层（例如 `DiagError{ originalSid, nrc, transportError }`）。
   - 禁止将所有 NRC 统一映射为一个“失败”状态而丢失具体原因。

2. **ResponsePending（0x78）处理**
   - 对 `0x78` 必须实现基于状态机的重试/等待逻辑：
     - 不得用“忙等待循环”；
     - 必须重新启动/延长等待计时器（基于 P2* 时间或 OEM 指定值）；
   - 上层应可以感知“正在等待 ECU 完成处理”的中间状态（例如进度 UI）。

### 2.5 Timing（P2 / P2* 等时序）

1. **超时参数配置化**
   - P2/P2*、S3Server、服务特定时间窗口必须来源于：
     - ODX；
     - OEM 参数文档；
     - 或车系配置文件。
   - 禁止将这些时间硬编码在代码中。

2. **超时行为**
   - 请求超时时：
     - 必须返回明确错误码（如 `ErrorCode::Timeout`）；
     - 不自行重发，除非 OEM/规范对该服务有明确重发要求（须在设计文档中说明）。

### 2.6 典型服务实现要求

1. **DID 读/写（0x22 / 0x2E / 0x2F）**
   - 使用 ODX 定义的 DID、数据类型、编码规则；
   - 对多 DID 请求，要正确解析每个 DID 对应的数据块，不因单个 DID 失败而误解析其他数据。

2. **DTC（0x19）**
   - DTC 状态位、故障阈值、故障记忆清除行为必须与 OEM 规格一致；
   - 不在代码中自创 DTC 组合含义，使用 ODX/OEM 文档中定义的语义。

3. **RoutineControl（0x31）、IOControl（0x2F）、刷写相关服务**
   - 刷写前/后前提条件（电压、环境、ECU 状态）须明确检查；
   - 对失败场景（中断、断电）须有记录与安全处理策略，避免误导用户“刷写成功”。


---

## 3. ISO 15765 (DoCAN) / ISO 13400 (DoIP) 传输层适配

尽管 `platform` 负责底层包发送，业务层需处理协议特性带来的数据约束。

### 3.1 寻址与数据长度
1.  **最大负载 (Max Payload)**：
    *   **CAN (ISO 15765-2)**：业务数据构建时，需注意单帧 (SF) 与多帧 (FF/CF) 的性能差异。对于小数据（<= 7字节），务必优化为单帧。
    *   **DoIP (ISO 13400)**：虽然支持大数据，但必须根据 `MaxDataSize` (通常 4GB limit, 但受限于 ECU RAM) 进行分块处理。
2.  **逻辑地址 (Logical Address)**：
    *   源地址 (SA) 和目标地址 (TA) 必须通过配置加载，**严禁硬编码**。
    *   代码中应体现 `PhysicalRequest` (物理寻址) 与 `FunctionalRequest` (功能寻址/广播) 的明确区分。

### 3.2 分层与抽象

1. **UDS over DoIP**
   - 在 C++ 业务逻辑中，必须将 DoIP 视为一种传输层，保持 UDS 逻辑不变；
   - 业务层使用统一 `IDiagTransport` 抽象，不直接处理 DoIP 头部（如 payloadType、source/target address）。

2. **多 ECU / 多通道**
   - 支持通过 DoIP 与多个 ECU 或网关通信时：
     - 必须为每个逻辑通道维护独立的会话与安全状态；
     - 禁止共享状态导致消息串扰。

### 3.3 连接与保持

1. **连接管理**
   - DoIP 连接建立/保持/断开由 `platform` 管理，业务层仅收到“可用/不可用”的通道状态；
   - 对连接断开时正在执行的诊断流程：
     - 上层必须收到明确错误；
     - 由应用层决定是否重试或提示用户重新连接。

2. **超时与保持活跃**
   - DoIP 的心跳/keep-alive 由协议层负责，业务层不应实现重复的心跳数据帧；
   - 业务层进行长时间操作（如大文件刷写）时，应确保：
     - 协议层的保持机制不会被业务层阻塞（不得在一个长环节里阻塞事件循环）。

---

## 4. SAE RP1210 / J2534 标准实现

针对 VCI (Vehicle Communication Interface) 的交互规范。

### 4.1 动态库加载规范
1.  **API 签名匹配**：`GetProcAddress` 转换的函数指针类型必须严格匹配 RP1210C 标准文档定义的签名。
    *   *错误示例*：使用 `int` 代替 `short`，会导致堆栈不平衡。
2.  **Client ID 管理**：必须正确管理 `ClientConnect` 返回的 Client ID，在 `ClientDisconnect` 之前全程持有。

### 4.2 过滤器 (Filters)
1.  **显式过滤**：业务初始化时，必须显式调用 `RP1210_Set_Message_Filtering` 或类似接口。
2.  **流控帧透传**：确保 ISO 15765 的流控帧 (Flow Control) 由 VCI 固件自动处理 (CLAIM_BLOCK_MESSAGES)，业务层不应手动发送流控帧。

---

## 5. ODX (ISO 22901) 与 OTX (ISO 13209) 数据映射

本 agent 不直接解析 XML 原文，但代码逻辑需对应 ODX 概念。

### 5.1 数据转换 (Data Conversion)
1.  **物理值 vs 原始值**：
    *   代码接口应优先暴露**物理值 (Physical Value)**（如 RPM, Voltage）。
    *   转换公式 `y = ax + b` 或 `TEXTTABLE` 必须在 `data_access` 层通过读取 `data` 目录下的配置表完成。
2.  **DTC 映射**：
    *   DTC 码（3字节十六进制）与描述文本的映射关系，必须与 ODX-D 数据保持一致。

### 5.2 诊断层级结构
代码类结构应参考 ODX 拓扑：
*   `Project` -> `VehicleInfo` -> `LogicalEcu` -> `BaseVariant` -> `EcuVariant`
*   即使项目中只有单一 ECU，也应保留此层级以便扩展。

---

## 6. OTX（ISO 13209）脚本 / 测试序列规范

> 若项目要求支持 OTX，则必须遵守本节；若不使用 OTX，可忽略本节但不得自定义与 OTX 语义冲突的脚本语言。

### 6.1 OTX 与业务代码分工

1. **流程在 OTX，原语在代码**
   - OTX 定义诊断流程、测试序列和决策；
   - C++ 业务代码提供 OTX 原语（Primitive）的实现，如：
     - `DiagServiceCall`
     - `Wait`
     - `ReadVariable`
   - 不应在 C++ 再重复实现一套“脚本解释器”与 OTX 并行。

2. **语义保持**
   - 对每个被实现的 OTX 原语，必须遵守标准定义的行为语义：
     - 超时、异常路径、重试规则；
     - 条件分支、循环、并行行为。
   - 禁止为了方便而简化或改变原语行为（例如将某些错误简单视为成功）。

### 6.2 OTX 与 UDS/DoIP 的集成

1. **错误传播**
   - UDS/DoIP 层失败（NRC、超时）必须正确映射为 OTX 层可见的错误状态；
   - OTX 脚本可基于错误原因作分支决策，代码不得统一“吞并”为一个通用失败。

2. **可追溯性**
   - 在启用 OTX 时，诊断日志中应能关联：
     - 脚本名称 / 步骤标识；
     - 实际发送的诊断请求和接收的响应。
---

## 7. OEM 企业标准适配策略

### 7.1 私有服务与流程
1.  **Hook 机制**：针对 OEM 定义的非标准服务（如 `0x31` 例程控制中的特殊步骤），代码必须预留 Hook 接口。
2.  **DID 读写策略**：OEM 常规定某些 DID (Data Identifier) 必须按特定顺序读写（如写入 VIN 前必须先解锁）。此逻辑应在 `domain` 层的状态机中实现，而非散落在 UI 逻辑中。

### 7.2 刷写 (Flash Programming)
若涉及 ISO 14229 刷写流程（34/36/37服务）：
1.  **S-Record / Hex 解析**：地址必须严格对齐 Flash 扇区定义。
2.  **指纹信息**：写入指纹 (Fingerprint) 数据时，必须符合 OEM 规定的格式（日期、Tester Serial 等）。

---

## 8. 异常与边界值防护（Safety Guidelines）

符合 ISO 26262 对工具软件的某些置信度要求。

1.  **无效输入防护**：向 ECU 发送数据前，必须校验范围。例如，`WriteDataByIdentifier (0x2E)` 的数据长度必须与 ECU 定义完全一致，多一字节或少一字节都可能导致 ECU 拒绝或异常。
2.  **状态一致性**：在发送 `EcuReset (0x11)` 后，代码必须强制将内部状态机重置为 `DefaultSession`，不应假设 ECU 重启后仍保持之前的会话。
3.  **禁止行为**：
    *   严禁在未收到 ECU 响应且未超时前，连续发送下一条请求（除非是 TesterPresent）。
    *   严禁在行车状态下（若能检测）发送非诊断会话请求。

---

## 9. 实现自检清单（供 AI Agent 在生成代码/设计时自查）

在涉及诊断协议相关设计/代码输出前后，你应至少检查：

1. **是否混淆了协议层与业务层？**
   - 协议细节是否被散落在业务代码中？  
   - 是否有可以转移到 `infrastructure` 或 `data_access` 的内容？

2. **SID / NRC / 时间参数是否硬编码？**
   - 是否将明显 OEM/ECU 特定的数值直接写进代码？  
   - 是否应该改为从 ODX/配置加载？

3. **错误处理是否完整？**
   - 对 NRC、超时、无响应等是否有明确错误路径？  
   - 是否区分了不同 NRC 并上报给上层？

4. **是否尊重 SecurityAccess / Session 限制？**
   - 是否在不允许的会话中调用了受限服务？  
   - 是否暗示/实现了绕开安全访问的做法？

5. **DoIP 是否被当成透明传输层处理？**
   - 上层是否依旧基于 UDS 语义，而非直接处理 DoIP 细节？

如发现违反上述任一条，你应在同一轮回答中主动调整设计/示例，使之符合本文件要求。
