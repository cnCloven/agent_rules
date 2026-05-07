# 配置与数据系统 API 速查 (file.h)

> **头文件路径：** `file.h`
>
> 提供全局配置管理、INI 配置文件读写、产品信息、数据库操作、二进制文件读写、菜单树导航等基础设施接口。

---

## 1. CConfig — 全局配置管理（全 static）

### 目录配置

| 方法签名 | 说明 |
|----------|------|
| `SetDiagDirectory(TString)` / `GetDiagDirectory()` | 诊断数据目录 |
| `SetUserDataDirectory(TString)` / `GetUserDataDirectory()` | 用户数据目录 |
| `SetDispDirectory(TString)` / `GetDispDirectory()` | 显示资源目录 |
| `SetMotorDirectory(TString)` / `GetMotorDirectory()` | 电机目录 |

### 语言/区域

| 方法签名 | 说明 |
|----------|------|
| `SetLanguage(TString)` / `GetLanguage()` | 当前语言代码（"CN"/"EN"等） |
| `SetMetric(BYTE)` / `GetMetric()` | 0=公制, 1=英制 |
| `SetCodePage(UINT)` / `GetCodePage()` | 代码页 |

### 车辆信息

| 方法签名 | 说明 |
|----------|------|
| `SetVIN(TString)` / `GetVIN()` | VIN码 |
| `GetVehicleName()` | 车型名称（只读） |
| `SetVehicleInfo(TString)` / `GetVehicleInfo()` | 车辆信息 |
| `SetVehicleID(UINT)` / `GetVehicleID()` | 车型ID |

### 产品

| 方法签名 | 说明 |
|----------|------|
| `SetProductType(int)` / `GetProductType()` | 产品类型 |
| `SetSerialNumber(TString)` / `GetSerialNumber()` | 序列号 |
| `GetSerialPort()` | 串口号 |
| `IsSupportKC100()` / `EnableSupportKC100(BOOL)` | KC100支持 |

### 扫描模式

| 方法签名 | 说明 |
|----------|------|
| `SetScanType(BYTE)` / `GetScanType()` | 扫描类型（0x00默认, 0x01 PRE/POST-SCAN阶段1, 0x02阶段2, 0x10 JD, 0x21 AD20单系统, 0x22 AD20全系统等） |
| `SetScanPath(TString)` / `GetScanPath()` | 扫描路径 |
| `SetScanIdm(UINT)` / `GetScanIdm()` | 扫描IDM |
| `SetSpecFlag(UINT)` / `GetSpecFlag()` | 特殊功能标志 |

### 菜单/UI

| 方法签名 | 说明 |
|----------|------|
| `SetLinkMenu(TString)` / `GetLinkMenu()` | 外链菜单名称 |
| `SetMenuParam(TString)` / `GetMenuParam()` | 菜单参数 |
| `EnableMenuMaterial(BOOL)` / `IsMenuMaterial()` | 菜单材质风格 |
| `EnableTopology(BOOL)` / `IsTopology()` | 拓扑模式 |
| `IsNewAPP()` / `DecideNewAPP(BOOL)` | 新APP标识 |

### 日志

| 方法签名 | 说明 |
|----------|------|
| `SetLogFile(TString)` / `GetLogFile()` | 日志文件路径 |
| `SetHistoryFile(TString)` / `GetHistoryFile()` | 历史文件路径 |
| `SetLogStampFlag(eLogStamp, BOOL)` | 日志时间戳标志 |
| `GetLogStampFlag()` → `WORD` | 获取日志标志 |
| `SetLogStampCutLen(int=14)` / `GetLogStampCutLen()` | 日志裁剪字节长度 |
| `GetLogStampWriteFlag(eLogStamp)` → `TString` | 获取日志写标志 |

### 运行

| 方法签名 | 说明 |
|----------|------|
| `SetRunFlag(BYTE)` / `GetRunFlag()` | 运行标志 |
| `SetDataFile(TString)` / `GetDataFile()` | 数据文件 |
| `SetDynamicInfo(TString)` / `GetDynamicInfo()` | 动态信息字符串 |
| `EnableMessage(BOOL)` / `IsShowMessage()` | 消息显示开关 |
| `SetDiagIP(TString)` / `GetDiagIP()` | 诊断IP |
| `SetExFunc(UINT)` / `GetExFunc()` | 扩展功能设置 |
| `SetLicensePath(TString)` / `GetLicensePath()` | License文件路径 |
| `SetTitle(TString)` / `GetTitle()` | 标题 |

### 常量定义

```cpp
// 运行标志
RUN_NORMAL  = 0
RUN_DEBUG   = 1
RUN_DEMO    = 2
RUN_MCU     = 4
RUN_LOG     = 8
RUN_HISTORY = 0x10

// 产品类型
Product_Default   = 0
Product_PS65
Product_CheckAuto
Product_EZ300
Product_i80PAD
Product_MJKJ
Product_iVCI
Product_H6PRO
Product_CAERI

// 扫描类型
SCAN_JD             = 0x10
SCAN_AD20           = 0x20
SCAN_AD20_SINGLE_SYS = 0x21
SCAN_AD20_ALL_SYS   = 0x22

// 日志时间戳枚举 eLogStamp
LOG_STAMP_TIME_DIAG_COMM = 1
LOG_STAMP_TIME_ALL       = 2
LOG_STAMP_FLAG_DIAG_D    = 4
LOG_STAMP_CUT            = 8

// 扩展功能枚举 eExFunc
EX_FUNC_GATEWAY = 0x01
```

---

## 2. CProfile — INI 配置文件读写（全 static）

| 方法签名 | 说明 |
|----------|------|
| `GetString(fileName, section, key, default)` → `TString` | 读取字符串 |
| `GetInteger(fileName, section, key, default)` → `int` | 读取整数 |
| `WriteString(fileName, section, key, value)` → `BOOL` | 写入字符串 |
| `WriteInteger(fileName, section, key, value)` → `BOOL` | 写入整数 |

---

## 3. CInformation — 产品信息（全 static）

| 方法签名 | 说明 |
|----------|------|
| `SetProductName(const char*)` / `GetProductName()` | 产品名称 |
| `SetSoftName(const char*)` / `GetSoftName()` | 软件名称 |
| `SetSoftVersion(float)` / `GetSoftVersion()` | 软件版本 |
| `GetLibdiagVersion()` → `TString` | 平台库版本号（格式 `"x.x.x.x_Txx xx"`） |

---

## 4. CDatabase 命名空间 — 数据库操作

### 4.1 MDB/BIN 文件操作

| 方法签名 | 说明 |
|----------|------|
| `Init(TString strFile)` → `BOOL` | 初始化MDB |
| `SetDatabase(TString strDatabase)` → `BOOL` | 设置当前DB |
| `SearchBinary(TString file, CBinary id)` / `SearchId(TString file, CBinary id)` → `CBinaryGroup` | 按索引ID查数据 |
| `GetIdByIndex(int index)` → `CBinary` | 获取指定下标的索引ID |
| `GetBinIdByIndex(TString file, int index)` → `CBinary` | 获取独立BIN文件中指定下标的ID |
| `GetAddrByIndex(int index)` → `UINT` | 获取指定下标对应数据地址 |
| `GetData(UINT addr)` → `CBinaryGroup` | 获取指定地址的数据 |
| `GetBinData(TString file, UINT addr)` → `CBinaryGroup` | 获取独立BIN指定地址数据 |
| `GetIdCount(TString file)` → `int` | 获取索引ID总数 |
| `GetFirstId(TString file, CBinary id)` / `GetNextId(int index, CBinary id)` → `int` | 顺序查找 |
| `QuickFindId(TString file, CBinary id)` → `int` | 二分查找 |
| `Destroy()` | 释放资源 |

### 4.2 文本/资源加载

| 方法签名 | 说明 |
|----------|------|
| `LoadText(CBinary id)` → `TString` | 加载文本 |
| `LoadAttr(CBinary id)` → `TString` | 加载属性 |
| `LoadExpress(CBinary id)` → `TString` | 加载表达式 |
| `LoadGroup(CBinary id)` → `CBinary` | 加载分组 |
| `LoadCommand(CBinary id)` → `CBinary` | 加载命令 |
| `GetCommand(CBinary id)` → `CSendFrame` | 获取发送命令帧 |

### 4.3 INI 配置解析（SetProfile 后可用）

| 方法签名 | 说明 |
|----------|------|
| `SetProfile(TString fileName, CBinary id, char sp=',')` → `BOOL` | 设置当前INI配置 |
| `GetSections(int index=0)` → `CGroup<TString>` | 获取所有节 |
| `GetSectionKeys(TString section, int index=0)` → `CGroup<TString>` | 获取节下所有键 |
| `GetBinary/GetString/GetInteger/GetHex(section, key, index=0)` | 读取指定节键值 |
| `GetBinaryGroup/GetStringGroup/GetWordGroup/GetDWordGroup/GetIntGroup/GetHexGroup(section, key, index=0)` | 读取分组值 |

### 4.4 搜索/MD5

| 方法签名 | 说明 |
|----------|------|
| `SearchFile(CGroup<CStringGroup>&, SearchStr)` → `BOOL` | 文件搜索 |
| `MD5Digest(CBinary/TString/BYTE*/const char*)` → `CBinary` | MD5哈希 |

### 4.5 全局 Item 操作

| 方法签名 | 说明 |
|----------|------|
| `GetItem()` → `CBinaryGroup` | 获取全局Item |
| `SetItem(CBinaryGroup)` | 设置全局Item |

---

## 5. CDataFile — 二进制数据文件

**类型枚举：** `typeData=1, typeDiag, typeDisp, typeUser`

| 方法签名 | 说明 |
|----------|------|
| `Open(TString file, BYTE type, BYTE flag)` → `BOOL` | 打开文件 |
| `ReadData(UINT addr, void*, int len)` / `ReadData(void*, int len)` → `int` | 读取数据 |
| `WriteData(UINT addr, void*, int len)` / `WriteData(void*, int len)` → `int` | 写入数据 |
| `ReadDataDecrypt(addr, data, len, level)` / `WriteDataEncrypt(addr, data, len, level)` | 加密读写 |
| `ReadByte(UINT)` / `ReadWord(UINT)` / `ReadDWord(UINT)` | 读取基础类型 |
| `Seek(UINT addr)` / `GetPosition()` / `GetSize()` / `GetFileSize()` | 文件定位 |
| `IsEOF()` / `Close()` | 关闭 |
| 静态：`DeleteFile(TString)`, `IsExistFile(TString)`, `CreateFolder(TString)`, `DeleteFolder(TString)` | 文件管理 |

---

## 6. CBinaryFile — 二进制文件读取（继承 CDataFile）

| 方法签名 | 说明 |
|----------|------|
| `SetDatabase(TString)` / `SetCurrFile(TString)` | 设置数据库/文件 |
| `SearchId(CBinary id)` → `CBinaryGroup` | 查找ID |
| `GetIdByIndex/GetAddrByIndex/GetData/GetFirstId/GetNextId/GetIdCount/QuickFindId` | 同CDatabase |
| `QuickSearch(const char* text, int rowNum, int maxStrLen)` → `UINT` | 快速文本搜索 |

---

## 7. CMdbFileReader — 线程安全 MDB 文件读取器

> 解决多线程文件句柄共享问题，接口同 CDatabase，独立文件句柄。

| 方法签名 | 说明 |
|----------|------|
| `Init(TString path, TString lang="")` → `BOOL` | 初始化 |
| `SetDatabase/SearchBinary/SearchId/LoadText/LoadAttr/LoadExpress/LoadGroup/GetCommand/LoadCommand` | 同CDatabase |
| `SetProfile/GetSections/GetSectionKeys/GetBinary/GetString/GetInteger/GetHex/...Group(...)` | INI解析 |
| `GetIdByIndex/GetAddrByIndex/GetData/GetIdCount/QuickFindId/GetFirstId/GetNextId` | 索引操作 |

---

## 8. CMenuNode 命名空间 — 菜单树导航

| 方法签名 | 说明 |
|----------|------|
| `Init(UINT id)` → `UINT` | 初始化菜单节点 |
| `GetNext(UINT addr)` / `GetParent(UINT addr)` / `GetChild(UINT addr)` → `UINT` | 树遍历 |
| `GetTaskId(UINT addr)` → `DWORD` | 获取任务ID |
| `GetParam(UINT addr)` → `DWORD` | 获取参数 |
| `GetMenuText(UINT addr)` / `GetExtraText(UINT addr)` → `TString` | 获取菜单文本 |

---

## 9. 全局函数

| 方法签名 | 说明 |
|----------|------|
| `AfxLoadString(CBinary id, const char* file=NULL)` → `TString` | 加载字符串资源 |
| `SetAllConfig(AFX_RUN_CONFIG config)` | 批量设置所有配置 |

---

## 典型使用示例

### 读取配置

```cpp
TString lang = CConfig::GetLanguage();        // "CN"
TString diagDir = CConfig::GetDiagDirectory();
BYTE metric = CConfig::GetMetric();            // 0=公制
```

### INI 文件读写

```cpp
TString val = CProfile::GetString("config.ini", "General", "Version", "1.0");
CProfile::WriteString("config.ini", "General", "Version", "2.0");
```

### 数据库查询

```cpp
CDatabase::SetDatabase("XTOOL0009.BIN");
CBinaryGroup bg = CDatabase::SearchId("XTOOL0009.BIN", binId);
TString text = CDatabase::LoadText(textId);
```

### INI 配置解析

```cpp
CDatabase::SetProfile("XTOOL0001.BIN", binId);
CGroup<TString> sections = CDatabase::GetSections();
TString val = CDatabase::GetString("READDTC", "DtcCmd");
```

### 文件操作

```cpp
CDataFile file;
if (file.Open("data.bin", CDataFile::typeDiag)) {
    BYTE b = file.ReadByte(0x100);
    file.Close();
}
```
