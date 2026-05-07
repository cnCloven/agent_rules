# 显示系统 API (disp.h)

> 头文件: `D:\work\platform\inc\disp.h`
> 本文档覆盖菜单、版本信息、故障码、数据流、动作测试、输入输出、列表等 UI 显示类及全局函数。

---

## 按键常量速查

| 常量 | 值 | 说明 |
|------|----|------|
| `KEY_ESC` | 0xFFFC | 返回/退出 |
| `KEY_OK` | 0xFFFA | 确认 |
| `KEY_NONE` | 0xFFF9 | 未按下按钮 |
| `KEY_HELP` | 0xFFF8 | 帮助 |
| `KEY_USER_BTN1` | 0xFFE0 | 自定义按钮1 |
| `KEY_USER_BTN2` | 0xFFE1 | 自定义按钮2 |
| `KEY_NEW_REPORT` | 0xFFE2 | 新报告 |
| `KEY_CDS_SELECTED` | 0xFFED | 数据流选中显示 |
| `KEY_HIDDENFUNC_BYTE` | 0xFFEE | 隐藏功能字节选择 |
| `KEY_HIDDENFUNC_BIT` | 0xFFEF | 隐藏功能位变更 |
| `KEY_ERASEDTC` | 0xFFF1 | 清除故障码 |
| `KEY_READDTC` | 0xFFF2 | 读取故障码 |
| `KEY_FREEZEFRAME` | 0xFFF5 | 冻结帧 |
| `KEY_SHORTTEST` | 0xFFF4 | 快速测试 |
| `KEY_DISPLAYDTC` | 0xFFF7 | 显示故障码 |
| `KEY_HOME` | 0xFFDF | 主页 |
| `KEY_DATA_OVERFLOW` | 0xEEEE | 数据溢出 |

## MessageBox 类型与返回值

**类型常量**:

| 常量 | 值 | 按钮组合 |
|------|----|----------|
| `MB_OK` | 0x00 | 确定 |
| `MB_OKCANCEL` | 0x01 | 确定 + 取消 |
| `MB_YESNO` | 0x04 | 是 + 否 |
| `MB_YESNOCANCEL` | 0x03 | 是 + 否 + 取消 |
| `MB_RETRYCANCEL` | 0x05 | 重试 + 取消 |
| `MB_NEXTCANCEL` | 0x06 | 继续 + 取消 |
| `MB_BACKNEXTCANCEL` | 0x07 | 后退 + 继续 + 取消 |
| `MB_BACKNEXTEXIT` | 0x08 | 后退 + 继续 + 退出 |
| `MB_RETRYEXIT` | 0x09 | 重试 + 退出 |
| `MB_NEXTEXIT` | 0x0A | 继续 + 退出 |
| `MB_NONE` | 0x0F | 无按钮（纯状态显示） |

**返回值**:

| 常量 | 值 |
|------|----|
| `IDOK` | 1 |
| `IDCANCEL` | 2 |
| `IDABORT` | 3 |
| `IDRETRY` | 4 |
| `IDIGNORE` | 5 |
| `IDYES` | 6 |
| `IDNO` | 7 |
| `IDNEXT` | 10 |
| `IDBACK` | 11 |
| `IDEXIT` | 12 |

---

## CMenuShow — 菜单显示

**全局对象**: `MenuShow`（直接使用，无需创建）

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char* title=NULL)` | 初始化（C字符串标题） | title: 标题文本 |
| `Init(TString title)` | 初始化（TString标题） | — |
| `Init(CBinary idTitle)` | 初始化（文本ID标题） | idTitle: XX_text.bin 中的索引ID |
| `Add(TString text, UINT id=0xFFFFFFFF)` | 添加菜单项 | text: 显示文本; id: 自定义项ID（省略则自动递增从0开始） |
| `Add(CBinary idItem, UINT id=0xFFFFFFFF)` | 添加菜单项（文本ID） | idItem: XX_text.bin 中的索引ID |
| `Show(UINT& selected)` → `UINT` | 显示菜单并等待选择 | selected: [out] 用户选中项的ID |
| `Show(WORD& selected)` → `WORD` | 同上（WORD版本） | 返回值: KEY_ESC=退出, KEY_NONE=未选择 |

### 典型用法

**标准菜单循环**（最常用模式）:

```cpp
MenuShow.Init("诊断菜单");
MenuShow.Add("读取版本");    // id=0（自动）
MenuShow.Add("读取故障码");  // id=1
MenuShow.Add("数据流");      // id=2
WORD nSelect = 0;

while (TRUE) {
    WORD nRet = MenuShow.Show(nSelect);
    if (KEY_ESC == nRet) break;
    if (KEY_NONE == nRet) continue;
    switch (nSelect) {
        case 0: /* 读取版本 */ break;
        case 1: /* 读取故障码 */ break;
        case 2: /* 数据流 */ break;
    }
}
```

**固定ID菜单**（菜单项ID不连续时）:

```cpp
MenuShow.Init("选择ECU");
MenuShow.Add("发动机", 0x10);
MenuShow.Add("变速箱", 0x20);
WORD nSelect = 0;

while (TRUE) {
    WORD nRet = MenuShow.Show(nSelect);
    if (KEY_ESC == nRet) break;
    if (KEY_NONE == nRet) continue;
    // nSelect 为 0x10/0x20，而非 0/1
    if (0x10 == nSelect) { /* 发动机 */ }
}
```

---

## CVehicleInfo — 版本信息显示

**全局对象**: `VehicleInfo`（直接使用）

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char* title=NULL)` | 初始化 | — |
| `Init(TString title)` / `Init(CBinary idTitle)` | 初始化重载 | — |
| `Add(TString explain, TString value)` | 添加版本信息条目 | explain: 名称, value: 值 |
| `Add(CBinary idExplain, TString value)` | 同上（名称用文本ID） | — |
| `Add(CBinary idExplain, CBinary idValue)` | 同上（均用文本ID） | — |
| `AddChar(CBinary/TString explain, CBinary data, WORD index, SHORT count)` | 从回复数据中提取ASCII字符 | index: 起始位, count: 字节数（负数为反向取）, 长度不超过1024 |
| `AddInt(CBinary/TString explain, CBinary data, WORD index, SHORT count)` | 从回复数据中提取十进制数 | 不超过16位数 |
| `AddHex(CBinary/TString explain, CBinary data, WORD index, SHORT count)` | 从回复数据中提取十六进制 | 以%.2X格式, 不超过512字节 |
| `SetButton(BYTE nButton, TString text)` | 设置自定义按钮 | nButton: BTN_USER1(1)/BTN_USER2(2), 最多2个 |
| `EnableKeyOk(BOOL isEnable)` | 使能确认按钮 | TRUE: 显示确定+取消, FALSE: 仅显示确定(返回KEY_ESC) |
| `SetExFuncBtnType(WORD nType)` | 设置扩展功能按钮 | nType: DEFAULT_TYPE(0)/IDENTIFIX_TYPE(1) |
| `GetCurSel()` → `SHORT` | 获取当前选中位置 | — |
| `Show(BOOL bUserClick=FALSE)` → `WORD` | 显示界面 | bUserClick: TRUE=点击条目返回下标; 返回: KEY_ESC/KEY_USER_BTN1/BTN2 |
| `GetCount()` → `int` | 获取条目数量 | — |

### 典型用法

```cpp
VehicleInfo.Init("ECU版本信息");
VehicleInfo.Add("VIN", "12345678901123456");
VehicleInfo.Add("硬件版本", "DEV-ECU");
VehicleInfo.Add("软件版本", "P547V1037");

// 从通信回复中提取版本信息
CBinary binData = CBinary("\x62\xF1\x88\x31\x32\x33", 6);
VehicleInfo.AddChar("软件号", binData, 3, 3);  // 从第3字节开始取3个字节的ASCII

VehicleInfo.SetButton(CVehicleInfo::BTN_USER1, "刷新");

WORD wKey = 0;
while (TRUE) {
    wKey = VehicleInfo.Show();
    if (KEY_ESC == wKey) break;
    if (KEY_USER_BTN1 == wKey) { /* 刷新操作 */ }
}
```

---

## CTroubleCode — 故障码显示

**全局对象**: `TroubleCode`（直接使用）

### 按钮枚举

| 枚举 | 值 | 说明 |
|------|----|------|
| `BTN_HELP` | 1 | 帮助按钮 |
| `BTN_ERASEDTC` | 2 | 清码按钮 |
| `BTN_FREEZEFRAME` | 4 | 冻结帧按钮 |
| `BTN_USER1` | 8 | 自定义按钮1 |
| `BTN_USER2` | 0x10 | 自定义按钮2 |
| `BTN_NEWREPORT` | 0x20 | 诊断报告按钮 |

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `Add(CBinary id, TString status="")` | 按数据库索引添加故障码 | id: 故障码索引, status: 状态文本 |
| `Add(CBinary id, CBinary idStatus)` | 同上（状态用文本ID） | — |
| `Add(CBinary id, BYTE nStatus)` | 同上（状态用字节值） | — |
| `Add(UINT id, TString status="", WORD nDtcLib=0xFFFF)` | 按UINT索引添加 | — |
| `Add(CBinary id, TString code, TString text, TString status="")` | 手动指定码号和描述 | code: "P0001", text: 故障描述 |
| `AddAttr(CBinary id, CBinary/BYTE status)` | 为已有故障码追加属性 | — |
| `SetHelp(CBinary id, TString help="")` | 设置帮助信息 | help: 帮助文本; 也可由*_DTCH.txt自动配置 |
| `SetCustom(callback)` | 注册未定义故障码处理回调 | callback: `TString(*)(CBinary)` |
| `SetButton(BYTE btn, TString text="")` | 设置按钮 | btn: BTN_XXX枚举 |
| `SetButton(BYTE btn, CBinary idText)` | 同上（文本ID版） | — |
| `SetButtonMask(CBinary id, BYTE btn, BOOL disable=TRUE)` | 设置指定故障码的按钮掩码 | disable: TRUE=置灰, FALSE=置亮 |
| `EnableFlag(BOOL bEnable)` | 允许/禁止添加未定义故障码 | — |
| `SetSupportNewReport(BOOL bDisable=FALSE)` | 设置是否支持诊断报告 | TRUE: 支持 |
| `GetCount()` → `int` | 获取故障码数量 | — |
| `GetTroubleCode(SHORT index=-1)` → `CBinary` | 获取当前/指定故障码ID | -1: 当前 |
| `GetCurSel()` → `SHORT` | 获取当前选择索引 | — |
| `CodeToPCBU(BYTE high, BYTE low)` → `TString` | 静态: 数值转PCBU码 | — |
| `Show()` → `WORD` | 显示故障码界面 | 返回: KEY_ESC/KEY_ERASEDTC/KEY_FREEZEFRAME/KEY_NEW_REPORT |

**公开成员**: `m_vsTroubleCode` (CGroup\<tagTroubleCode\>) — 故障码数据列表

### 典型用法

**标准故障码显示**:

```cpp
TroubleCode.Init("发动机故障码");
TroubleCode.Add(CBinary("\x00\x00", 2), "P0001", "信号传感器故障", "激活");
TroubleCode.Add(CBinary("\x00\x01", 2), "C0001", "转向角传感器未匹配", "非激活");

TroubleCode.SetHelp(CBinary("\x00\x00", 2), "检查发动机"); // ID需与Add时一致

WORD nKey;
while (TRUE) {
    nKey = TroubleCode.Show();
    if (KEY_ESC == nKey) break;
}
```

**带清码和冻结帧**:

```cpp
TroubleCode.Init();
TroubleCode.Add(CBinary("\x00\x00", 2), "P0001", "故障描述", "激活");

TroubleCode.SetButton(CTroubleCode::BTN_ERASEDTC, "清码");
TroubleCode.SetButton(CTroubleCode::BTN_FREEZEFRAME, "读冻结帧");
// 控制哪些故障码可以读冻结帧
TroubleCode.SetButtonMask(CBinary("\x00\x00", 2), CTroubleCode::BTN_FREEZEFRAME, FALSE); // FALSE=可点击

while (TRUE) {
    nKey = TroubleCode.Show();
    if (KEY_ESC == nKey) break;
    else if (KEY_ERASEDTC == nKey) { /* 执行清码 */ }
    else if (KEY_FREEZEFRAME == nKey) { /* 读取冻结帧 */ }
}
```

**未定义故障码回调**:

```cpp
TroubleCode.EnableFlag(TRUE);  // 允许未定义故障码
TroubleCode.SetCustom(MyCodeCallback);

// 回调函数 — 为未定义的故障码生成码号
TString MyCodeCallback(CBinary idTroubleCode) {
    return "C0001";
}
```

---

## CTroubleList — 故障信息列表

**全局对象**: `TroubleList`（直接使用）

与 `CTroubleCode` 类似，但使用纯文本添加条目（不依赖数据库索引）。

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `Add(TString text, BYTE status, TString help="")` | 添加故障信息条目 | text: 故障文本, status: 状态值 |
| `SetButton(BYTE btn, TString text="")` | 设置按钮 | btn: BTN_HELP/BTN_ERASEDTC/BTN_FREEZEFRAME/BTN_USER1/BTN_USER2 |
| `SetButtonMask(WORD index, BYTE btn, BOOL disable=TRUE)` | 设置条目按钮掩码 | index: 条目索引 |
| `GetCount()` → `int` | 获取数量 | — |
| `GetCurSel()` → `SHORT` | 获取当前选择 | — |
| `Show()` → `WORD` | 显示界面 | — |

---

## CMultiSelect — 多选数据流

**全局对象**: `MultiSelect`（直接使用）

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `SetFile(TString file)` | 设置MDB中Bin文件名 | — |
| `Add(CBinary id, CBinaryGroup* items=NULL)` | 按ID添加数据流 | — |
| `Add(TString item)` | 按文本添加 | — |
| `Add(CBinaryGroup& group)` | 批量添加 | — |
| `AddGroup(CBinary idGroup, BYTE flag)` | 添加分组 | flag: DSF_STREAM/DSF_GROUP |
| `SetMaxSelectedNumber(WORD max)` | 设置最大可选数量 | — |
| `Show()` → `WORD` | 显示选择界面 | 返回: KEY_OK=确认选择, KEY_ESC=取消 |
| `GetDataStream()` → `CBinaryGroup&` | 获取选中的数据流 | — |
| `GetInternalOrder()` → `CGroup<WORD>&` | 获取选中顺序 | — |
| `IsSelected(int index)` → `BOOL` | 查询某项是否被选中 | — |
| `GetItemNumber()` → `int` | 获取总项数 | — |
| `GetItemText(int index)` → `TString` | 获取指定项文本 | — |

---

## CDataStream — 数据流显示

**全局对象**: `DataStream`（直接使用）
**继承关系**: `CDataStream` 是 `CActiveTest` 和 `CSpecialTest` 的基类

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| **初始化** | | |
| `Init(const char* title=NULL, BYTE flag=DS_NORMAL)` | 初始化 | flag: DS_NORMAL/DS_VW |
| `Init(TString/CBinary title, BYTE flag=DS_NORMAL)` | 初始化重载 | — |
| `SetNewUI(BOOL bNew=TRUE)` | 启用新版UI | — |
| `SetFile(TString file)` | 设置MDB中Bin文件名 | — |
| **添加数据流** | | |
| `Add(CBinary id, CBinaryGroup* items=NULL)` | 按ID添加 | id: 6字节数据流索引 |
| `Add(CBinaryGroup& group)` | 批量添加 | — |
| `Add(TString name, TString value="", TString unit="")` | 按名称添加 | — |
| `Add(CBinary id, TString value, TString unit="")` | 按ID添加（带初始值） | — |
| `Add(UINT id, BYTE sheet)` | 按UINT索引添加 | — |
| `AddGroup(CBinary idGroup, BYTE flag)` | 添加分组 | flag: DSF_STREAM/DSF_GROUP |
| **值操作** | | |
| `SetValue(TString name, TString value, TString unit="")` | 按名称设值 | — |
| `SetValue(CBinary id, TString value, TString unit="")` | 按ID设值 | — |
| `SetReferenceValue(CBinary id, TString value, TString min="", TString max="", TString unit="")` | 设参考值范围 | — |
| `SetName(CBinary id, TString text)` | 修改显示名称 | — |
| **查询** | | |
| `GetDataStream(SHORT index=-1)` → `CBinary` | 获取指定索引的数据流ID | -1: 当前 |
| `GetCurrentIndex(CBinary* id)` → `WORD` | 获取ID对应的索引 | — |
| `GetCurrentRange(WORD& top, WORD& bottom)` | 获取当前可视范围索引 | [out] top/bottom |
| `GetCurSel()` → `SHORT` | 获取当前选中索引 | — |
| `GetCount()` → `WORD` | 数据流总数 | — |
| **计算** | | |
| `SetCustom(callback)` | 注册自定义计算回调 | callback: `TString(*)(CBinary, CReceiveFrame&)` |
| `Calc(CBinary id, CReceiveFrame& rf)` → `TString` | 用数据流库公式计算值 | — |
| `Calc(CBinary id, CBinary& data)` → `TString` | 同上（一维数组版） | — |
| `IsExpressValid(CBinary id)` → `BOOL` | 检查算法公式是否有效 | — |
| `GetCommand(CBinary id)` → `CSendFrame` | 读取数据流库中的发送命令 | — |
| **按钮/显示** | | |
| `SetButton(BYTE btn, TString text="")` | 设置按钮 | btn: BTN_HELP(1)/BTN_USER1(2)/BTN_USER2(4) |
| `Show(BOOL bWait=FALSE)` → `WORD` | 显示并等待操作 | 返回: KEY_ESC/KEY_NONE/KEY_OK/KEY_CDS_SELECTED/KEY_USER_BTNx |
| `RemoveDatastream()` | 清空所有数据流 | — |
| `AutoStep()` → `BOOL` | 自动步进 | — |
| `AutoScroll(int focus=-2)` | 自动滚动 | — |

**关键公开成员**:
- `m_vsDataStream` (CGroup\<tagDataStream\>) — 数据流列表
- `m_vsSelectedDS` (CBinaryGroup) — 用户选中的数据流
- `m_vsSelectedDSIndex` (CGroup\<WORD\>) — 用户选中的数据流索引列表

### 典型用法

**标准数据流显示循环**:

```cpp
DataStream.Init("发动机数据流");
DataStream.SetNewUI();

CBinary binId("\x48\x00\x00\x00\x00\x01", 6);
for (int i = 1; i <= 0x1C; i++) {
    binId.SetAt(5, i);
    DataStream.Add(binId, "");
}

WORD ntop = 0, nBottom = 0;
while (TRUE) {
    // 仅刷新可见范围（性能优化关键）
    DataStream.GetCurrentRange(ntop, nBottom);
    for (int i = ntop; i < nBottom; i++) {
        CBinary id = DataStream.GetDataStream(i);
        TString value = /* 从ECU读取并计算 */;
        DataStream.SetValue(id, value);
    }

    WORD ret = DataStream.Show();
    if (ret == KEY_ESC) break;
    if (ret == KEY_CDS_SELECTED) {
        // 用户点了"选中显示"，可通过 m_vsSelectedDSIndex 获取选中项
    }
}
```

**自定义计算回调**（数据流库无公式时）:

```cpp
DataStream.SetCustom(MyCalcFunc);

// 回调函数 — 当 Calc() 找不到数据流库公式时调用
TString MyCalcFunc(CBinary idDataStream, CReceiveFrame& rf) {
    if (rf.IsEmpty()) return "";
    return rf[0].ToString();
}
```

**自定义按钮**:

```cpp
DataStream.Init();
DataStream.SetNewUI();
DataStream.SetButton(0x02, "btn2");  // BTN_USER1
DataStream.SetButton(0x04, "btn3");  // BTN_USER2

// ...添加数据流...

WORD ret = DataStream.Show();
if (KEY_USER_BTN1 == ret) { /* btn2被按下 */ }
if (KEY_USER_BTN2 == ret) { /* btn3被按下 */ }
```

---

## CBatteryData — 电池包数据流

**全局对象**: `BatteryData`（直接使用）
**继承**: `CBatteryData` 继承自 `CDataStream`

### 按钮状态枚举 (eButtonStatus)

| 枚举 | 值 | 说明 |
|------|----|------|
| `BUTTON_NONE` | -1 | 无效按钮（查询不到时返回） |
| `BUTTON_DISABLE` | 0 | 按钮显示但禁用 |
| `BUTTON_ENABLE` | 1 | 按钮显示且可点击 |
| `BUTTON_HIDE` | 2 | 按钮隐藏 |

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| **电压相关** | | |
| `SetVoltageTitle(TString title)` | 设置电压页标题 | — |
| `AddVoltage(CBinary id, TString value="")` | 添加电压数据流 | — |
| `AddVoltage(TString name, TString value="")` | 同上（按名称） | — |
| `GetVoltageSize()` → `WORD` | 获取电压数量 | — |
| `SetVoltageValue(CBinary/TString/WORD, TString value)` | 设置电压值 | — |
| `SetVoltageRange(TString min, TString max)` | 设置电压范围 | — |
| `SetVoltageGroup(CGroup<CGroup<WORD>>& group)` | 设置电压分组 | — |
| `SetVoltageGroup(CBinary/TString/WORD, WORD group)` | 设置单体分组 | — |
| **温度相关** | | |
| `SetTemperatureTitle(TString title)` | 设置温度页标题 | — |
| `AddTemperature(CBinary/TString, TString value="")` | 添加温度数据流 | — |
| `GetTemperatureSize()` → `WORD` | 获取温度数量 | — |
| `SetTemperatureValue(CBinary/TString/WORD, TString value)` | 设置温度值 | — |
| `SetTemperatureRange(TString min, TString max)` | 设置温度范围 | — |
| `SetTemperatureGroup(...)` | 设置温度分组（同电压） | — |
| **总体信息** | | |
| `SetTotalBattery(WORD count)` | 设置电池总数 | — |
| `SetTotalCurrent(TString current)` | 设置总电流 | — |
| `SetTotalVoltage(TString volt)` | 设置总电压 | — |
| `SetDifferenceVoltage(TString diff)` | 设置压差 | — |
| `SetMaxVoltage(TString)` / `SetMinVoltage(TString)` | 设置最大/最小电压 | — |
| `SetSOC(TString value)` / `SetSOH(TString value)` | 设置SOC/SOH | — |
| `GetSOC()` / `GetSOH()` → `TString` | 获取SOC/SOH | — |
| **动态分析** | | |
| `SetUiType(BYTE type)` | 设置UI类型 | UI_DATA_STREAM(0)/UI_DYNAMIC_ANALYSIS(1) |
| `StartDynamicData()` / `StopDynamicData()` | 开始/停止动态数据采集 | — |
| `GetDynamicStatus()` → `BYTE` | 获取动态状态 | — |
| `SetDynamicVoltage(...)` | 设置动态电压值 | — |
| **自定义按钮** | | |
| `AddButton(TString text, WORD id=0xFFFF)` | 添加自定义按钮 | id: 按钮ID（也是返回值） |
| `SetButtonText(WORD id, TString text)` | 修改按钮文本 | — |
| `SetButtonStatus(WORD id, eButtonStatus status)` | 设置按钮状态 | — |
| `IsButtonExist(WORD id)` → `bool` | 按钮是否存在 | — |
| `DeleteButton(WORD id)` | 删除按钮 | — |
| `ClearButtons()` | 清除所有自定义按钮 | — |
| **其他** | | |
| `SetBatteryVolDivisor(DWORD divisor)` | 设置总电压分隔数量 | — |
| `SetDivisorBubbleTips(TString tips)` | 设置关键提示信息 | — |
| `Show(BOOL bWait=FALSE)` → `WORD` | 显示界面 | 返回: KEY_ESC/KEY_NONE/KEY_OK/按钮ID |

---

## CActiveTest — 动作测试

**全局对象**: `ActiveTest`（直接使用）
**继承**: `CActiveTest` 继承自 `CDataStream`（可使用数据流的 Add/SetValue/GetDataStream 等方法）

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `AddButton(TString text, WORD id=0xFFFF)` | 添加动作按钮 | id: 按钮ID（也是Show的返回值），省略则自动递增 |
| `AddButton(CBinary idText, WORD id=0xFFFF)` | 同上（文本ID版） | — |
| `EnableButton(WORD id, BOOL bEnable)` | 设置按钮使能/禁用 | — |
| `SetButtonStatus(WORD id, BYTE status)` | 设置按钮状态 | 0=禁用, 1=可用 |
| `SetButtonText(WORD id, TString/CBinary text)` | 修改按钮文本 | — |
| `SetNewQuickTest(BOOL bFlag)` | 设置新版UI | — |
| `SetSysStatus(CBinary id, BYTE status)` | 设置系统状态 | — |
| `SetCurStatus(BYTE status)` | 设置当前状态 | — |
| `SaveCurSysDtc(WORD index, CGroup<tagOneDtc>& dtc)` | 保存当前系统故障码 | — |
| `Show(BOOL bWait=FALSE)` → `WORD` | 显示界面 | 返回: KEY_ESC/KEY_NONE/按钮ID |

### 典型用法

```cpp
ActiveTest.Init("超速设定阈值");
ActiveTest.Add("发动机转速", "0", "rpm");  // 继承自CDataStream的Add
ActiveTest.AddButton("写入", 1);
ActiveTest.AddButton("开始执行", 2);
ActiveTest.EnableButton(1, FALSE);  // 初始禁用"写入"

while (TRUE) {
    CBinary id = ActiveTest.GetDataStream();
    ActiveTest.SetValue(id, /* 实时值 */);
    ActiveTest.SetCurStatus(TRUE);

    WORD nKey = ActiveTest.Show();
    if (KEY_ESC == nKey) break;
    else if (2 == nKey) {
        // "开始执行"被按下
        ActiveTest.EnableButton(1, TRUE);   // 启用"写入"
        ActiveTest.EnableButton(2, FALSE);  // 禁用"开始"
    }
    else if (1 == nKey) {
        // "写入"被按下
    }
}
```

---

## CSpecialTest — 特殊功能测试

**全局对象**: `SpecialTest`（直接使用）
**继承**: `CSpecialTest` 继承自 `CActiveTest`（可使用其全部方法）

### 额外接口

| 方法 | 功能 |
|------|------|
| `Init(const char*/TString/CBinary)` | 初始化 |
| `SetPromptText(TString text)` | 设置文本框提示内容（支持\n换行） |
| `SetPromptText(CBinary idText)` | 同上（文本ID版） |
| `Show(BOOL bWait=FALSE)` → `WORD` | 显示界面 |

### 典型用法

```cpp
SpecialTest.Init("DPF再生");
SpecialTest.Add("发动机转速", "650", "rpm");
SpecialTest.Add("冷却液温度", "40", "℃");
SpecialTest.AddButton("激活", 0);
SpecialTest.AddButton("停止", 1);
SpecialTest.SetPromptText("测试条件：\n1.请启动发动机>10s;\n2.冷却液温度>40℃");

while (TRUE) {
    WORD nKey = SpecialTest.Show();
    if (KEY_ESC == nKey) break;
    else if (0 == nKey) { /* 激活 */ }
    else if (1 == nKey) { /* 停止 */ }
    SpecialTest.EnableButton(!nKey, TRUE);
    SpecialTest.EnableButton(nKey, FALSE);
}
```

---

## CShortTest — 快速测试

**全局对象**: `ShortTest`（直接使用）

### 按钮枚举

| 枚举 | 值 | 说明 |
|------|----|------|
| `BTN_QUICKERASE` | 1 | 快速清码 |
| `BTN_DISPLAYDTC` | 2 | 显示故障码 |
| `BTN_DIAGNOSTIC` | 4 | 诊断 |

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `Add(TString text, UINT id=0xFFFFFFFF)` | 添加显示项 | — |
| `Add(CBinary id, UINT nId=0xFFFFFFFF)` | 同上（文本ID版） | — |
| `Add(TString text, TString value)` | 添加带值的项 | — |
| `SetName(TString/CBinary)` | 设置当前项名称 | — |
| `SetValue(TString/CBinary)` | 设置当前项值 | — |
| `SetButton(BYTE btn)` | 设置按钮组合 | btn: BTN_XXX 按位或组合 |
| `GetCurId()` → `UINT` | 获取当前选中ID | — |
| `AutoStep(WORD key)` | 自动步进 | — |
| `Show()` / `Show2()` → `WORD` | 显示界面 | — |

---

## 输入类

### CMultInput — 多输入

**全局对象**: `MultInput`（直接使用）

**输入类型标志 (chFlag)**:

| 标志 | 说明 |
|------|------|
| `'N'` | 数字键盘 |
| `'X'` | 十六进制 |
| `'C'` | 字母 |
| `'V'` | 任意字符 |
| `'U'` | 大写+数字 |
| `'L'` | 小写+数字 |
| `'F'` | 浮点数 |
| `0` (数值) | 不允许编辑 |

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `Add(TString explain, TString value, char flag='N', const char* default=NULL)` | 添加输入框 | value: 初始值（支持\|分隔下拉选项）|
| `Add(CBinary idExplain, TString value, char flag='N', const char* default=NULL)` | 同上（文本ID版） | — |
| `SetPromptText(TString/CBinary)` | 设置提示信息 | — |
| `Show()` → `CInputValue` | 显示并等待输入 | — |

### CFormInput — 表单输入

**全局对象**: `FormInput`（直接使用）

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `AddInput(TString explain, TString value, char flag='V', const char* default=NULL, BOOL required=TRUE)` | 添加输入框 | required: 是否必填 |
| `AddChoice(TString explain, TString value, const char* default=NULL, BOOL required=TRUE)` | 添加选择框 | value: 选项用\|分隔 |
| `SetPromptText(TString/CBinary)` | 设置提示信息 | — |
| `Show()` → `CInputValue` | 显示并等待输入 | — |

### CSpecialInput — 特殊输入

**全局对象**: `SpecialInput`（直接使用）

| 方法 | 功能 |
|------|------|
| `Init(const char*/TString/CBinary)` | 初始化 |
| `SetMode(BYTE mode)` | 设置模式 |
| `Add(TString explain, TString value, char flag='N', ...)` | 添加输入框 |
| `SetPromptText(TString/CBinary)` | 设置提示文本 |
| `SetPicture(TString picFile)` | 设置图片路径 |
| `SetNote(TString/CBinary)` | 设置注意信息 |
| `Show()` → `CInputValue` | 显示并等待输入 |

### CProgInput — 编程输入

**全局对象**: `ProgInput`（直接使用）

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `Add(TString explain, TString value, TString button, char flag='N')` | 添加输入项（带按钮） | button: 按钮文本 |
| `SetValue(TString explain, TString value)` | 设置指定项的值 | — |
| `SetButton(TString explain, TString button)` | 设置指定项的按钮文本 | — |
| `Show()` → `CInputValue` | 显示并等待输入 | — |

### CInputValue — 输入返回值类

`Show()` 方法返回此类，用于获取用户输入结果。

| 方法 | 功能 |
|------|------|
| `GetKey()` → `WORD` | 获取按键值 (KEY_ESC=返回, KEY_OK=确认) |
| `GetInt(int index=0)` → `int` | 获取第N个输入的整数值 |
| `GetFloat(int index=0)` → `double` | 获取浮点值 |
| `GetString(int index=0)` → `TString` | 获取字符串值 |
| `GetBinary(int index=0)` → `CBinary` | 获取二进制值 |
| `GetHex(int index=0)` → `DWORD` | 获取十六进制值 |
| `GetIndex(int index=0)` → `int` | 获取选择索引 |
| `GetCount()` → `int` | 获取输入项数量 |

### 典型用法

**多输入框**:

```cpp
MultInput.Init("车辆标定参数");
MultInput.Add("VIN", "12345678012345678|54321", 'N');  // |分隔=下拉选项
MultInput.Add("硬件号", "P1532V1023", 'X');
MultInput.Add("客户ID", "abcdefg", 'C');
MultInput.SetPromptText("请输入标定参数");

while (TRUE) {
    CInputValue value = MultInput.Show();
    if (value.GetKey() == KEY_ESC) break;
    for (int i = 0; i < value.GetCount(); i++) {
        TString str = value.GetString(i);
    }
    break;
}
```

**表单输入**:

```cpp
FormInput.Init("车辆信息");
FormInput.AddChoice("车型", "福田|江淮|重汽", "", TRUE);
FormInput.AddChoice("年款", "2022|2021|2020", "", TRUE);
FormInput.AddInput("备注", "", 'V', "", FALSE);  // 非必填

while (TRUE) {
    CInputValue value = FormInput.Show();
    if (value.GetKey() == KEY_ESC) break;
    // 处理输入结果
    break;
}
```

---

## CHiddenFunc — 刷隐藏功能

**全局对象**: `HiddenFunc`（直接使用）

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `SetCodeInfo(TString prompt, CBinary srcCode)` | 设置原始编码信息 | prompt: 提示文本, srcCode: 原始编码数据 |
| `SetByteCode(CBinary byteCode)` | 设置当前字节编码 | — |
| `SetByteRange(WORD start, WORD length=1)` | 设置可操作的字节范围 | — |
| `GetSelectedByteIndex()` → `WORD` | 获取当前选中字节索引 | Show返回KEY_HIDDENFUNC_BYTE时调用 |
| `AddBitCheck(TString name, TString desc, BOOL checked=FALSE, WORD id=0xFFFF)` | 添加勾选项 | — |
| `AddBitDropDown(TString name, CGroup<TString> list, WORD default=0, WORD id=0xFFFF)` | 添加下拉框项 | — |
| `EnableBit(WORD id, BOOL bEnable)` | 启用/禁用位项 | — |
| `GetChangedBitId()` → `WORD` | 获取变更的位ID | Show返回KEY_HIDDENFUNC_BIT时调用 |
| `GetBitValue(WORD id)` → `WORD` | 获取位值 | CheckBox: 0/1; DropDown: 选项索引 |
| `SetPromptText(TString/CBinary)` | 设置提示文本 | — |
| `AddButton(TString/CBinary text, WORD id=0xFFFF)` | 添加按钮 | — |
| `EnableButton(WORD id, BOOL bEnable)` | 启用/禁用按钮 | — |
| `DeleteButton(WORD id)` | 删除按钮 | — |
| `SetButtonText(WORD id, TString/CBinary)` | 修改按钮文本 | — |
| `Show()` → `WORD` | 显示界面 | 返回: KEY_ESC/KEY_HIDDENFUNC_BYTE/KEY_HIDDENFUNC_BIT/按钮ID |

---

## 列表与网格类

### CGridList — 三列网格列表

**全局对象**: `GridList`（直接使用）

| 方法 | 功能 |
|------|------|
| `Init(const char*/TString/CBinary)` | 初始化 |
| `Add(TString item1, TString item2, TString item3)` | 添加三列数据行 |
| `Show()` → `WORD` | 显示 |

### CUserGrid — 用户自定义网格

**全局对象**: `UserGrid`（直接使用）

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `SetColumn(int col, int wid, int align)` | 设置列属性 | col: 列号, wid: 宽度, align: 对齐 |
| `SetItemText(int row, int col, TString text)` | 设置单元格文本 | — |
| `GetItemText(int row, int col)` → `TString` | 获取单元格文本 | — |
| `SetOffset(DWORD offset)` | 设置偏移（平台内部使用） | — |
| `SetFlag(BYTE flag)` | 设置标志 | — |
| `EnableIdentifix(bool enable)` | 启用Identifix按钮 | — |
| `Show(WORD& sel)` → `WORD` | 显示并返回选择 | sel: [out] 选中行 |
| `Show()` → `WORD` | 显示（无选择参数） | — |

### CListShow — 通用列表显示

**全局对象**: `ListShow`（直接使用）

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `SetColumn(int col, int width, TString title="")` | 设置列属性 | col: 列号, width: 宽度, title: 列标题 |
| `SetItemText(int row, int col, TString text)` | 设置单元格文本 | — |
| `AddItem(TString text)` | 添加行（单列） | — |
| `AddButton(TString text, WORD id=0xFFFF)` | 添加按钮 | — |
| `SetButtonText(WORD id, TString text)` | 修改按钮文本 | — |
| `EnableButton(WORD id, BOOL bEnable)` | 启用/禁用按钮 | — |
| `SetButtonStatus(WORD id, BYTE status)` | 设置按钮状态 | 0=禁用, 1=灰色(可用), 2=使用, 3=按压 |
| `SetFlag(BYTE flag)` | 设置标志 | — |
| `GetItemText(int row, int col=0)` → `TString` | 获取文本 | — |
| `Show(WORD& sel)` → `WORD` | 显示并返回选择 | sel: [out] 选中行 |

---

## CSmartEnter — 智能进入

**全局对象**: `SmartEnter`（直接使用）

### 按钮状态枚举

| 枚举 | 值 | 说明 |
|------|----|------|
| `BTNS_HID` | 0 | 不显示按钮 |
| `BTNS_DIS` | 1 | 按钮禁用 |
| `BTNS_BLUE` | 2 | 蓝色按钮 |
| `BTNS_WHITE` | 3 | 白色按钮 |

### 接口速查

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `AddItem(TString flag, TString name, TString status, BYTE btnState=BTNS_HID, TString btn="", DWORD total=0, DWORD current=0)` | 添加进入项 | flag: 图标标识（如"ENG"）, name: 系统名, status: 状态 |
| `SetItemStatus(WORD index, TString status, BYTE btnState=BTNS_HID, TString btn="", DWORD total=0, DWORD current=0)` | 更新项状态 | — |
| `SetItemProgress(WORD index, DWORD total, DWORD current)` | 设置进度 | — |
| `SetItemResult(WORD index, TString result)` | 设置检测结果 | — |
| `SetItemButton(WORD index, BYTE btnState, TString btn="")` | 设置项按钮 | — |
| `SetBottomButton(TString text, BYTE state=BTNS_BLUE)` | 设置底部按钮 | — |
| `EnableBottomButton(BOOL bEnable)` | 启用/禁用底部按钮 | — |
| `SetFlag(BYTE flag)` | 设置标志 | — |
| `Show()` → `WORD` | 显示界面 | 返回: KEY_NONE/KEY_ESC/KEY_OK(底部按钮)/行号(行按钮) |

---

## CGraphList — 图形列表

**全局对象**: `GraphList`（直接使用）

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init(const char*/TString/CBinary)` | 初始化 | — |
| `SetGraphType(BYTE type)` | 设置图形类型 | — |
| `SetListStep(int min, DWORD step, BYTE count)` | 设置列表刻度 | — |
| `AddItem(TString name, BYTE status, DWORD value=0, TString unit="")` | 添加图形项 | status: BTN_NONE/BTN_DISABLE/BTN_NORMAL/BTN_PRESS |
| `SetItemValue(BYTE index, DWORD value)` | 设置项值 | — |
| `SetItemStatus(BYTE index, BYTE status)` | 设置项状态 | — |
| `SetDataStep(int min, DWORD step, BYTE count)` | 设置数据刻度 | — |
| `SetDataValue(TString name, DWORD value, TString unit)` | 设置数据值 | — |
| `SetButtonClear(TString text)` | 设置清除按钮 | — |
| `SetButtonHelp(TString text, TString value)` | 设置帮助按钮 | — |
| `Show(BOOL bWait=FALSE)` → `WORD` | 显示界面 | — |

---

## CVehicleStep — 车辆引导步骤

**全局对象**: `VehicleStep`（直接使用）

| 方法 | 功能 |
|------|------|
| `Init(const char*/TString/CBinary)` | 初始化 |
| `SetType(BYTE type)` | 设置类型 |
| `SetStepName(CStringGroup names)` | 设置步骤名称列表 |
| `SetStepIndex(BYTE index)` | 设置当前步骤索引 |
| `SetPromptText(TString/CBinary)` | 设置提示文本 |
| `SetRPM(TString name, TString value, TString unit, TString min, TString max, TString step="")` | 设置转速显示 |
| `SetRPMValue(TString value)` | 更新转速值 |
| `SetTemperature(...)` | 设置温度显示（参数同RPM） |
| `SetTemperatureValue(TString value)` | 更新温度值 |
| `SetTimeStep(TString name, TString value)` | 设置时间步骤 |
| `SetTestStep(TString name, TString value)` | 设置测试步骤 |
| `Show()` → `WORD` | 显示界面 |

---

## CDisplay 命名空间 — 全局函数

> 命名空间中的函数直接调用，如 `CDisplay::Init()`, `MessageBox(...)`, `StatusBox(...)` 等。
> 注：`MessageBox`、`StatusBox`、`InputBox` 也作为全局函数可不加命名空间前缀直接调用。

### 系统控制

| 函数 | 功能 |
|------|------|
| `CDisplay::Init()` / `CDisplay::Destroy()` | 初始化/销毁显示系统 |
| `CDisplay::SubScanInit()` / `CDisplay::SubScanDestroy()` | 子扫描模式初始化/销毁 |
| `CDisplay::GetAppName()` → `TString` | 获取APP名称 |
| `CDisplay::GetAppVersion()` → `TString` | 获取APP版本 |
| `CDisplay::GetMenuPath()` → `TString` | 获取菜单路径 |
| `CDisplay::SetCommLog(LOG_SW sw)` | 设置通信日志 (LOG_ON/LOG_OFF) |
| `CDisplay::GetFuncSupport(TString func)` → `BYTE` | 查询APP功能支持（单条） |
| `CDisplay::GetFuncSupport(CStringGroup& funcs)` → `CBinary` | 查询APP功能支持（批量） |
| `CDisplay::GetDSNewUISupport()` → `BYTE` | 获取是否支持新版数据流UI (1=支持) |
| `CDisplay::GetNewUiSupport(WORD type)` → `BYTE` | 查询指定UI功能支持 (1=支持) |
| `CDisplay::SetVehicleVinInfo(TString vin, TString vehicleName, TString year="")` → `BOOL` | 设置VIN信息到APP |
| `CDisplay::GetDeviceType()` → `TString` | 获取设备类型 |
| `CDisplay::GetDeviceInfo()` → `TString` | 获取设备信息 |

### 弹窗/输入

| 函数 | 功能 | 关键参数 |
|------|------|----------|
| `MessageBox(TString text, BYTE flag=MB_OK, const char* title=NULL)` → `BYTE` | 消息弹窗 | flag: MB_XXX类型; 返回: IDOK/IDCANCEL等 |
| `StatusBox(TString text, BYTE percent=0, const char* title=NULL)` → `WORD` | 状态提示（支持进度条） | percent: 0-100进度百分比 |
| `InputBox(TString prompt, TString default, char format='N', const char* title=NULL, WORD maxLen=0)` → `CInputValue` | 单行输入框 | format: 'N'/'X'/'C'/'V'/'F'等 |
| `TimeDownBox(TString text, DWORD totalTime=0, const char* title=NULL)` → `WORD` | 倒计时弹窗 | totalTime: 总时间(ms) |

### 菜单树

| 函数 | 功能 |
|------|------|
| `ShowTree(UINT id, BOOL(*fnMenuHandle)(UINT), ...)` | 显示菜单树（回调接收菜单项ID） |
| `ShowTree(UINT id, BOOL(*fnMenuHandle)(CMenuItem*), ...)` | 显示菜单树（回调接收菜单节点） |
| `ControlTree(BYTE code)` | 控制菜单树 (TREE_GO/TREE_STOP) |

### 自动诊断

| 函数 | 功能 |
|------|------|
| `QuickTest(CGroup<CGroupSys*>& sys, callback)` | 快速测试/自动扫描 |
| `TopoTest(CGroup<CGroupSys*>& sys, callback, CTopoItem* topo=NULL)` | 拓扑测试 |
| `TopoTestV2(...)` | 拓扑测试V2（支持扩展列表） |
| `TopoTestWithPrescan(...)` | 带预扫描的拓扑测试 |
| `PickScanSystem(CGroup<CGroupSys*>& sys, CMenuItem* item=NULL)` | 选择扫描系统 |

### 文件/工具

| 函数 | 功能 |
|------|------|
| `SelectFile(TString title, TString path, TString filter, ...)` → `CInputValue` | 文件选择界面 |
| `ShowPicture(TString picFile, TString prompt, BYTE flag=MB_OK, ...)` → `BYTE` | 展示图片 |
| `PromptPage(TString title, BYTE flag, TString prompt, TString note, TString pic="", ...)` → `BYTE` | 提示页面（文本+图片+注释） |
| `HexEditor(TString file)` → `TString` | 十六进制编辑器 |
| `OpenPdfReader(TString file)` | 打开PDF阅读器 |
| `ControlPanel(BYTE item, BYTE subItem, ...)` → `WORD` | 控制面板 |
| `ScanQrCode()` → `TString` | 扫描二维码 |
| `Println(TString text)` | 输出调试文本 |

### 网络控制

| 函数 | 功能 |
|------|------|
| `SetPadWIFI(BYTE state)` → `BOOL` | 设置WIFI开关 |
| `SetPadLANDHCP(BYTE state)` → `BOOL` | 设置有线网络DHCP |
| `SetPadLAN(UINT ipaddr, ...)` → `BOOL` | 设置固定IP |
| `GetPadEthernetIP()` → `TString` | 获取以太网IP |
| `GetNetWorkIp()` → `TString` | 获取网络IP |
| `CtrlNetworkInterface(eCtrlNetworkInterfaceParams method)` → `WORD` | 控制网络接口切换 |
| `IfWanISAvailable()` → `BOOL` | 判断是否可联网 |
| `GetAppConnectType()` → `BYTE` | 获取当前通信类型 |
| `SetAppConnectType(COMM_TYPE type)` → `BOOL` | 设置通信类型 (TYPE_BT/TYPE_WIRE/TYPE_WIFI等) |

---

## 扫描系统相关类

### CScanDtc — 扫描故障码集合

| 方法 | 功能 |
|------|------|
| `Add(TString code, TString text, TString status="", TString help="", TString info="")` | 添加故障码 |
| `Add(DWORD id, TString code, TString text, ...)` | 添加故障码（带ID） |
| `GetCount()` → `int` | 获取数量 |
| `GetDtc(int index)` → `tagOneDtc*` | 获取指定故障码 |
| `Clear()` | 清空 |
| `Delete(TString code)` / `Delete(int i)` | 删除指定故障码 |
| `Unique()` | 去重 |

### CDtcFrz — 故障码冻结帧

| 方法 | 功能 |
|------|------|
| `CDtcFrz(TString code, TString text, ...)` | 构造函数 |
| `AddFrz(TString text, TString value, TString unit)` → `DWORD` | 添加冻结帧项 |
| `Getcount()` → `DWORD` | 获取数量 |
| `Delete(TString text)` | 删除指定项 |
| `Clear()` | 清空 |

### CLinkSet — 通信链路配置

用于自动扫描时配置 ECU 通信参数。

| 方法 | 功能 | 关键参数 |
|------|------|----------|
| `Init()` | 从 CSheetSet 初始化 | — |
| `SetProtocol(WORD protocol)` | 设置协议类型 | — |
| `SetCommPort(BYTE sendLine, BYTE recvLine, WORD linkCtrl)` | 设置通信端口 | — |
| `SetBaudrate(UINT bps, BYTE parity=PB_NONE, BYTE dataBits=8)` | 设置波特率 | — |
| `SetCommTime(WORD comm_time, WORD P4, WORD P3, WORD P2, WORD P1)` | 设置通信时间参数 | — |
| `SetDumpByte(BYTE dumpByte)` | 设置转储字节 | — |
| `SetPackParam(BYTE pack_type, DWORD pack_flag, BYTE param_cnt, ...)` | 设置打包参数 | 可变参数 |
| `SetFilterParam(BYTE filterType, BYTE filterCnt, ...)` | 设置过滤参数 | filterType: 0-5 |
| `SetBusyCount(WORD n7F78=65535, WORD n7F21=65535, WORD n7F23=65535)` | 设置忙等待计数 | — |
| `AddEnterCmd(CBinary cmd, DWORD flag=INVALID)` | 添加进入命令 | — |
| `AddDtcCmd(CBinary cmd, DWORD flag=INVALID)` | 添加读码命令 | — |
| `AddClrCmd(CBinary cmd, DWORD flag=INVALID)` | 添加清码命令 | — |
| `AddPrescanCmd(CBinary cmd, DWORD flag=INVALID, eCommandType type=NORMAL_COMMAND)` | 添加预扫描命令 | — |
| `InitLinkSet()` → `int` | 初始化协议参数 | 0=成功 |
| `QuickPulseEnter(DWORD flag, CBinary& frame, WORD lowTime=25, WORD highTime=25)` | 快速脉冲进入 | — |
| `AddressCodeEnter(BYTE addrCode, ...)` | 地址码进入 | — |
| `AutoFlowControl(DWORD flag, CBinary cmd, WORD delay=0)` | 自动流控 | — |
| `KeepCommLink(DWORD flag, CBinary cmd, WORD keepTime=800)` | 保持通信链路 | — |

### CScanSys — 扫描系统（继承自 CItemNode）

| 方法 | 功能 |
|------|------|
| `AddLinkSet(CLinkSet& linkSet)` | 手动添加链路 |
| `LoadLinkSet(UINT excelId)` | 从表格加载链路 |
| `GetLinkSet()` → `CLinkSet*` | 获取当前Checked的链路 |
| `FindLinkSet(CLinkSet& linkSet)` → `BOOL` | 查找链路 |
| `EnterSystem()` → `BOOL` | 进入系统 |
| `ExitSystem()` → `BOOL` | 退出系统 |
| `GetName()` / `SetName(TString)` | 获取/设置系统名称 |
| `GetVin()` / `SetVin(TString)` | 获取/设置VIN |
| `GetMileage()` / `SetMileage(TString, TString unit)` | 获取/设置里程 |

### CGroupSys — 系统组（含故障码和ECU信息）

| 方法 | 功能 |
|------|------|
| `GetSystem()` → `CScanSys*` | 获取系统 |
| `GetSubSystem(int index)` → `CScanSys*` | 获取子系统 |
| `GetSubSysNum()` → `int` | 获取子系统数量 |
| `GetSysDtc()` → `CScanDtc*` | 获取系统故障码 |
| `GetSysDtcFrz()` → `CScanDtcFrz*` | 获取冻结帧 |
| `GetSysEcuInfo()` → `CScanEcuInfo*` | 获取ECU信息 |
| `AddSubSystem(const CScanSys& item)` | 添加子系统 |

---

## CMenuTree / CMenuItem — 菜单树

### CMenuTree

| 方法 | 功能 |
|------|------|
| `CMenuTree(UINT id)` | 构造函数，从数据库加载菜单树 |
| `Load(UINT id)` → `CMenuItem*` | 加载菜单树 |
| `LoadLazy(UINT id)` → `CMenuItem*` | 懒加载菜单树 |
| `Create(TString text, UINT taskId=INVALID, ...)` → `CMenuItem*` | 创建根节点 |
| `GetRoot()` → `CMenuItem*` | 获取根节点 |
| `Free()` | 释放菜单树 |

### CMenuItem（继承自 CItemNode）

| 方法 | 功能 |
|------|------|
| `InsertItem(TString text, UINT taskId=INVALID, ...)` → `CMenuItem*` | 在同级插入项 |
| `InsertChild(TString text, UINT taskId=INVALID, ...)` → `CMenuItem*` | 插入子项 |
| `FindItem(UINT key, BYTE type=BY_TASKID, BOOL bBFS=FALSE)` → `CMenuItem*` | 按ID查找节点 |
| `FindItem(const char* key, BYTE type=BY_EXTRA, BOOL bBFS=FALSE)` → `CMenuItem*` | 按文本查找节点 |
| `RemoveItem()` / `RemoveChild()` | 删除节点/子节点 |
| `GetParent()` / `GetChild()` / `GetNext()` | 树导航 |
| `GetText()` → `TString` | 获取文本 |
| `SetText(TString)` | 设置文本 |
| `GetTaskId()` / `SetTaskId(UINT)` | 获取/设置任务ID |
| `GetParameter()` / `SetParameter(UINT)` | 获取/设置参数 |
| `EnableItem(BOOL)` / `VisibleItem(BOOL)` | 启用/可见控制 |
| `Clone()` → `CMenuItem*` | 克隆节点 |
