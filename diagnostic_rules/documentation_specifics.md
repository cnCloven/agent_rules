## 1. 协议一致性声明 PICS（Protocol Implementation Conformance Statement）

### 1.1 目标

- 明确声明：本车系实现的 UDS / DoIP / RP1210 能力与限制；
- 供 OEM、测试团队、集成方与架构师快速判断协议兼容性。

### 1.2 放置位置与命名建议

```text
HD_<Carline>/doc/protocol/
  ├─ pics_uds.md
  ├─ pics_doip.md
  ├─ pics_can_transport.md (如需)
  └─ pics_oem_extensions.md
```

### 1.3 PICS 通用结构模板

每个 PICS 文档建议包含以下章节：

1. **Scope / 范围**  
   - 指明适用车系、ECU 范围与适用软件版本。
2. **Reference / 引用标准**  
   - 如：ISO 14229-x, ISO 15765-2, ISO 13400-x, OEM 规范编号。
3. **Supported Features / 支持特性列表**（表格形式）  
4. **Not Supported / 限制与例外**  
5. **Timing / 性能与定时参数**  
6. **Error Handling / NRC 与异常处理行为**

### 1.4 UDS PICS 关键字段（`pics_uds.md`）

至少包括：

- **会话支持**：
  ```markdown
  | Session Type            | SID | Supported | Remarks                  |
  |-------------------------|-----|-----------|--------------------------|
  | DefaultSession          | 0x10 01 | Yes   | 上电默认会话             |
  | ExtendedDiagnostic      | 0x10 03 | Yes   | 支持数据流与例程          |
  | ProgrammingSession      | 0x10 02 | Yes/No | 仅部分 ECU 支持           |
  ```

- **服务支持列表**：
  ```markdown
  | Service                    | SID  | Supported | Notes                            |
  |---------------------------|------|-----------|----------------------------------|
  | DiagnosticSessionControl  | 0x10 | Yes       |                                  |
  | EcuReset                  | 0x11 | Yes       | Soft Reset only                  |
  | ReadDTCInformation        | 0x19 | Yes       | 支持 0x02/0x0A/0x0E 子功能         |
  | SecurityAccess            | 0x27 | Yes       | Level 1/3; SeedKey OEM 专用算法   |
  ```

- **NRC 行为**（只列出实际使用的）：
  ```markdown
  | NRC Code | Meaning                          | Usage                                           |
  |----------|----------------------------------|------------------------------------------------|
  | 0x11     | ServiceNotSupported              | 不支持的 SID 时返回                              |
  | 0x12     | SubFunctionNotSupported          | 不支持子功能时返回                               |
  | 0x13     | IncorrectMessageLengthOrFormat   | 长度错误或格式错误时返回                         |
  | 0x78     | ResponsePending                  | 长时操作统一返回；上层必须轮询或等待             |
  ```

- **Timing 参数**（参考 ISO 与 OEM）：
  ```markdown
  | Parameter | Value (ms) | Configurable | Notes                       |
  |-----------|------------|-------------|-----------------------------|
  | P2        | 50         | Yes         | ECU 响应超时（正常）          |
  | P2*       | 5000       | Yes         | Pending 场景的最大等待时间    |
  ```

### 1.5 DoIP PICS 关键字段（`pics_doip.md`）

- DoIP 版本、支持功能（Vehicle Announcement、Routing Activation 等）；
- 逻辑地址列表（与数据配置保持一致）；
- 安全相关约束（是否允许远程刷写等）。

---

## 2. 架构文档特殊要求（Diagnostic Context）

### 2.1 必备文档列表扩展

建议至少包含以下文件（示例命名）：

- `doc/architecture/overview.md`  
- `doc/architecture/modules.md`  
- `doc/architecture/data_model.md`  
- `doc/architecture/decisions.md`

### 2.2 `overview.md` 内容要求

最少应包括：

1. **系统上下文**  
   - 文字化描述软件与外部实体（VCI、ECU、platform、用户）的关系；
   - 示例：
     ```markdown
     - 外部实体：
       - Platform：提供 UI、通信封装、JSON 与日志能力；
       - VCI：通过 RP1210 动态库与车辆网络交互；
       - ECU：车辆控制单元，支持 UDS over CAN / DoIP。
     ```

### 2.3 `modules.md` 内容要求

- 列出车系内**主要业务模块**（例如 DTC、刷写、编码、安全访问等）；
- 对每个模块，至少描述：
  ```markdown
  ## Module: DiagnosticSessionManager
  - 所在层级：domain
  - 主要职责：
    - 管理 UDS 会话状态（默认/扩展/编程会话）；
    - 向上提供 Start/Stop 接口；
    - 与 IDiagTransport 交互发送 0x10/0x11 等服务。
  ```

### 2.4 `data_model.md` 内容要求

- 描述用于表示 ECU、DTC、服务、数据流等核心领域对象的数据结构；
- 说明这些对象如何从 `HD_<Carline>/data` 加载；
- 指明与 ODX/OTX 概念的对应关系（如 `LogicalEcu`, `BaseVariant` 等）。

---

## 3. 用户手册特殊要求（Diagnostic Context）

### 3.1 必备章节

- **环境准备**：支持的 VCI 类型（RP1210 设备列表）。
- **设备连接与 ECU 识别**：如何选择 VCI，如何连接车辆（OBD 口说明）。
- **主要功能操作步骤**：
  - 读取/清除故障码；
  - 查看实时数据流；
  - 刷写流程（若开放给用户）。
- **安全警告与限制**：明确指出哪些操作可能影响行车安全或车辆状态（如行车禁止操作）。
