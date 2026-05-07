# 平台 API 索引

> 本文件为精简索引，详细接口说明请按需读取对应文档。

## 文档目录

| 文档 | 涵盖范围 | 关键类/命名空间 |
|------|----------|-----------------|
| [display.md](docs/api/display.md) | 显示系统 — UI弹框、菜单、列表、输入、图片、拓扑图 | `CDisplay`、`StatusBox`、`MessageBox`、`MenuBox`、`ListBox`、`InputBox`、`ImageBox`、`TopoTestBox`、`SuperListPro`、`Grid` |
| [comm.md](docs/api/comm.md) | 通讯系统 — 帧构造/解析、协议、ECU通讯、过滤器、多路通讯 | `CSendFrame`、`CReceiveFrame`、`CProtocol`、`CCommEcu`、`CCommFilter`、`MultComm` |
| [config.md](docs/api/config.md) | 配置与数据 — 全局配置、INI读写、MDB/BIN数据库、菜单树 | `CConfig`、`CProfile`、`CDatabase`、`CDataFile`、`CBinaryFile`、`CMdbFileReader`、`CMenuNode` |
| [diag.md](docs/api/diag.md) | 诊断系统 — 全局对象、诊断基类、动态库、授权、扫描框架 | `CDiagnoseSystem`、`CDiagnoseApp`、`CDynamicLibrary`、`CWarrant`、全局对象(`extern`) |
| [types.md](docs/api/types.md) | 基础类型 — 二进制数据、字符串、容器模板 | `CBinary`、`TString`、`CGroup<T>`、`CBinaryGroup`、`CStringGroup` |
| [ui-components.md](docs/api/ui-components.md) | 新UI组件系统 — 构建器、网格布局、21种具体组件、使用模式 | `CCodeUiBuilder`(推荐)、`CComponentBuilder`、`CXtoolUiBaseGrid`、`SuperListPro`、`SelectBox`、`Input`、`ComboBox`、`Progress` |
| [misc.md](docs/api/misc.md) | 工具与辅助 — 代理、表达式、JSON、转换、设备环境、加解密 | `MyDelegate`、`CExpress`、`CJsonBuilder`、`CDataConvertProcess`、`CDevEnvironment`、`CExcelFile` |

## 快速查找

**需要发送/接收诊断报文？** → `comm.md` — `CCommEcu::SendReceiveFrame`
**需要读取配置或数据库？** → `config.md` — `CConfig` / `CDatabase`
**需要弹框、菜单、列表等UI？** → `display.md` — `CDisplay` 命名空间
**需要操作二进制数据？** → `types.md` — `CBinary`
**需要构建新UI页面？** → `ui-components.md` — `CCodeUiBuilder` + 组件（继承链: Grid → ComponentBuilder → CodeUiBuilder）
**需要判断设备能力？** → `misc.md` — `CDevEnvironment::Is*Supported()`
**需要实现诊断流程？** → `diag.md` — `CDiagnoseSystem` 继承模式

## 全局对象速览

诊断程序中可直接使用的预实例化对象（声明于 `diag.h`）：

| 对象名 | 类型 | 用途 |
|--------|------|------|
| `MenuShow` | `CMenuShow` | 菜单显示 |
| `DataStream` | `CDataStream` | 数据流 |
| `TroubleCode` | `CTroubleCode` | 故障码 |
| `ActiveTest` | `CActiveTest` | 动作测试 |
| `SpecialTest` | `CSpecialTest` | 特殊功能 |
| `BatteryData` | `CBatteryData` | 电池数据 |
| `Information` | `CInformation` | 产品信息 |

## 头文件映射

| 头文件 | 对应文档 |
|--------|----------|
| `inc/disp.h` | display.md |
| `inc/comm.h` | comm.md |
| `inc/file.h` | config.md |
| `inc/diag.h` | diag.md |
| `inc/binary.h`、`inc/type.h` | types.md |
| `inc/baseComponents/**`、`inc/customized/ComponentBuilder/*` | ui-components.md |
| `inc/delegate.h`、`inc/calc.h`、`inc/jsonBuilder.h`、`inc/dataconvert.h`、`inc/devEnvironment.h`、`inc/encdec.h`、`inc/metric.h`、`inc/utils.h`、`inc/excel.h` | misc.md |
