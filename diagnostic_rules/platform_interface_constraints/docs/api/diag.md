# 诊断系统 API 速查 (diag.h)

> **头文件**: `D:\work\platform\inc\diag.h`
> 包含诊断系统基类、应用基类、动态库加载、授权管理，以及所有全局 UI 对象的 extern 声明。
> `diag.h` 同时 using namespace CDisplay / CCommEcu / CDatabase / CCommFilter，使得这些命名空间下的函数可直接使用。

---

## 1. 全局对象声明

diag.h 通过 extern 声明了所有可直接使用的全局 UI 对象：

| 对象名 | 类型 | 用途 |
|--------|------|------|
| `MenuShow` | `CMenuShow` | 菜单显示 |
| `ShortTest` | `CShortTest` | 快速测试 |
| `VehicleInfo` | `CVehicleInfo` | 车辆信息 |
| `TroubleCode` | `CTroubleCode` | 故障码 |
| `FaultCodeUI` | `CFaultCodeUI` | 故障码UI（支持冻结帧） |
| `MultiSelect` | `CMultiSelect` | 多选数据流 |
| `DataStream` | `CDataStream` | 数据流 |
| `ActiveTest` | `CActiveTest` | 动作测试 |
| `SpecialTest` | `CSpecialTest` | 特殊功能 |
| `TopoTest` | `CTopoTest` | 拓扑测试 |
| `MultInput` | `CMultInput` | 多项输入 |
| `FormInput` | `CFormInput` | 表单输入 |
| `SpecialInput` | `CSpecialInput` | 特殊输入 |
| `ProgInput` | `CProgInput` | 编程输入 |
| `HiddenFunc` | `CHiddenFunc` | 隐藏功能 |
| `GraphList` | `CGraphList` | 图形列表 |
| `TroubleList` | `CTroubleList` | 故障列表 |
| `BatteryData` | `CBatteryData` | 电池数据流 |
| `VehicleStep` | `CVehicleStep` | 车型步骤 |
| `VehicleReport` | `CVehicleReport` | 车辆报告 |
| `TPMSManage` | `CTPMSManage` | 胎压管理 |
| `GridList` | `CGridList` | 网格列表 |
| `UserGrid` | `CUserGrid` | 用户网格 |
| `ListShow` | `CListShow` | 通用列表 |
| `SmartEnter` | `CSmartEnter` | 智能输入 |
| `InspectTestUI` | `CInspectTestUI` | 检测测试UI |
| `VehicleData` | `CVehicleData` | 车辆数据（仅Cocos） |

---

## 2. CDiagnoseSystem — 诊断系统基类

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `CDiagnoseSystem()` | — | 构造函数 |
| `virtual EnterSystem(UINT idm)` | `BOOL` | 进入诊断系统 |
| `virtual Diagnose(UINT idm) = 0` | `BOOL` | 诊断主逻辑（纯虚函数，子类必须实现） |
| `virtual ExitSystem(UINT idm)` | `BOOL` | 退出诊断系统 |
| `virtual OnIdle()` | `void` | 空闲回调 |
| `static EnableIdle(BOOL, DWORD=0)` | `void` | 启用/禁用空闲处理 |
| `static IsEnableIdle()` | `BOOL` | 查询空闲状态 |

成员变量：

| 成员 | 类型 | 说明 |
|------|------|------|
| `m_vsScanTroubleCode` | `CGroup<tagFaultCode>` | 扫描故障码结果 |
| `m_qtfScanType` | `QTF_TYPE` | 扫描类型 |
| `m_qftScanDtcFlag` | `QTF_DTC` | 扫描DTC标志 |
| `m_pDiagnoseSystem` (static) | `CDiagnoseSystem*` | 当前诊断系统指针 |

宏：`AfxGetSystem()` → 获取当前诊断系统指针

---

## 3. CDiagnoseApp — 诊断应用基类

| 方法 | 说明 |
|------|------|
| `CDiagnoseApp()` | 构造函数 |
| `virtual InitInstance()` | 初始化实例（子类 CScanApp 重写此方法） |
| `m_pDiagnoseApp` (static) | 当前应用指针 |

---

## 4. CDynamicLibrary — 动态库加载

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `Load(TString strDllPath)` | `BOOL` | 加载动态库（.so/.dll 完整路径） |
| `GetFuncPointer(TString strFuncName)` | `void*` | 获取导出函数指针（需强转） |
| `Close()` | `void` | 卸载动态库 |
| `SetFlags(int flags)` | `void` | 设置加载标志（RTLD_LAZY等，仅Linux有效） |

---

## 5. CWarrant — 授权管理

| 方法 | 说明 |
|------|------|
| `static Lisence()` → BOOL | 授权校验 |

---

## 6. 扫描框架

### 6.1 CodeScan 函数

```cpp
BOOL CodeScan(CDiagnoseSystem *pSystem, UINT idm=0, UINT flag=ESF_NORMAL);
```

扫描标志：`ESF_NORMAL=0x00`, `ESF_CODE_PRIOR=0x01`, `ESF_USER_ENTER=0x02`, `ESF_AUTO_SCAN=0x100`

### 6.2 扫描函数映射宏

```cpp
BEGIN_SCAN_MAP()
    ON_SCAN_FUNCTION("FuncName", FuncPointer)
END_SCAN_MAP()
```

### 6.3 动态扫描

| 函数 | 说明 |
|------|------|
| `GetPkgDynamicLibPath(const string& path)` → string | 获取指定诊断包的 libscan 路径 |
| `DynamicScan(TString path, TString func, UINT idm, ...)` → BOOL | 动态加载执行扫描 |

---

## 7. 典型使用示例

### 7.1 诊断系统标准流程

```cpp
class CMySystem : public CDiagnoseSystem {
public:
    virtual BOOL Diagnose(UINT idm) {
        // 菜单分发
        UINT sel;
        MenuShow.Init(LoadText(idm));
        MenuShow.Add(LoadText(ID_READ_VERSION));
        MenuShow.Add(LoadText(ID_READ_DTC));
        while (MenuShow.Show(sel) != KEY_ESC) {
            switch (sel) {
                case 0: ReadVersion(); break;
                case 1: ReadDTC(); break;
            }
        }
        return TRUE;
    }
};
```

### 7.2 动态库加载

```cpp
CDynamicLibrary lib;
if (lib.Load("/path/to/libprog.so")) {
    typedef void (*FuncPtr)(CBaseInfo*);
    FuncPtr fn = (FuncPtr)lib.GetFuncPointer("FunctionInterface");
    if (fn) fn(&baseInfo);
    lib.Close();
}
```

### 7.3 动态扫描

```cpp
std::string libPath = GetPkgDynamicLibPath("Europe/PS_TRANSPORTER");
if (!libPath.empty()) {
    DynamicScan("Europe/PS_TRANSPORTER", "ScanFunc", idm);
}
```
