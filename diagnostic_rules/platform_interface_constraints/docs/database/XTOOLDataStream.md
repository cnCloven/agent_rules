# XTOOLDataStream 数据库文档

## 1 业务角色

XTOOLDataStream（综合数据流数据库）是奔驰诊断系统中 **数据流功能的导航和流程控制库**。它定义了数据流功能的完整交互流程：从入口菜单树、分支条件判断、子文件加载、到最终的数据展示动作。

**在数据流体系中的定位：**
- `XTOOLDataStream` 是数据流功能的 **"大脑"**，负责流程导航和逻辑控制
- `XTOOLCVStream` 是数据流功能的 **"仓库"**，负责存储具体测量项定义
- DataStream 通过 `DSGroupRef` 引用 CVStream，通过 `FileName` 引用自身子节点

**典型业务场景：**
1. 用户进入数据流功能 -> 系统加载 DataStream 的入口节点
2. 根据 `Begin`/`DSBegin` 节点的 Child 判断流程分支
3. 检查 `Valid` 条件（Keyword）决定是否显示快捷入口或菜单
4. 展示 `DSMenu` 菜单供用户选择（如"灯光"、"电压"等分组）
5. 用户选择后，通过 `DSGroupRef1` 引用 CVStream 加载具体测量项
6. 或通过 `FileName` 加载子节点文件继续导航

---

## 2 TXT 行格式

**文件基本信息：**
- 文件路径：`data/XtoolNum/XTOOLDataStream.txt`
- 宏定义：`XtoolDataStream` -> `CConfig::GetDiagDirectory()+"XtoolNum0/XTOOLDataStream.BIN"`
- 运行时格式：BIN（由 TXT 编译生成）
- 总行数：约 139,032 行
- 节点前缀：`0x88`
- 本文件为 **多节点文件**，包含多个 8 字节节点 ID，每个节点对应一个 ECU 的数据流流程定义

### 2.1 节点头

```
0x88,0x00,0xe0,0x01,0x00,0x00,0x01,0x00		\"
```

节点之间以 `\n"` + 空行 + 新节点 ID 行分隔。每个 ECU 可能有多个节点（通过 `FileName` 字段跨节点引用）。

### 2.2 节点类型说明

本文件包含以下几种关键的 section 类型（由 `Value` 字段标识）：

| Value 类型 | 含义 | 典型动作 |
|------------|------|----------|
| `DSBegin` | 数据流入口起始节点 | 读取 DSText、Child，判断是否有子文件 |
| `Begin` | 流程起始节点 | 读取 Next 字段进入流程分支 |
| `DSAct` | 动作节点 | 执行数据流展示/检测，处理 DSGroupRef 引用 |
| `DSMenu` | 菜单节点 | 展示菜单列表供用户选择 |
| `DSMenuItemNode` | 菜单项节点 | 单个菜单项定义（文本 + Next 跳转） |
| `DSMenuItemFile` | 菜单项文件节点 | 菜单项指向另一个子文件节点 |
| `DSLoad` | 加载节点 | 加载子文件节点 |
| `DSTest` | 测试节点 | 执行诊断测试并展示结果 |
| `DSEnd` | 结束节点 | 流程终止，Next=FF |

### 2.3 字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `Value` | 节点类型标识 | `DSBegin`、`DSAct`、`DSMenu` 等 |
| `Child` | 子字段/子节点列表（`\|\|`分隔） | `DSText\|\|FileName`、`Show\|\|DSGroupRef1\|\|Next` |
| `Next` | 下一步跳转目标（`\|\|`分隔多选） | `XTOOL_Valid_3_2_1\|\|XTOOL_3_2`、`FF`（结束） |
| `Valid` | Keyword 条件表达式（XML 格式） | `<Valid><For><Keyword>DEF@FUN_AKTIV</Keyword></For></Valid>` |
| `Show` | 是否显示（`true`/`false`） | `true` |
| `DSText` / `DSText1` | 显示文本 ID | `2649`、`2341` |
| `DSGroupRef1` | CV 数据流引用 | `0x88,...\|all_CV\|Licht` |
| `FileName` | 子节点文件引用 | `0x88,0x00,0xe0,0x01,0x00,0x00,0x02,0x00` |
| `AddKeyWrod` | 附加 Keyword | `DEF@...` |
| `DSCSDMake1` | 手动执行函数引用 | `Pub_BoxUnbekannteVariante` |
| `DSShopExpr{N}` | Shop 表达式（用于存储变量） | `ls10=...` |
| `DSTableTitle` | 表格标题引用 | 文本 ID |
| `DSTableItem{N}` | 表格数据行引用 | 文本 ID |
| `DTCTestRef{N}` | DTC 测试引用 | DT 算法名 |
| `Select` | 测试结果分支选择 | `yes\|...\|\|no\|...` |

### 2.4 DSGroupRef 引用格式

```
DSGroupRef1=0x88,0x00,0xe0,0x01,0x00,0x00,0x01,0x00|all_CV|Licht
             └── CVStream 节点 ID ──────────────────┘ └─前缀─┘ └分组名┘
```

此格式被代码解析为三部分，用 `|` 分隔：
1. CVStream 中的 8 字节节点 ID
2. section 前缀（如 `all_CV`）
3. 分组名或通配符（如 `Licht`、`*gs44`，`*` 表示动态替换）

---

## 3 代码调用流程

### 3.1 主入口：BenzReadDataStreamMode3

**文件：** `code/BenzDataStream.cpp`，第 2079 行

```
BenzReadDataStreamMode3()                  -- 数据流 Mode3 入口
    |
    +--> 构建 binID = "\x88\x00\x00\x00\x00\x00\x01\x00"
    |       设置 binID[2..3] = m_ECUHexStr[0..1]   -- 填入 ECU 标识
    |
    +--> BenzLoadNodeNew(XtoolDataStream, BinaryToString(binID))  -- 加载入口节点
    |
    +--> BenzGetString(XtoolDataStream, ..., "XTOOL_0_0", "Child")  -- 读取入口 Child
    +--> BenzGetString(XtoolDataStream, ..., "XTOOL_0_0", "AddKeyWrod")  -- 读取 Keyword
    |
    +--> 遍历 Child：
    |       |
    |       +--> "FileName" -> BenzGetString(..., "FileName") 获取子节点 ID
    |       |       +--> BenzLoadNode(XtoolDataStream, strNode)  -- 加载子节点
    |       |       +--> BenzRunChild(strNode, "XTOOL_0_0")      -- 递归执行子流程
    |       |
    |       +--> "Next" -> BenzRunChild(binID_str, "XTOOL_0_0")  -- 直接跳转
```

### 3.2 核心递归引擎：BenzRunChild

**文件：** `code/BenzDataStream.cpp`，第 2137 行 + `code/BenzDiagnose.cpp`

```
BenzRunChild(strNode, strSection, iFlag)
    |
    +--> BenzGetString(XtoolDataStream, strNode, strSection, "Value")  -- 读取节点类型
    |
    +--> 根据 Value 分派：
    |
    |   "Begin" / "DSBegin"
    |       +--> BenzChildBegin()  -- 处理 Begin 逻辑，返回 Next
    |
    |   "DSAct"
    |       +--> BenzChildDSAct()  -- 执行动作逻辑
    |           |
    |           +--> 检查 Valid 条件
    |           +--> 遍历 Child：
    |           |       AddKeyWrod -> BenzDSAddKeyword()
    |           |       DSCSDMake  -> BenzDSManualAddFunction()  -- 手动执行函数
    |           |       DSGroupRef -> BenzGetString() 获取引用 -> 传给 BenzGetDSInfo()
    |           |              +--> [转入 CVStream 读取，见 CVStream 文档 §3]
    |           |       DSShopExpr -> BenzDSShopExpr()  -- 设置 Shop 变量
    |           |       DTCTestRef -> BenzDTCTestRef()  -- DTC 测试
    |           |       Show       -> 控制是否显示
    |           |
    |           +--> BenzShowDataStream()  -- 向 UI 展示数据流
    |           +--> BenzLoadNode(XtoolDataStream, strNode)  -- 重新加载当前节点
    |           +--> BenzGetString(..., strChild)  -- 获取下一步
    |
    |   "DSMenu"
    |       +--> BenzChildDSMenu()  -- 展示菜单
    |           +--> 遍历 Next 中的菜单项
    |           +--> BenzGetString(..., "DSText1")  -- 获取菜单文本
    |           +--> BenzGetString(..., "Valid")     -- 检查显示条件
    |           +--> BenzGetString(..., "FileName")  -- 检查子文件 Valid
    |           +--> 用户选择后跳转到对应菜单项的 Next
    |
    |   "DSMenuItemNode"
    |       +--> BenzDSMenuItemNode()  -- 处理菜单项
    |           +--> BenzGetString(..., "Next")       -- 获取跳转目标
    |           +--> BenzGetString(..., "AddKeyWrod") -- 设置 Keyword
    |           +--> BenzGetString(..., "DSShopExpr") -- 设置变量
    |
    |   "DSMenuItemFile"
    |       +--> BenzDSMenuItemFile()  -- 加载子文件
    |           +--> BenzGetString(..., "FileName")
    |           +--> BenzLoadNode(XtoolDataStream, strNewNode)
    |           +--> BenzRunChild(strNewNode, "XTOOL_0_0")  -- 递归进入子文件
    |
    |   "DSLoad"
    |       +--> BenzChildDSLoad()  -- 加载子文件节点
    |           +--> BenzGetString(..., "FileName")
    |           +--> BenzLoadNode(XtoolDataStream, strNewNode)
    |           +--> BenzRunChild(strNewNode, "XTOOL_0_0")
    |
    |   "DSTest"
    |       +--> BenzChildDSTest()  -- 执行测试
    |           +--> 遍历 Child 获取 DTCTestRef
    |           +--> 根据测试结果走 Select 分支
    |
    |   "DSEnd" / Next=="FF"
    |       +--> 流程结束，返回
```

### 3.3 封装 API 到 CDatabase::SetProfile 的追溯链

```
BenzReadDataStreamMode3()
    |
    +--> BenzLoadNodeNew(XtoolDataStream, strNode)    [BenzDataStream.cpp:2092]
    |       |
    |       +--> CBinary binID = HexTstringToBinary(strNode)
    |       +--> SetProfile(strFile, binID)            [BenzDataStream.cpp:2072]
    |               |
    |               +--> CDatabase::SetProfile(XtoolDataStream_BIN路径, binID)
    |                       -- 平台 API：加载 BIN 文件中 binID 对应的 INI 数据段
    |
    +--> BenzGetString(XtoolDataStream, ...)           [BenzDataStream.cpp:2097]
    |       |
    |       +--> GetString(strSection, strKey)          -- CDatabase 继承方法
    |       |       -- 从 SetProfile 已加载的数据中读取 section/key 值
    |       |
    |       +--> 若值为空，尝试遍历 '0'-'9' 后缀节点：
    |               +--> BenzLoadNodeNew(strFile, strNodeNew)
    |               +--> GetString(strSection, strKey)
    |
    +--> BenzLoadNode(XtoolDataStream, strNode)        [BenzDataStream.cpp:2110]
            |
            +--> CBinary binID = HexTstringToBinary(strNode)
            +--> SetProfile(strFile, binID)             [BenzDataStream.cpp:3116]
                    |
                    +--> CDatabase::SetProfile(XtoolDataStream_BIN路径, binID)
```

**三个封装 API 的 SetProfile 追溯对比：**

| 封装函数 | 定义位置 | SetProfile 调用位置 | 差异 |
|----------|----------|---------------------|------|
| `BenzLoadNode` | 第 3113 行 | 第 3116 行 | 直接封装，失败返回 FALSE |
| `BenzLoadNodeNew` | 第 2065 行 | 第 2072 行 | 增加空节点检查，逻辑相同 |
| `BenzGetString` | 第 2338 行 | 内部调用 `BenzLoadNodeNew` | 增加后缀遍历回退机制 |

---

## 4 带注释真实样本

### 样本 1：入口节点（DSBegin）

```ini
# 节点 ID：ECU 0xe0,0x01 的入口
0x88,0x00,0xe0,0x01,0x00,0x00,0x01,0x00		\"
[XTOOL_0_0]                                   # 固定入口 section 名
Value=DSBegin                                  # 类型：数据流入口起始
DSText=2649                                    # 显示文本 ID（如"数据流"标题）
Child=DSText||FileName                         # 子字段：文本 + 子文件引用
FileName=0x88,0x00,0xe0,0x01,0x00,0x00,0x02,0x00  # 跳转到第 2 个子节点
\n"
```

### 样本 2：流程起始节点（Begin）+ Valid 条件分支

```ini
# 子节点：ECU 0xe0,0x01 的第 2 个节点
0x88,0x00,0xe0,0x01,0x00,0x00,0x02,0x00		\"
[XTOOL_0_0]                                   # 入口 section
Value=Begin                                    # 类型：流程起始
Child=Next                                     # 子字段：仅 Next 跳转
Next=XTOOL_Valid_3_2_1||XTOOL_3_2             # 两个候选分支（Valid 优先匹配）

[XTOOL_Valid_3_2_1]                            # 带 Valid 条件的分支
Valid=<Valid><For><Keyword>DEF@FUN_AKTIV</Keyword></For></Valid>
                                               # 条件：需要 FUN_AKTIV keyword 激活
Value=DSAct                                    # 条件满足时：执行 DSAct 动作
Show=true                                      # 显示此动作
DSGroupRef1=0x88,0x00,0xe0,0x01,0x00,0x00,0x01,0x00|all_CV|*gs44
                                               # 引用 CVStream：节点 ID | 前缀 all_CV | 分组 *gs44
                                               # *gs44 = 动态替换（由 DSShopExpr 设置的 gs44 变量决定）
Child=Show||DSGroupRef1||Next                  # 字段列表
Next=FF                                        # 执行完毕后结束

[XTOOL_3_2]                                    # 无条件分支（兜底）
Value=DSMenu                                   # 类型：菜单
Child=Next                                     # 子字段：Next
Next=XTOOL_3_2_DSMenuItemNode_0||XTOOL_3_2_DSMenuItemNode_1||XTOOL_3_2_DSMenuItemNode_2
                                               # 三个菜单项
\n"
```

### 样本 3：菜单项节点 -> 引用 CVStream 分组

```ini
[XTOOL_3_2_DSMenuItemNode_0]                   # 菜单项 0
Value=DSMenuItemNode                           # 类型：菜单项
DSText1=2341                                   # 菜单显示文本 ID（如"灯光"）
Child=DSText1||Next                            # 字段：文本 + 跳转
Next=XTOOL_7_4                                 # 跳转到 DSAct 节点

[XTOOL_7_4]                                    # 菜单项对应的动作节点
Value=DSAct                                    # 类型：动作
Show=true                                      # 显示
DSGroupRef1=0x88,0x00,0xe0,0x01,0x00,0x00,0x01,0x00|all_CV|Licht
                                               # 引用 CVStream 的 "Licht"（灯光）分组
                                               # -> 对应 CVStream 中的 [XTOOL_all_CV_Licht_30]
Child=Show||DSGroupRef1||Next                  # 字段列表
Next=FF                                        # 展示完数据流后结束
```

### 样本 4：DSLoad 节点（加载子文件）+ NULL 终止

```ini
[XTOOL_7_31]                                   # DSLoad 节点
Value=DSLoad                                   # 类型：加载子文件
Child=FileName                                 # 子字段：文件名
FileName=NULL                                  # NULL = 无子文件（终止）
```

### 样本 5：带 Except 条件的 Valid 分支

```ini
[XTOOL_Valid_1_3_1]                            # 带条件的分支
Valid=<Valid><For><Keyword>DEF@FUN_AKTIV</Keyword><Except><Keyword>DEF@FUN_AIRBAG</Keyword></Except></For></Valid>
                                               # 条件：FUN_AKTIV 激活 且 FUN_AIRBAG 未激活
Value=DSAct                                    # 动作节点
Show=true
DSGroupRef1=0x88,0x00,0xe0,0x0b,0x00,0x00,0x01,0x00|all_CV|*gs44
                                               # 引用另一个 CVStream 节点（0x0b ECU）
Child=Show||DSGroupRef1||Next
Next=FF
```

---

## 5 新增记录模板

### 模板 A：新增 ECU 数据流入口（两节点结构）

**节点 1：入口节点**

```ini
0x88,0x00,{ECU_H},{ECU_L},0x00,0x00,0x01,0x00		\"
[XTOOL_0_0]
Value=DSBegin
DSText={标题文本ID}
Child=DSText||FileName
FileName=0x88,0x00,{ECU_H},{ECU_L},0x00,0x00,0x02,0x00
\n"
```

**节点 2：菜单节点**

```ini
0x88,0x00,{ECU_H},{ECU_L},0x00,0x00,0x02,0x00		\"
[XTOOL_0_0]
Value=Begin
Child=Next
Next={Valid分支section名}||{兜底菜单section名}

[{Valid分支section名}]
Valid=<Valid><For><Keyword>{Keyword条件}</Keyword></For></Valid>
Value=DSAct
Show=true
DSGroupRef1=0x88,0x00,{ECU_H},{ECU_L},0x00,0x00,0x01,0x00|all_CV|{分组名或*变量}
Child=Show||DSGroupRef1||Next
Next=FF

[{兜底菜单section名}]
Value=DSMenu
Child=Next
Next={菜单项1}||{菜单项2}||{菜单项3}

[{菜单项1}]
Value=DSMenuItemNode
DSText1={菜单文本ID}
Child=DSText1||Next
Next={动作节点section名}

[{动作节点section名}]
Value=DSAct
Show=true
DSGroupRef1=0x88,0x00,{ECU_H},{ECU_L},0x00,0x00,0x01,0x00|all_CV|{CVStream分组名}
Child=Show||DSGroupRef1||Next
Next=FF
\n"
```

### 模板 B：在已有 ECU 菜单中新增菜单项

```ini
# 1. 在已有 DSMenu 的 Next 列表中追加新菜单项 section 名
# 2. 新增以下两个 section：

[XTOOL_{X}_{Y}_DSMenuItemNode_{N}]
Value=DSMenuItemNode
DSText1={菜单项文本ID}
Child=DSText1||Next
Next=XTOOL_{动作节点编号}

[XTOOL_{动作节点编号}]
Value=DSAct
Show=true
DSGroupRef1={CVStream节点ID}|all_CV|{分组名}
Child=Show||DSGroupRef1||Next
Next=FF
```

### 模板 C：新增带条件加载的子文件菜单项

```ini
[XTOOL_{X}_{Y}_DSMenuItemFile_{N}]
Value=DSMenuItemFile
DSText1={菜单项文本ID}
FileName={子节点8字节ID}
AddKeyWrod={可选Keyword}
Child=DSText1||FileName||AddKeyWrod
```

**填写说明：**
- `{ECU_H},{ECU_L}`：ECU 标识的高低字节，与 `m_ECUHexStr` 对应
- `{标题文本ID}`：多语言文本库中已注册的 ID
- `{CVStream节点ID}`：必须与 CVStream 中的实际节点 ID 一致
- `{分组名}`：对应 CVStream 中 `[XTOOL_all_CV_{分组名}_{组号}]` 的分组名部分
- `*变量名`：动态分组引用，变量由 `DSShopExpr` 在流程中设置
- `FF`：固定终止标记，表示流程结束
- Valid 条件中的 `<Except>` 可用于排除特定 Keyword

**注意事项：**
1. 新增 ECU 入口时，需确保 CVStream 中已有对应节点 ID 的数据项定义
2. 菜单项的 Next 跳转目标 section 必须在同一节点内定义
3. 跨节点引用使用 `FileName` + `BenzLoadNode`，不能用 Next 直接跳转
4. 所有 DSGroupRef 中的节点 ID 必须是 CVStream 文件中的有效节点 ID
