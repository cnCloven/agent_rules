# 工具与辅助类 API 速查

> 涵盖：delegate.h（代理回调）、calc.h（表达式计算）、jsonBuilder.h（JSON构建）、
> dataconvert.h（数据转换）、devEnvironment.h（设备环境）、encdec.h（加密解密）、
> metric.h（度量单位）、utils.h（工具函数）、excel.h（表格数据）

---

## 1. MyDelegate — 代理回调 (delegate.h)

基于 `std::function` 的事件监听机制。注册回调传入函数对象，注销传入 `nullptr`。

| 方法 | 说明 |
|------|------|
| `addGetMenuPathListener(callback)` / `getMenuPath()` / `isListenGetMenuPath()` | 菜单路径 |
| `addGetLogFileListener(callback)` / `getLogFile()` / `isListenGetLogFile()` | 日志文件获取 |
| `addSetLogFileListener(callback)` / `setLogFile(string)` / `isListenSetLogFile()` | 日志文件设置 |
| `addGetRunFlagListener(callback)` / `getRunFlag()` / `isListenGetRunFlag()` | 运行标志获取 |
| `addSetRunFlagListener(callback)` / `setRunFlag(BYTE)` / `isListenSetRunFlag()` | 运行标志设置 |
| `addGetHistoryFileListener(callback)` / `getHistoryFile()` / `isListenGetHistoryFile()` | 历史文件获取 |
| `addSetHistoryFileListener(callback)` / `setHistoryFile(string)` / `isListenSetHistoryFile()` | 历史文件设置 |
| `addIsEnableIdleListener(callback)` / `isEnableIdle()` / `isListenIsEnableIdle()` | 空闲启用查询 |
| `addOnIdleListener(callback)` / `onIdle()` / `isListenOnIdle()` | 空闲回调 |
| `addGetIdleTimeListener(callback)` / `getIdleTime()` / `isListenGetIdleTime()` | 空闲时间获取 |

---

## 2. CExpress — 表达式计算引擎 (calc.h)

全 static 方法。T_VAR 结构体包含 key、vt（类型）、ival/fval（值）、str、bin。

值类型枚举：VV_FLOAT=0, VV_INT, VV_STR, VV_KCHAR, VV_KBYTE, VV_KFRAME, VV_KBIT, VV_KLEN, VV_KSW, VV_KVAR, VV_BIN

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `Calc(CBinary exp, CReceiveFrame& rf, T_VAR& val, const char* pos=NULL)` | `BOOL` | 表达式计算（二进制表达式+接收帧） |
| `Calc(const char* exp, CReceiveFrame& rf, T_VAR& val, const char* pos=NULL)` | `BOOL` | 表达式计算（字符串表达式） |
| `Calc(CBinary exp, CBinary& data, T_VAR& val, const char* pos=NULL)` | `BOOL` | 表达式计算（二进制数据） |
| `Calc(const char* exp, CBinary& data, T_VAR& val, const char* pos=NULL)` | `BOOL` | 表达式计算（字符串+二进制） |
| `Format(CBinary fmt, T_VAR& val)` / `Format(const char* fmt, T_VAR& val)` | `TString` | 格式化输出 |
| `Calc(CBinary idExpress, CBinary& data, UINT pos=0)` | `TString` | 从数据库表达式计算并格式化 |
| `Calc(TString file, CBinary idExpress, CBinary& data, UINT pos=0)` | `TString` | 从独立BIN文件计算 |

辅助宏：`T_VAL(v)`, `I_VAL(v)`, `F_VAL(v)`, `S_VAL(v,z)`, `V_VV(v1,v2)`

---

## 3. CJsonBuilder — JSON构建器 (jsonBuilder.h)

基于 RapidJson 的流式 JSON 构建。调用顺序：Start → Add → End → Get。

| 方法 | 说明 |
|------|------|
| `Reset()` | 重置 |
| `StartObject()` / `StartObject(const char* key)` | 开始对象 `{}` / `"key": {}` |
| `EndObject()` | 结束对象 |
| `StartArray()` / `StartArray(const char* key)` | 开始数组 `[]` / `"key": []` |
| `EndArray()` | 结束数组 |
| `AddNull(const char* key)` | 添加 null |
| `AddBool(bool)` / `AddBool(key, bool)` | 添加布尔值 |
| `AddInt(int)` / `AddInt(key, int)` | 添加整数 |
| `AddInt64(int64_t)` / `AddInt64(key, int64_t)` | 添加64位整数 |
| `AddDouble(double)` / `AddDouble(key, double)` | 添加浮点数 |
| `AddString(string)` / `AddString(key, string)` | 添加字符串 |
| `AddBoolArray(key, vector<bool>)` | 添加布尔数组 |
| `AddIntArray(key, vector<int>)` | 添加整数数组 |
| `AddInt64Array(key, vector<int64_t>)` | 添加64位整数数组 |
| `AddDoubleArray(key, vector<double>)` | 添加浮点数组 |
| `AddStringArray(key, vector<string>)` | 添加字符串数组 |
| `AddObject(CJsonBuilder&)` / `AddObject(key, CJsonBuilder&)` | 添加嵌套对象 |
| `AddObject(string)` / `AddObject(key, string)` | 从JSON字符串添加对象 |
| `GetJsonString()` → `std::string` | 获取构建的JSON字符串 |

---

## 4. CDataConvertProcess — 数据转换 (dataconvert.h)

全 static 方法。

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `Split(CGroup<TString>& out, TString content, TString sep, BOOL ignoreMulti=TRUE)` | `DWORD` | 字符串分割 |
| `UIntToString(DWORD val, BYTE type=10)` | `TString` | 无符号整数→字符串（10进制/16进制） |
| `UIntToBinary(DWORD val, WORD len=0)` | `CBinary` | 无符号整数→二进制 |
| `IntToDecString(INT val)` | `TString` | 有符号整数→十进制字符串 |
| `StrToUInt(TString val, BYTE type=10)` | `DWORD` | 字符串→无符号整数 |
| `HexDataToString(BYTE* data, WORD len)` | `TString` | 十六进制数据→字符串 |
| `BinaryToString(CBinary data)` | `TString` | Binary→十六进制字符串 |
| `HexStrToBinary(TString hexStr)` | `CBinary` | 十六进制字符串→Binary |

---

## 5. CDevEnvironment — 设备环境 (devEnvironment.h)

全 static，不可实例化。提供设备/APP能力查询。

### 设备信息键值枚举 eDeviceInfoKey
| 枚举值 | 含义 |
|--------|------|
| `KEY_OS_VERSION=0` | 操作系统版本 |
| `KEY_PKG_VERSION=1` | 包版本 |
| `KEY_PKG_NAME=2` | 包名 |
| `KEY_DEVICE_NAME=3` | 设备名称 |
| `KEY_UI_VERSION=4` | UI版本 |
| `KEY_APP_VERSION=5` | APP版本 |
| `KEY_VCI_VERSION=6` | VCI版本 |
| `KEY_VCI_TYPE=7` | VCI类型 |
| `KEY_DEVICE_SN=8` | 设备序列号 |
| `KEY_APP_VERSION_CODE=11` | APP版本号 |

### 功能支持查询（全部返回 bool）

| 方法 | 说明 |
|------|------|
| `IsBenzProgramSupported()` | 奔驰编程/在线设码功能 |
| `IsImmoKeyProgramSupported()` | 防盗钥匙编程 |
| `IsNetworkSwitchSupported()` | 网络切换（DoIP用） |
| `IsSpecOptimizeSupported()` | 十大特殊功能优化 |
| `IsLoggingInstrumentationSupported()` | 诊断日志采集 |
| `IsDensoFunctionSupported()` | Denso相关功能 |
| `IsImageBoxSupported()` | 图片弹窗 |
| `IsTopoTestExtListSupported()` | 拓扑测试扩展列表 |
| `IsCameraSupported()` | 摄像头 |
| `IsBasicLoginSupported()` | 基础登录 |
| `IsMenuV2Supported()` | 多级菜单页面 |
| `IsTPMSMenuV2Supported()` | 胎压管理V2 |
| `IsNastfSupported()` | NASTF功能 |
| `IsAnnualInspectionSupported()` | 年检功能 |
| `IsInfotechInspectSupported()` | Infotech一键检测 |
| `IsVWSFDUnlockChargingSupported()` | 大众SFD付费解锁 |
| `IsVciDPDUSupported()` | VCI D-PDU支持 |
| `IsVciSDRAMSupported()` | VCI SDRAM支持 |
| `IsVciMultiLinkSupported()` | VCI多路CAN通信 |
| `IsVciLinkFilterSupported()` | VCI链路过滤 |

### 设备信息获取

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `GetDeviceInfoByKey(eDeviceInfoKey key)` | `string` | 获取设备信息 |
| `GetDeviceRegionCode()` | `string` | 国家/地区代码 |
| `GetDeviceUserName()` | `string` | 注册用户名 |

---

## 6. 加密解密 (encdec.h)

| 函数 | 说明 |
|------|------|
| `CalcKey(TString strSerialNo)` → TString | 根据序列号计算密钥 |
| `_SeqEncDec(UINT key, void* sn, int len, BYTE flag)` | 序列加解密（0=加密, 1=解密） |
| `_SeqDecrypt(key, sn, len)` | 解密宏 |
| `_SeqEncrypt(key, sn, len)` | 加密宏 |

---

## 7. 度量单位 (metric.h)

| 函数 | 说明 |
|------|------|
| `GetMetricIndex(TString strUnit)` → BYTE | 获取单位度量索引 |
| `MetricTanslate(BYTE metric, TString& val, TString& unit)` | 公制/英制转换（同时转值和单位） |
| `MetricTanslateUnitOnly(BYTE metric, TString& unit)` | 仅转换单位 |
| `GetMetricValue(BYTE metric)` → TString | 获取度量值 |

---

## 8. 工具函数 (utils.h)

| 函数 | 说明 |
|------|------|
| `Delay(UINT ms)` | 延时（毫秒） |
| `Clock()` → UINT | 获取时钟值 |
| `GetSystemCurrentTime()` → string | 获取当前系统时间（_COCOS） |
| `GetSystemLocalTime()` → string | 获取本地时间（_COCOS） |
| `FixFilePath(const string& path)` → string | 修正文件路径（_COCOS） |
| `IsValidVin(TString vin, BOOL isCheck)` → BOOL | VIN码校验（_COCOS） |
| `CalcAlgorithmDynamicLibraryValue(filepath, src, len, des, maskH, maskL, level)` → int | 动态库算法计算（_COCOS） |
| `CalcCheckDynamicLibraryValue(filepath, addr, len, src, des)` → int | 动态库校验计算（_COCOS） |

---

## 9. CExcelFile — 表格数据文件 (excel.h)

继承 CBinaryFile。用于读取 Excel 格式的 BIN 数据文件。

| 方法 | 说明 |
|------|------|
| `SearchId(BYTE sheet, UINT id, void* recordset, BOOL quick=FALSE)` → BOOL | 按ID搜索记录 |
| `GetFuncIndex(UINT idm, ST_INDEX* index)` → BOOL | 获取功能索引 |
| `LoadText(DWORD id)` → TString | 加载文本 |
| `LoadStat(DWORD id)` → TString | 加载状态文本 |
| `LoadTable(DWORD id, CSheetTable*)` → BOOL | 加载表格 |
| `LoadField(DWORD id, int index)` → AFX_RET_DATA | 加载字段 |
| `LoadCommand(DWORD id, CSheetCmd*)` → BOOL | 加载命令 |
| `LoadSheet(BYTE sheet)` → BOOL | 加载工作表 |
| `SetExcelId(UINT)` / `GetExcelId()` | 设置/获取Excel ID |

全局变量：`g_rf`(CReceiveFrame), `g_set`(CSheetSet), `g_file`(CExcelFile), `g_dtc`(CBinary), `g_input`(CInputValue)

---

## 10. 典型使用示例

### JSON构建
```cpp
CJsonBuilder json;
json.StartObject();
json.AddString("vin", "WDB9066571S123456");
json.AddInt("ecuId", 0xE001);
json.StartArray("dtcList");
json.AddString("P0100");
json.AddString("P0200");
json.EndArray();
json.EndObject();
std::string result = json.GetJsonString();
```

### 数据转换
```cpp
CBinary bin = CDataConvertProcess::HexStrToBinary("22F190");
TString hex = CDataConvertProcess::BinaryToString(bin);  // "22F190"
DWORD val = CDataConvertProcess::StrToUInt("0xFF", 16);  // 255
```

### 设备能力查询
```cpp
if (CDevEnvironment::IsBenzProgramSupported()) {
    // 执行在线设码
}
std::string sn = CDevEnvironment::GetDeviceInfoByKey(CDevEnvironment::KEY_DEVICE_SN);
```

### 度量转换
```cpp
TString val = "100";
TString unit = "km/h";
BYTE metric = CConfig::GetMetric();
MetricTanslate(metric, val, unit);  // 英制时转换为 mph
```
