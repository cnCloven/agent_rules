# 通信系统 API 速查 (comm.h)

> 头文件: `D:\work\platform\inc\comm.h`
> 适用于平台通信层开发，详细 wiki 参考 RequireDoc/

---

## CSendFrame — 发送帧构造

### 枚举常量

| 常量 | 值 | 说明 |
|------|----|------|
| `RFN_AUTO` | 0xFF | 自动接收帧数 |
| `RFN_LOOP` | 0xFE | 循环接收 |
| `RFN_MULT` | 0xFC | 多帧接收 |
| `RFN_HOLD` | 0xFB | 保持接收 |
| `RFN_FLASH` | 0xF9 | Flash接收 |

### 内部类 CFrame 成员

| 成员 | 说明 |
|------|------|
| `m_binSendCmd` | 发送命令数据 |
| `m_nReceiveFrameNumber` | 接收帧数 |
| `m_iCanbusId` | CAN总线ID |
| `m_nDumpByte` | 转储字节 |

### 接口速查

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `CSendFrame()` | — | — | 默认构造 |
| `operator=(CSendFrame&)` | CSendFrame引用 | CSendFrame& | 赋值运算符 |
| `operator+=(CSendFrame&/CBinaryGroup&/CBinary&/CFrame&)` | 各类型引用 | CSendFrame& | 追加运算符 |
| `Add(CBinary&)` | 发送数据 | — | 添加发送数据 |
| `Add(CBinaryGroup&)` | 一组数据 | — | 添加一组数据 |
| `Add(CBinary&, UINT iCanbusId, BYTE nDumpByte)` | 数据、CAN ID、转储字节 | — | 添加带CAN ID数据 |
| `operator[](BYTE)` | 帧索引 | CFrame& | 获取帧（下标方式） |
| `GetFrame(BYTE)` | 帧索引 | CFrame& | 获取帧 |
| `SetDefaultReceiveFrameNumber(BYTE n=0x01)` | 默认帧数 | — | 设置默认接收帧数 |
| `Empty()` | — | — | 清空所有帧 |
| `GetSize()` | — | WORD | 获取帧数量 |

---

## CReceiveFrame — 接收帧解析

### 接口速查

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `operator=(CReceiveFrame&/CBinary&/CBinaryGroup&)` | 各类型引用 | CReceiveFrame& | 赋值运算符 |
| `operator+=(CReceiveFrame&/CBinary&/CBinaryGroup&)` | 各类型引用 | CReceiveFrame& | 追加运算符 |
| `Add(CBinary&)` | 二进制数据 | — | 添加接收帧 |
| `Add(CBinaryGroup&)` | 一组数据 | — | 添加一组接收帧 |
| `Add(CReceiveFrame&)` | 接收帧引用 | — | 合并接收帧 |
| `operator[](WORD)` | 帧索引 | CBinary& | 获取帧（下标方式） |
| `GetFrame(WORD)` | 帧索引 | CBinary& | 获取帧 |
| `Empty()` | — | — | 清空所有帧 |
| `GetSize()` | — | WORD | 获取帧数量 |
| `IsEmpty()` | — | BOOL | 判断是否为空 |
| `RemoveAt(WORD index, SHORT count=1)` | 起始索引、删除数量 | — | 删除指定位置帧 |

---

## CProtocol — 协议处理

### 成员变量

| 成员 | 说明 |
|------|------|
| `m_nProtType` | 协议类型 |
| `m_nCommTime[4]` | 通信时间参数 |
| `m_nCanType` | CAN类型 |
| `m_nDumpByte` | 转储字节 |
| `m_nFlowPosi` | 流控位置 |
| `m_nTargetAddr` | 目标地址 |
| `m_nSourceAddr` | 源地址 |
| `m_nHeaderByte` | 头字节 |
| `m_nCanbusId` | CAN总线ID |
| `m_nDoipAddr` | DoIP地址 |

### 接口速查

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| **通用打包解包** | | | |
| `Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | 通用协议打包 |
| `Unpack(CBinary&)` | 原始数据 | CBinary | 通用协议解包 |
| **KWP协议** | | | |
| `KWP_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | KWP打包 |
| `KWP_Unpack(CBinary&)` | 原始数据 | CBinary | KWP解包 |
| **ISO协议** | | | |
| `ISO_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | ISO打包 |
| `ISO_Unpack(CBinary&)` | 原始数据 | CBinary | ISO解包 |
| **CAN协议** | | | |
| `CAN_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | CAN打包 |
| `CAN_Unpack(CBinary&)` | 原始数据 | CBinary | CAN解包 |
| **CANFD协议** | | | |
| `CANFD_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | CANFD打包 |
| `CANFD_Unpack(CBinary&)` | 原始数据 | CBinary | CANFD解包 |
| **其他协议** | | | |
| `VPWM_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | VPW打包 |
| `BOSCH_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | BOSCH打包 |
| `BOSCH_Unpack(CBinary&)` | 原始数据 | CBinary | BOSCH解包 |
| `BMW_CAN_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | BMW CAN打包 |
| `BMW_CAN_Unpack(CBinary&)` | 原始数据 | CBinary | BMW CAN解包 |
| `BMW_MODE2_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | BMW MODE2打包 |
| `BMW_MODE2_Unpack(CBinary&)` | 原始数据 | CBinary | BMW MODE2解包 |
| `BMW_MODE3_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | BMW MODE3打包 |
| `BMW_MODE3_Unpack(CBinary&)` | 原始数据 | CBinary | BMW MODE3解包 |
| `BMW_DOIP_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | BMW DoIP打包 |
| `BMW_DOIP_Unpack(CBinary&)` | 原始数据 | CBinary | BMW DoIP解包 |
| `DOIP_Pack(DWORD flag, CBinary&)` | 标志、数据 | CBinary | DoIP打包 |
| `DOIP_Unpack(CBinary&)` | 原始数据 | CBinary | DoIP解包 |
| **静态校验** | | | |
| `CheckSum(CBinary&)` | 数据 | — | 校验和 |
| `CheckCrc(CBinary&)` | 数据 | — | CRC校验 |
| `CheckXor(CBinary&)` | 数据 | — | 异或校验 |
| `CheckData(CBinary&, BYTE type)` | 数据、校验类型 | — | 通用数据校验 |
| **参数设置** | | | |
| `SetParameter(BYTE target, BYTE source)` | 目标地址、源地址 | — | 设置协议参数 |
| `SetParameter(BYTE header, BYTE target, BYTE source)` | 头字节、目标、源 | — | 设置协议参数（含头字节） |
| `SetParameter(DWORD sysAddr)` | 系统地址 | — | 设置系统地址参数 |
| `SetCanbusId(DWORD id, BYTE extra)` | CAN ID、扩展字节 | — | 设置CAN总线ID |
| `SetDoipAddr(WORD addr)` | DoIP地址 | — | 设置DoIP地址 |

---

## CCommEcu 命名空间 — ECU通信核心

> 命名空间中的函数直接调用，如 `CCommEcu::Init()`, `SendReceive(...)` 等。
> 注：常用的 `SendReceive`、`SendReceiveFrame` 等也作为全局函数可不加命名空间前缀直接调用。

### 初始化与销毁

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `Init()` | — | — | 默认初始化 |
| `Init(serialPort, parity, stopBit)` | 串口号、校验位、停止位 | — | 带串口参数初始化 |
| `Destroy()` | — | — | 销毁通信 |

### 硬件与状态

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetHardwareType(BYTE)` | 硬件类型 | — | 设置硬件类型 |
| `ResetCommbox()` | — | — | 重置通信盒 |
| `TestCommbox()` | — | — | 测试通信盒 |
| `GetStatus()` | — | — | 获取通信状态 |
| `GetAdcValue()` | — | double | 获取ADC值 |
| `GetPowerVolt()` | — | WORD | 获取电源电压 |
| `GetVciBaudrate()` | — | — | 获取VCI波特率 |
| `GetVciType()` | — | — | 获取VCI类型 |
| `GetVciVersion()` | — | — | 获取VCI版本 |
| `GetVciSerialNumber()` | — | — | 获取VCI序列号 |
| `IsSupportCANFD()` | — | — | 是否支持CANFD |
| `IsSupportSelectPin()` | — | — | 是否支持引脚选择 |
| `GetPinVolt(CGroup<double>*)` | 电压数组指针 | — | 获取引脚电压 |

### 超时与延时

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetTimeout(UINT ms)` | 超时毫秒 | — | 设置通信超时 |
| `GetTimeout()` | — | — | 获取当前超时值 |
| `SetCommDelay(WORD)` | 延时值 | — | 设置通信延时 |
| `SetCommDelay100us(WORD)` | 延时值(100us) | — | 设置通信延时(100us) |
| `SetCommDelayTick(WORD)` | 延时Tick | — | 设置通信延时Tick |
| `SetCommDelayRTC(WORD)` | 延时RTC | — | 设置通信延时RTC |

### 通道与协议

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetChannel(BYTE=CHAN_STD)` | 通道号 | — | 设置通信通道 |
| `GetChannel()` | — | — | 获取当前通道 |
| `SetProtocol(WORD, BOOL=TRUE)` | 协议类型、使能 | — | 设置通信协议 |
| `GetProtocol()` | — | CProtocol* | 获取协议对象指针 |
| `SetCommPort(send, recv, linkCtrl)` | 发送线、接收线、链路控制 | — | 设置通信端口 |
| `SetBenzPort(send, recv, linkCtrl)` | 发送线、接收线、链路控制 | — | 设置奔驰专用端口 |

### 波特率

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetBaudrate(UINT bps, BYTE parity=PB_NONE, BYTE bits=8)` | 波特率、校验、数据位 | — | 设置串口波特率 |
| `SetCanBaudrate(UINT base, UINT data=CANFD_DATABPS_2M)` | 基础波特率、数据波特率 | — | 设置CAN波特率 |
| `AutoSeekBps()` | — | DWORD | 自动搜索波特率 |
| `VciAutoSeekBps(BYTE=0)` | 参数 | — | VCI自动搜索波特率 |

### 通信时间

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetCommTime(P4, P3, P2, P1)` | 四个时间参数 | — | 设置通信时间参数 |

### 链路保持

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `KeepCommLink(BYTE flag)` | LINK_RUN/LINK_STOP | — | 启动/停止链路保持 |
| `KeepCommLink(DWORD flag, WORD keepTime, CBinary&/CSendFrame&/...)` | 标志、间隔时间、保持数据 | — | 带数据的链路保持 |

### 自动流控

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `AutoFlowControl(DWORD flag, CBinary&, WORD delay=0)` | 标志、流控数据、延时 | — | 设置自动流控（带数据） |
| `AutoFlowControl(BYTE flag)` | AFC_ENABLE/AFC_DISABLE | — | 启用/禁用自动流控 |

### 发送与接收

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SendReceive(DWORD flag, CSendFrame&)` | 标志、发送帧 | CReceiveFrame | 发送并接收（多帧） |
| `SendReceive(DWORD flag, CBinary/WORD len, ...)` | 标志、数据/长度 | CReceiveFrame | 发送并接收（重载） |
| `SendReceiveFrame(DWORD flag, CBinary/...)` | 标志、数据 | CBinary | 发送并接收（单帧简化版） |
| `ReceiveOnly(DWORD=DEFAULT, BOOL=FALSE)` | 标志、选项 | CBinary | 仅接收单帧 |
| `ReceiveOnlyMultiFrame(DWORD=DEFAULT, BOOL=FALSE)` | 标志、选项 | CReceiveFrame | 仅接收多帧 |

### 协议透传

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `Pack(DWORD flag, CBinary&)` | 标志、数据 | — | 打包数据 |
| `Unpack(CBinary&)` | 原始数据 | — | 解包数据 |
| `SetParameter(...)` | 参数同CProtocol | — | 设置协议参数 |
| `SetCanbusId(...)` | 参数同CProtocol | — | 设置CAN ID |
| `SetDoipAddr(...)` | 参数同CProtocol | — | 设置DoIP地址 |

### 安全与算法

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `CalcSeedKey(WORD type, CBinary data)` | 算法类型、种子数据 | CBinary | 计算安全密钥 |
| `CallFunction(WORD func, CBinary param)` | 函数号、参数 | CBinary | 调用本地算法函数 |

### 云端与服务器（_COCOS）

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `CallFunction(vin, func, param, seed, pin)` | VIN、函数号、参数、种子、PIN | CBinary | 云端算法调用 |
| `CallFunction2(strFunc, param)` | 函数名、参数 | CBinary | 云端算法调用（字符串版） |
| `CallServerFunc(service, invoke, content, ...)` | 服务、接口、内容 | TString | 调用服务器函数 |
| `UploadServerData(...)` | — | — | 上传数据到服务器 |
| `DownloadServerData(...)` | — | — | 从服务器下载数据 |
| `DownloadFileFromCloud(...)` | — | — | 从云端下载文件 |
| `UploadFileToOSS(...)` | — | — | 上传文件到OSS |
| `DownloadFileFromOSS(...)` | — | — | 从OSS下载文件 |

### DoIP

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `DoipNetworkInit()` | — | — | DoIP网络初始化 |
| `DoipNetworkDestroy()` | — | — | DoIP网络销毁 |
| `DoipCheckNetwork()` | — | — | DoIP网络检测 |
| `DoipCreateConnect(timeout=0)` | 超时时间 | — | 创建DoIP连接 |
| `DoipSendReceive(flag, CSendFrame&)` | 标志、发送帧 | CReceiveFrame | DoIP发送接收 |
| `DoipKeepCommLink(...)` | — | — | DoIP链路保持 |
| `DoipSetIPAddress(...)` | IP地址 | — | 设置DoIP IP地址 |
| `DoipSetCommMode(...)` | — | — | 设置DoIP通信模式 |

### 地址码进入

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `AddressCodeEnter(addressCode, ...)` | 地址码及其他参数 | CReceiveFrame | 地址码进入ECU |

### 快速脉冲

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `QuickPulseEnter(flag, frame, lowTime, highTime)` | 标志、帧、低电平时间、高电平时间 | CBinary | 快速脉冲进入 |

### FlashCode

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `FlashCode(type, bitInterval, byteInterval, ...)` | 类型、位间隔、字节间隔 | CBinary | FlashCode通信 |

### ImmoBox（_COCOS）

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `InitImmoBox()` | — | — | 初始化ImmoBox |
| `SetImmoBoxType(eImmoBoxTye)` | ImmoBox类型 | — | 设置ImmoBox类型 |
| `SendReceiveImmoBox(CBinary)` | 发送数据 | CBinary | ImmoBox通信 |

### 批量操作

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `BeginBatch()` | — | — | 开始批量操作 |
| `EndBatch(flag)` | 标志 | CReceiveFrame | 结束并执行批量 |
| `AddFrameToBuff(...)` | — | — | 添加帧到缓冲区 |
| `RunBatch(...)` | — | — | 运行批量操作 |

### IO电平控制

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetCommLevel(BYTE)` | LEVEL_HIGH/LEVEL_LOW | — | 设置通信电平 |
| `SetDtsLevel(BYTE)` | 电平值 | — | 设置DTS电平 |
| `SetDoIPLevel(BYTE)` | 电平值 | — | 设置DoIP电平 |
| `SetPin7Level(BYTE)` | 电平值 | — | 设置Pin7电平 |
| `SetCan120R(BYTE)` | CAN120R_ON/OFF | — | 设置CAN 120R终端电阻 |
| `GetCommLevel()` | — | — | 获取通信电平 |

---

## CCommFilter 命名空间 — 通信过滤器

### 接口速查

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetNormalFilter(offset, mask, value)` | 偏移、掩码、值 | — | 设置普通过滤器 |
| `SetTimeoutFilter()` | — | — | 设置超时过滤器 |
| `SetKeywordFilter(...)` | 关键字参数 | — | 设置关键字过滤器 |
| `SetCanFilterId(BYTE count, ...)` | 数量、CAN ID列表 | — | 直接设置CAN过滤ID |
| `SetCanFilterBegin()` | — | — | 开始CAN过滤设置 |
| `AddCanFilterId(UINT canId, UINT mask=0xFFFFFFFF)` | CAN ID、掩码 | — | 添加CAN过滤ID |
| `SetCanFilterEnd()` | — | — | 结束CAN过滤设置 |
| `SetCanAllFilter()` | — | — | 接收所有CAN帧 |
| `SetEncryptCanFilterBegin()` | — | — | 开始加密CAN过滤设置 |
| `AddEncryptCanFilterId(TString id, TString mask="")` | ID字符串、掩码字符串 | — | 添加加密CAN过滤ID |
| `SetEncryptCanFilterEnd()` | — | — | 结束加密CAN过滤设置 |

---

## 关键常量

### 协议类型

| 常量 | 值 | 说明 |
|------|----|------|
| `PT_NORMAL` | 0x00 | 普通协议 |
| `PT_KWP` | 0x01 | KWP协议 |
| `PT_ISO` | 0x02 | ISO协议 |
| `PT_CAN` | 0x07 | CAN协议 |
| `PT_CANFD` | 0x1C | CANFD协议 |
| `PT_DOIP` | 0x1A | DoIP协议 |
| `PT_BMW_DOIP` | 0x1B | BMW DoIP协议 |
| `PT_BENZ_DOIP` | 0x23 | 奔驰DoIP协议 |

### CAN波特率

| 常量 | 值 | 说明 |
|------|----|------|
| `CAN_BPS_500K` | 0x01040312 | 500K波特率 |
| `CAN_BPS_250K` | 0x01080712 | 250K波特率 |
| `CAN_BPS_1000K` | 0x01040309 | 1M波特率 |
| `CANFD_DATABPS_2M` | — | CANFD数据段2M |
| `CANFD_DATABPS_5M` | — | CANFD数据段5M |

### 发送接收标志

| 常量 | 值 | 说明 |
|------|----|------|
| `SF_PACK` | 0x0800 | 发送时打包 |
| `RF_UNPACK` | 0x1000 | 接收时解包 |
| `SF_CANS` | 0x010000 | CAN标准帧发送 |
| `RF_COMB` | 0x4000 | 接收帧合并 |
| `SF_DUMP` | 0x0100 | 转储发送 |
| `RF_LOOP` | 0x00FE | 循环接收 |
| `RF_AUTO` | 0x00FF | 自动接收帧数 |
| `RF_MULT` | 0x00FC | 多帧接收 |

### VCI类型

| 常量 | 值 | 说明 |
|------|----|------|
| `VCI_VCI1` | 0x00 | VCI1 |
| `VCI_VCI2` | 0x22 | VCI2 |
| `VCI_VCI3` | 0x3C | VCI3 |
| `VCI_IVCI2` | 0x3A | IVCI2 |
| `VCI_VCIP` | 0x7C | VCIP |
| `VCI_NXP_A1` | 0xA1 | NXP A1 |
| `M600` | 0xA4 | M600 |

### 链路保持与电平

| 常量 | 值 | 说明 |
|------|----|------|
| `LINK_RUN` | 0xFF | 启动链路保持 |
| `LINK_STOP` | 0x00 | 停止链路保持 |
| `LEVEL_HIGH` | 0xFF | 高电平 |
| `LEVEL_LOW` | 0x00 | 低电平 |
| `CAN120R_ON` | 0xFF | CAN 120R终端电阻开启 |

---

## 全局便捷函数

### 通信初始化

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `STD_CAN_INIT(toolId, ecuId, bps=CAN_BPS_500K)` | 工具ID、ECU ID、波特率 | BOOL | 标准CAN初始化 |
| `EXT_CAN_INIT(toolId, ecuId, bps=CAN_BPS_500K)` | 工具ID、ECU ID、波特率 | BOOL | 扩展CAN初始化 |
| `STD_KWP_INIT(targetAddr, sourceAddr, bps=10400, kLine=OBDII_P7)` | 目标地址、源地址、波特率、K线 | BOOL | 标准KWP初始化 |
| `STD_ISO_INIT(addressCode, kLine=OBDII_P7, waitTime=30)` | 地址码、K线、等待时间 | BOOL | 标准ISO初始化 |
| `STD_BOSCH_INIT(addressCode, kLine=OBDII_P7, waitTime=30)` | 地址码、K线、等待时间 | CReceiveFrame | 标准BOSCH初始化 |
| `STD_PWM_INIT()` | — | BOOL | 标准PWM初始化 |
| `STD_VPW_INIT()` | — | BOOL | 标准VPW初始化 |

### 调试日志

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `debug(TString/const char*/CBinary/CReceiveFrame/...)` | 各类型数据 | — | 调试日志输出 |
| `dbglog(const char *fmt, ...)` | 格式化字符串 | — | 格式化日志输出 |
| `dbgstring(const char*)` | 字符串 | — | 字符串日志输出 |

---

## MultComm 命名空间 — 多通道CAN通信

### CMultLinkCanComm

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `StartComm(callback)` | 回调函数 | bool | 启动多通道通信 |

### CommControl

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `SetChanCanCommCfg(...)` | 通道配置参数 | — | 设置通道CAN通信配置 |
| `SetFilterBegin()` | — | — | 开始过滤设置 |
| `AddOneFilter(...)` | 过滤参数 | — | 添加过滤条件 |
| `SetFilterEnd()` | — | — | 结束过滤设置 |
| `SendOnePack(...)` | 数据包 | — | 发送单个数据包 |
| `StopComm()` | — | — | 停止通信 |

### 解包处理器

| 类型 | 说明 |
|------|------|
| `UnPackHandler` | 基础解包处理器 |
| `UDSPackHandler` | UDS协议解包处理器 |
| `NormalCanPackHandler` | 普通CAN解包处理器 |
| `BMWCanPackHandler` | BMW CAN解包处理器 |

### ChannelHandler

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `RegisterIDUnpacker(...)` | ID和解包器 | — | 注册ID解包器 |
| `GetUnPackerViaId(...)` | ID | — | 通过ID获取解包器 |

---

## 典型使用示例

### 标准CAN通信

```cpp
// 初始化通信
STD_CAN_INIT(0x07E0, 0x07E8, CAN_BPS_500K);
// 发送并接收
CBinary binData = SendReceiveFrame(SF_CANS | SF_PACK | RF_UNPACK, CBinary("\x22\xF1\x90", 3));
```

### KWP协议通信

```cpp
STD_KWP_INIT(0x01, 0xF1, 10400, OBDII_P7);
CReceiveFrame rf = SendReceive(KWP_80 | SF_PACK | RF_UNPACK | RF_COMB, CBinary("\x21\x01", 2));
```

### DoIP通信

```cpp
DoipNetworkInit();
DoipSetIPAddress("192.168.1.1");
DoipSetCommMode(PT_BENZ_DOIP, TRUE);
DoipCreateConnect();
SetDoipAddr(0x0001);
CReceiveFrame rf = DoipSendReceive(SF_PACK | RF_UNPACK | RF_COMB, sf);
```

### 链路保持

```cpp
KeepCommLink(SF_CANS | SF_PACK, 2000, CBinary("\x3E\x80", 2));  // 每2秒发3E80
// ... 执行诊断操作 ...
KeepCommLink(LINK_STOP);  // 停止保持
```

### CAN过滤设置

```cpp
SetCanFilterBegin();
AddCanFilterId(0x07E8);
AddCanFilterId(0x07DF);
SetCanFilterEnd();
```
