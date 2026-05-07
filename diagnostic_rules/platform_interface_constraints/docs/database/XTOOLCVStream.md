# XTOOLCVStream 数据库文档

## 1 业务角色

XTOOLCVStream（CV 数据流数据库）是奔驰诊断系统中 **数据流功能的底层数据项定义库**。它存储了每个 ECU 数据流通道的具体测量项定义，包括诊断命令名称、显示文本 ID、数值格式、单位、映射值和标准值范围等信息。

**在数据流体系中的定位：**
- `XTOOLDataStream` 负责数据流的 **导航菜单和流程控制**（菜单树、跳转逻辑、Valid 条件判断）
- `XTOOLCVStream` 负责数据流的 **具体测量项内容定义**（DT 算法名、显示名、格式、单位、枚举映射）
- 两者通过 `DSGroupRef` 字段关联：DataStream 中的 `DSGroupRef1` 引用 CVStream 中的节点 ID + 分组名

**典型业务场景：** 用户在数据流菜单中选择某一分组（如"灯光"）后，系统通过 CVStream 获取该分组下所有测量项（如左转向灯状态、尾灯状态、刹车灯状态等），并据此执行诊断命令、格式化显示值。

---

## 2 TXT 行格式

**文件基本信息：**
- 文件路径：`data/XtoolNum/XTOOLCVStream.txt`
- 宏定义：`XtoolCVStream` -> `CConfig::GetDiagDirectory()+"XtoolNum0/XTOOLCVStream.BIN"`
- 运行时格式：BIN（由 TXT 编译生成）
- 总行数：约 101,615 行
- 节点前缀：`0x88`
- 本文件为 **单节点文件**，即整个文件只有一个 8 字节节点 ID，所有 section 均在该节点下

### 2.1 节点头

```
0x88,0x00,0xe0,0x01,0x00,0x00,0x01,0x00		\"
```

每个 ECU 对应一个 8 字节十六进制节点 ID，其中 `0x88` 为固定前缀，后续字节编码 ECU 信息。本文件每个节点 ID 下包含大量 section。

### 2.2 记录类型

本文件包含两种 section 类型：

**类型 A：数据项定义（叶节点）**

```
[XTOOL_all_CV_{编号}_{序号}]
DSDiagserving={DT算法名称}          -- 诊断命令/算法名称
Format={格式字符串}                  -- 可选，如 %.0f、%.1f、%.2f
DSUnit={单位标识}                    -- 可选，如 REG_TEMP、空
DSCVText={文本ID}                    -- 多语言文本 ID，用于显示名称
Specified={标准值范围}               -- 可选，如 S_-20.0...85.0
cmdvalue1={条件}|{文本ID}            -- 可选，枚举映射值
cmdvalue2={条件}|{文本ID}            -- 可选
AddKeyWrod={Keyword表达式}           -- 可选，条件关键字
DSRVListRef={参考值列表引用}         -- 可选
Child={字段列表，用||分隔}           -- 声明本 section 包含哪些字段
```

**类型 B：分组定义（DSGroupDef）**

```
[XTOOL_all_CV_{分组名}_{组号}]
Value=DSGroupDef
Child={子数据项section名列表，用||分隔}
```

### 2.3 字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `DSDiagserving` | DT 诊断算法名称（用于实际发送诊断命令） | `DT_Ausgangszustaende_Blinker_Links` |
| `Format` | 数值格式化字符串 | `%.0f`、`%.1f`、`%.2f` |
| `DSUnit` | 物理单位标识 | `REG_TEMP`（温度）、空（无单位） |
| `DSCVText` | 多语言显示文本 ID，逗号分隔时含附加修饰 | `46118`、`46722,M_79277` |
| `Specified` | 标准值范围 | `S_-20.0...85.0` |
| `cmdvalue{N}` | 枚举映射：`条件表达式\|文本ID` | `nicht aktiv\|11652`、`<=7.0\|2938` |
| `AddKeyWrod` | 附加 Keyword 条件 | `DEF@PS_BLINKLICHT_LINKS` |
| `DSRVListRef` | 参考值列表引用节 | 引用 `XTOOL_{name}` 下的 DSRVItemDef |
| `Child` | 本 section 包含的字段名列表 | `DSDiagserving\|\|Format\|\|DSUnit\|\|DSCVText` |
| `Value` | section 类型标识（仅分组使用） | `DSGroupDef`、`DSListDef` |

---

## 3 代码调用流程

### 3.1 主入口

**文件：** `code/BenzDataStream.cpp`，函数 `BenzGetDSInfo(TString strDS)` (第 4311 行)

```
用户选择数据流分组
    |
    v
BenzGetDSInfo(strDS)           -- strDS 格式："节点ID|分组前缀|分组名"
    |
    +--> BenzSplitString(strDS, "|", gDtc)  -- 拆分为 gDtc[0]=节点ID, gDtc[1]=前缀, gDtc[2]=分组名
    |
    +--> BenzLoadNode(XtoolCVStream, gDtc[0])   -- 加载 CVStream 节点
    |       |
    |       +--> [封装API追溯] 见 §3.3
    |
    +--> BenzGetStringCV(XtoolCVStream, gDtc[0], "XTOOL_"+gDtc[1], "Child")  -- 获取顶层分组的 Child 列表
    |
    +--> 遍历 Child 列表，根据 strRep 前缀匹配找到目标分组
    |       |
    |       +--> BenzGetStringCV(..., strFind, "Valid")    -- 检查 Valid 条件
    |       +--> BenzValidNode(sValid)                     -- 验证 Keyword
    |
    +--> BenzGetStringCV(..., strChild, "Value")           -- 获取节点类型
    |       |
    |       +--> 若 "DSGroupDef" -> 获取 Child 展开子项列表
    |       +--> 否则 -> 直接作为单项处理
    |
    +--> 遍历每个数据项：
            |
            +--> BenzGetStringCV(..., "DSCVText")          -- 获取显示文本 ID
            +--> BenzGetStringCV(..., "Format")            -- 获取格式
            +--> BenzGetStringCV(..., "DSDiagserving")     -- 获取 DT 算法名
            +--> BenzGetStringCV(..., "DSUnit")            -- 获取单位
            +--> BenzGetStringCV(..., "Child")             -- 获取字段列表
            +--> 遍历 Child 中的 cmdvalue{N} -> 构建映射表
            +--> BenzGetStringCV(..., "Specified")         -- 获取标准值
            +--> BenzGetStringCV(..., "DSRVListRef")       -- 获取参考值列表
            |
            +--> 填充 Ds_Struct 结构体 -> 返回 CGroup<Ds_Struct>
```

### 3.2 BenzGetStringCV 函数定义

**位置：** `code/BenzDataStream.cpp` 第 2366 行

```cpp
TString CBenzDiagnose::BenzGetStringCV(TString strFile, TString strNode, TString strSection, TString strKey)
{
    BenzLoadNodeNew(strFile, strNode);          // 确保节点已加载
    TString strValue = GetString(strSection, strKey);  // 从当前 INI 读取值
    if (GetSectionKeys(strSection).size() <= 0) // 若 section 不存在
    {
        // 尝试加载 "ff" 后缀节点中的 XTOOL_Child 映射
        TString strNodeNew = strNode;
        strNodeNew[last-1] = 'f'; strNodeNew[last-2] = 'f';
        // ...重定向到实际节点后重新读取
    }
    BenzUpdateStrName(strValue);  // 处理 * 前缀等动态文本替换
    return strValue;
}
```

### 3.3 封装 API 到 CDatabase::SetProfile 的追溯链

```
BenzGetDSInfo()
    |
    +--> BenzLoadNode(XtoolCVStream, gDtc[0])           [BenzDataStream.cpp:4320]
    |       |
    |       +--> CBinary binID = HexTstringToBinary(strNode)  -- 将十六进制字符串转为二进制
    |       +--> SetProfile(strFile, binID)                    [BenzDataStream.cpp:3116]
    |               |
    |               +--> CDatabase::SetProfile(strFile, binID)
    |                       -- 平台 API：根据 BIN 文件路径和节点 ID 加载对应 INI 数据段
    |                       -- strFile = XtoolCVStream = GetDiagDirectory()+"XtoolNum0/XTOOLCVStream.BIN"
    |                       -- binID = 8 字节节点标识
    |
    +--> BenzGetStringCV(XtoolCVStream, ...)             [BenzDataStream.cpp:4324]
            |
            +--> BenzLoadNodeNew(strFile, strNode)       [BenzDataStream.cpp:2368]
            |       |
            |       +--> HexTstringToBinary(strNode)
            |       +--> SetProfile(strFile, binID)      [BenzDataStream.cpp:2072]
            |               |
            |               +--> CDatabase::SetProfile(strFile, binID)
            |
            +--> GetString(strSection, strKey)
                    -- CDatabase 继承方法：从已加载的 INI 数据中读取指定 section/key 的值
```

**关键追溯结论：**
- `BenzLoadNode()` 和 `BenzLoadNodeNew()` 都是 `CDatabase::SetProfile()` 的封装
- `BenzLoadNode` (第 3113 行)：`SetProfile(strFile, HexTstringToBinary(strNode))`
- `BenzLoadNodeNew` (第 2065 行)：同样调用 `SetProfile(strFile, HexTstringToBinary(strNode))`
- `BenzGetStringCV` 内部先调用 `BenzLoadNodeNew` 确保节点加载，然后通过 `GetString` 读取键值

---

## 4 带注释真实样本

### 样本 1：叶节点 -- 简单状态值（枚举型）

```ini
[XTOOL_all_CV_1_0]                           # section 名：all_CV 分组下第 1 项，内部序号 0
DSDiagserving=DT_Ausgangszustaende_Blinker_Links   # DT 算法：左转向灯输出状态
cmdvalue1=nicht aktiv|11652                   # 枚举值 1：不活跃 -> 文本 ID 11652
cmdvalue2=aktiv|11653                         # 枚举值 2：活跃 -> 文本 ID 11653
DSCVText=46118                                # 显示名称文本 ID：46118
AddKeyWrod=DEF@PS_BLINKLICHT_LINKS            # 条件 Keyword：左转向灯功能激活时才显示
Child=DSDiagserving||cmdvalue1||cmdvalue2||DSCVText||AddKeyWrod  # 本 section 包含的字段声明
```

### 样本 2：叶节点 -- 数值型（带格式、单位、标准值）

```ini
[XTOOL_all_CV_313_28]                         # section 名：all_CV 分组下第 313 项，内部序号 28
DSDiagserving=DT_Temperature_Amp              # DT 算法：功放温度
Format=%.1f                                   # 格式：保留 1 位小数
DSUnit=REG_TEMP                               # 单位：温度（代码中会替换为实际单位符号）
Specified=S_-20.0...85.0                      # 标准值范围：-20.0 到 85.0
DSCVText=36132,M_24058                        # 显示文本 ID：36132，附加修饰文本 M_24058
AddKeyWrod=DEF@PSHUHT                         # 条件 Keyword
Child=DSDiagserving||Format||DSUnit||Specified||DSCVText||AddKeyWrod  # 字段声明
```

### 样本 3：叶节点 -- 多级枚举映射

```ini
[XTOOL_all_CV_82_27]                          # section 名：all_CV 分组下第 82 项，内部序号 27
DSDiagserving=DT_STO_ReadInternalData2_TankState  # DT 算法：油箱状态读取
cmdvalue1=<=7.0|2938                          # 值 <=7.0 -> 文本 ID 2938
cmdvalue2=<=6.0|18623,82168                   # 值 <=6.0 -> 文本 ID 18623,82168
cmdvalue3=<=5.0|17446,82168                   # 值 <=5.0 -> 文本 17446,82168
cmdvalue4=<=4.0|16729,46887,82168             # 值 <=4.0 -> 文本 16729,46887,82168
cmdvalue5=<=3.0|36991,82168                   # 值 <=3.0 -> 文本 36991,82168
cmdvalue6=<=2.0|82413                         # 值 <=2.0 -> 文本 82413
cmdvalue7=<=1.0|2655,31572                    # 值 <=1.0 -> 文本 2655,31572
cmdvalue8=<=0.0|16729                         # 值 <=0.0 -> 文本 16729
DSCVText=126345                               # 显示名称文本 ID
Child=DSDiagserving||cmdvalue1||cmdvalue2||cmdvalue3||cmdvalue4||cmdvalue5||cmdvalue6||cmdvalue7||cmdvalue8||DSCVText
```

### 样本 4：分组定义（DSGroupDef）

```ini
[XTOOL_all_CV_Licht_30]                       # 分组名："Licht"（灯光），组号 30
Value=DSGroupDef                              # 类型标识：分组定义
Child=XTOOL_all_CV_1_0||XTOOL_all_CV_2_1||XTOOL_all_CV_3_2||XTOOL_all_CV_4_3||XTOOL_all_CV_5_4||...
                                              # 子数据项列表（左转向灯、左尾灯、刹车灯、倒车灯、右转向灯...）
```

### 样本 5：顶层列表定义（DSListDef）

```ini
[XTOOL_all_CV]                                # 顶层列表：all_CV
Value=DSListDef                               # 类型标识：列表定义
Child=XTOOL_all_CV_1_0||...||XTOOL_all_CV_Licht_30||XTOOL_all_CV_Spannung_31||...||XTOOL_all_CV_XTOOLOTHER_43
                                              # 包含所有数据项和分组定义
Value=DSGroupDef                              # 第二个 Value：也作为分组用
```

---

## 5 新增记录模板

### 模板 A：新增叶节点（数值型数据项）

```ini
[XTOOL_all_CV_{编号}_{序号}]
DSDiagserving={DT算法名称}
Format={格式字符串，如 %.1f}
DSUnit={单位标识，如 REG_TEMP 或留空}
Specified={标准值范围，如 S_-20.0...85.0，可选}
DSCVText={多语言文本ID}
AddKeyWrod={Keyword条件表达式，可选}
Child=DSDiagserving||Format||DSUnit||Specified||DSCVText||AddKeyWrod
```

**填写说明：**
- `{编号}`：通常为数字（如 314），在分组内唯一
- `{序号}`：分组内递增序号（如 29），用于代码遍历时自增查找
- `DSDiagserving`：必须对应 NEWLRNCAL 或其他算法库中已定义的 DT 算法名
- `Format`：`%.0f`（整数）、`%.1f`（1 位小数）、`%.2f`（2 位小数）
- `DSUnit`：`REG_TEMP`（温度）、空（无单位）或其他已定义的单位标识
- `DSCVText`：需在多语言文本库中已注册的 ID
- `Child`：必须列出本 section 中实际存在的所有字段名

### 模板 B：新增叶节点（枚举型数据项）

```ini
[XTOOL_all_CV_{编号}_{序号}]
DSDiagserving={DT算法名称}
cmdvalue1={条件表达式}|{文本ID}
cmdvalue2={条件表达式}|{文本ID}
DSCVText={多语言文本ID}
AddKeyWrod={Keyword条件表达式，可选}
Child=DSDiagserving||cmdvalue1||cmdvalue2||DSCVText||AddKeyWrod
```

### 模板 C：新增分组定义

```ini
[XTOOL_all_CV_{分组名}_{组号}]
Value=DSGroupDef
Child={子数据项section名1}||{子数据项section名2}||...
```

**填写说明：**
- `{分组名}`：语义化英文名（如 `Licht`、`Spannung`、`Navigation`）
- `{组号}`：在 all_CV 顶层列表中的递增序号
- `Child`：引用本文件中已有的叶节点 section 名
- 新增分组后，需要在顶层 `[XTOOL_all_CV]` 的 Child 列表中追加此分组名

**注意事项：**
1. 新增分组后，必须同步更新 `XTOOLDataStream` 中对应菜单项的 `DSGroupRef1` 引用
2. 新增的 DT 算法名须在 NEWLRNCAL 算法库中已注册
3. `{序号}` 需保证在同一分组内连续递增，代码通过序号自增遍历数据项
