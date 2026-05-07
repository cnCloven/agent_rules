# 新 UI 组件体系 API 速查

> **头文件目录**: `inc/baseComponents/`、`inc/customized/ComponentBuilder/`
> 继承链: `CXtoolUiBaseGrid` → `CComponentBuilder` → `CCodeUiBuilder`
> 实际编程中使用 **CCodeUiBuilder** 构建界面，组件通过 AddComponent 装入，Show() 驱动事件循环。

---

## 1. CXtoolUiBaseComponent — 组件抽象基类

| 方法 | 说明 |
|------|------|
| `Init()` | 初始化（重置状态） |
| `SetValue(string)` / `GetValue()` | 设置/获取值 |
| `SetColor(string)` / `GetColor()` | 设置/获取颜色（如 `"#FF0000"`） |
| `SetTitle(string)` / `GetTitle()` | 设置/获取标题 |
| `SetText(string)` / `GetText()` | 设置/获取文本 |
| `static Version()` → string | 获取组件库版本号 |

纯虚方法（子类必须实现）：`toJsonObject()`、`clone()`、`parseReturnValue()`、`getType()`、`getCid()`

---

## 2. CXtoolUiBaseGrid — 网格容器

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `Init()` | void | 初始化 |
| `AddComponent(const CXtoolUiBaseComponent&)` | void | 添加组件 |
| `GetComponent(int index)` | `const CXtoolUiBaseComponent*` | 获取组件（可能返回 nullptr） |
| `SetComponent(int index, const CXtoolUiBaseComponent&)` | bool | 替换指定位置组件 |
| `RemoveComponent(int index)` | bool | 移除组件 |
| `ClearComponent()` | void | 清空所有组件 |
| `GetComponentSize()` | int | 组件数量 |
| `AddGrid(const CXtoolUiBaseGrid&)` | void | 添加子网格（水平分栏） |
| `GetGrid/SetGrid/RemoveGrid/ClearGrid` | — | 子网格管理 |
| `Clear()` | void | 清空所有 |
| `GetSelectedComponentIndex()` | int | 当前选中组件下标（-1=无） |

---

## 3. CComponentBuilder — 构建器基类

> 头文件: `inc/customized/ComponentBuilder/ComponentBuilder.h`
> 继承自 CXtoolUiBaseGrid，是所有构建器的基类。**构造函数为 protected，不可直接实例化**。

| 方法 | 说明 |
|------|------|
| `Init()` | 初始化构建器 |
| `SetTitle(const string& title)` | 设置页面标题 |
| `GetTitle()` → string | 获取标题 |
| `AddButton(int id, const string& text)` | 添加按钮，id 为唯一标识，Show() 返回该 id |
| `DeleteButton(int id)` | 删除按钮 |
| `EnableButton(int id, bool enable)` | 启禁按钮 |
| `EnableKeyEsc(bool enable)` | 启禁返回/退出键（false=禁止用户退出） |
| `SetNewInterface()` | 标记为新界面（首次 Show 后自动复位为 false） |
| `GetRTSelectedComponent()` → vector\<int\> | 获取实时选中的组件 cid 和选中索引 |
| `static Version()` → string | 构建器版本号 |

---

## 4. CCodeUiBuilder — 编程界面构建器（推荐使用）

> 头文件: `inc/customized/ComponentBuilder/CodeBuilder.h`
> 继承自 CComponentBuilder，**可直接实例化**，是实际编程中使用的构建器。

| 方法 | 说明 |
|------|------|
| `CCodeUiBuilder()` | 默认构造 |
| `CCodeUiBuilder(string title)` | 带标题构造 |
| `CCodeUiBuilder(string title, const CXtoolUiBaseGrid& grid)` | 带标题和初始网格构造 |
| `ActiveRT(bool active)` | 启用实时刷新（用于进度条等需要持续刷新的页面） |
| `Show()` → WORD | 显示界面，返回 KEY_ESC / 按钮 id |

---

## 5. 具体组件类（21个）

### 布局/展示类

| 组件类 | 用途 | 关键方法 |
|--------|------|----------|
| `CXtoolUiComponentText` | 文本展示 | `SetText/SetTitle/SetIcon/SetBold/SetAlign/SetColor/SetReplicable/SetFold/SetScale/SetRichText` |
| `CXtoolUiComponentTitle` | 标题 | `SetText` |
| `CXtoolUiComponentKeyValue` | 键值对 | `SetTitle/AddPairValue/GetPairValue/SetPairValue` |
| `CXtoolUiComponentSupportList` | 支持列表 | `SetTitle/AddStringValue/GetStringValue` |
| `CXtoolUiComponentImage` | 图片 | `SetImageValue/SetTitle/SetImageDisplay(w,h)` |
| `CXtoolUiComponentLine` | 分隔线 | 无额外方法 |
| `CXtoolUiComponentStatus` | 状态指示 | `SetStatusType(eStatusType)` |
| `CXtoolUiComponentProgress` | 进度条 | `SetTitle/SetPrompt/SetProgress(0-100)/SetLeftBottomText/SetRightBottomText` |
| `CXtoolUiComponentLoad` | 加载指示 | `SetText` |
| `CXtoolUiComponentHelpBox` | 帮助信息 | 继承 ClassifyBox + `SetReset/GetReset` |

### 容器/列表类

| 组件类 | 用途 | 关键方法 |
|--------|------|----------|
| `CXtoolUiComponentBox` | 通用容器 | `AddComponent/GetComponent/SetComponent/RemoveComponent/ClearComponent` |
| `CXtoolUiComponentSuperList` | 表格列表 | `SetTitle/AddRowObject/SetRowObject/SetColWidth/GetItemObject/SetItemObject` |
| `CXtoolUiComponentSuperListPro` | 增强表格列表 | `Init(cid)/SetTitle/AddRowObject/SetRowObject/SetWidthList/SetShowSearch/SetShowFreeze/DisableSelect/EnableBorder/GetRowCount` |
| `CXtoolUiComponentClassifyBox` | 分类容器 | `Init(cid)/InitObject(id)/SetObjectText/AddObjectComponent/GetSelected` |

### 交互/输入类

| 组件类 | 用途 | 关键方法 |
|--------|------|----------|
| `CXtoolUiComponentButton` | 按钮 | `Init(text,id)/SetText/Enable/SetId/GetId/SetColor/SetBgColor` |
| `CXtoolUiComponentExpandButton` | 展开按钮 | `Init(text,enable)/AddButton/SetButtonByIndex/GetButtonById` |
| `CXtoolUiComponentInput` | 文本输入 | `Init(cid)/SetTitle/SetText/GetText/Enable/SetMaxRow` |
| `CXtoolUiComponentComboBox` | 下拉选择 | `Init(cid)/SetTitle/AddOption/SetOption/GetOption/GetSelectedIndex/EnableInput/Enable` |
| `CXtoolUiComponentSelectBox` | 选择框(带列) | `Init(cid)/AddRowObject/GetRowObject/SetColWidth/AddTitle/SetShowSearch` |
| `CXtoolUiComponentSelect` | 选择器 | `Init(cid)/AddSelection/GetSelection/SetSelection/SetSelections` |
| `CXtoolUiComponentCheckBox` | 复选框 | `Init(cid)/GetState/SetState/Enable` |

### CXtoolUiComponentText::eIcon 枚举

```
ICON_NONE=0, ICON_WARNING=1, ICON_TICK=2, ICON_EXCLAMATION=3,
ICON_MIL_OFF=4, ICON_MIL_ON=5, ICON_BLUE_TIP=6, ICON_YELLOW_CAUTION=7, ICON_RED_WARNING=8
```

### CXtoolUiComponentSelectBox 关键类型

```cpp
enum eSelectionType { SELECTION_TYPE_SINGLE=0, SELECTION_TYPE_CHECK=1 };
enum eChoiceState { CHOICE_HIDEN=-1, CHOICE_NONE=0, CHOICE_SELECTED=1 };
struct tagRowObject {
    int radiusId;                        // 单选组 ID（同组互斥）
    eSelectionType selectionType;        // 单选 / 多选
    std::string text;                    // 行文本
    std::vector<std::string> vctTexts;   // 多列文本
    std::vector<int> vecChoicesState;    // 选中状态
};
```

### CXtoolUiComponentSuperListPro 关键类型

```cpp
struct tagRowObject {
    std::string backgroundColor;
    std::vector<CXtoolUiBaseComponent*> vctComponents;  // 行内组件列表
    void Init();
    void SetBackgroundColor(const string& strBgColor);
    void AddComponent(const CXtoolUiBaseComponent& component);
    void SetComponent(int iIndex, const CXtoolUiBaseComponent& component);
    const CXtoolUiBaseComponent* GetComponent(int iIndex);
    void ClearComponents();
};
```

---

## 6. 典型使用示例（基于 CCodeUiBuilder）

### 6.1 基本页面：文本 + 按钮 + 事件循环

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("操作确认");

// 添加带图标的警告文本
CXtoolUiComponentText tipText;
tipText.Init();
tipText.SetIcon(CXtoolUiComponentText::ICON_WARNING);
tipText.SetTitle("注意");
tipText.SetText("请确认是否继续执行操作？\n1) 关闭点火开关\n2) 等待30秒\n3) 重新打开点火开关");
tipText.SetAlign("left");
builder.AddComponent(tipText);

builder.AddButton(0x10, "确认");
builder.AddButton(0x20, "取消");

while (true)
{
    WORD wKey = builder.Show();
    if (KEY_ESC == wKey || 0x20 == wKey) {
        break;  // 返回/取消
    }
    if (0x10 == wKey) {
        // 执行操作...
        break;
    }
}
```

### 6.2 SuperListPro 表格：表头 + 数据行 + 列宽

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("版本信息");

CXtoolUiComponentSuperListPro tablePro;
tablePro.Init(0);
tablePro.SetShowFreeze(true);  // 冻结表头

CXtoolUiComponentSuperListPro::tagRowObject row;
CXtoolUiComponentText cellText;

// 表头行（带背景色）
row.Init();
cellText.SetAlign("left");
cellText.SetBold(true);
cellText.SetText("项目");
row.AddComponent(cellText);
cellText.SetAlign("center");
cellText.SetText("状态A");
row.AddComponent(cellText);
cellText.SetText("状态B");
row.AddComponent(cellText);
row.SetBackgroundColor("#6C7987");
tablePro.AddRowObject(row);

// 数据行
row.Init();
cellText.Init();
cellText.SetBold(false);
cellText.SetAlign("left");
cellText.SetText("ECU-001");
row.AddComponent(cellText);
cellText.SetAlign("center");
cellText.SetBold(true);
cellText.SetText("完成");
row.AddComponent(cellText);
cellText.SetText("等待");
row.AddComponent(cellText);
tablePro.AddRowObject(row);

// 设置列宽比例（总和100）
tablePro.SetWidthList({70, 15, 15});
builder.AddComponent(tablePro);

builder.AddButton(0x10, "确认");
builder.Show();
```

### 6.3 SelectBox 单选/多选列表

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("选择操作");

CXtoolUiComponentSelectBox selectBox;
selectBox.Init();
selectBox.AddTitle("请选择目标项");
selectBox.SetShowSearch(true);  // 启用搜索栏

// 添加单选项（radiusId 相同 → 同组互斥）
vector<string> options = {"选项 A", "选项 B", "选项 C"};
for (int i = 0; i < options.size(); ++i)
{
    CXtoolUiComponentSelectBox::tagRowObject row;
    row.radiusId = 0;  // 同一单选组
    row.selectionType = CXtoolUiComponentSelectBox::SELECTION_TYPE_SINGLE;
    row.text = options[i];
    row.vecChoicesState = {(i == 0) ?
        CXtoolUiComponentSelectBox::CHOICE_SELECTED :
        CXtoolUiComponentSelectBox::CHOICE_NONE};
    selectBox.AddRowObject(i, row);
}
selectBox.SetColWidth({85, 15});
builder.AddComponent(selectBox);

builder.AddButton(0x10, "确认");
builder.AddButton(0x20, "取消");

while (true)
{
    WORD wKey = builder.Show();
    if (KEY_ESC == wKey || 0x20 == wKey) break;
    if (0x10 == wKey)
    {
        // 读取用户选择结果
        auto* pSelectBox = static_cast<const CXtoolUiComponentSelectBox*>(builder.GetComponent(0));
        if (pSelectBox)
        {
            for (int i = 0; i < options.size(); ++i)
            {
                auto* pRow = pSelectBox->GetRowObject(i);
                if (pRow->vecChoicesState[0] == CXtoolUiComponentSelectBox::CHOICE_SELECTED)
                {
                    // options[i] 被选中
                }
            }
        }
        break;
    }
}
```

### 6.4 进度条实时刷新

```cpp
// 成员变量持有 builder，避免每次重建
CCodeUiBuilder m_progressBuilder;

// --- 初始化阶段 ---
void InitProgress(string strTitle, string strPrompt)
{
    m_progressBuilder.Init();
    m_progressBuilder.SetTitle(strTitle);
    m_progressBuilder.EnableKeyEsc(false);  // 禁止用户退出
    m_progressBuilder.ActiveRT(true);       // 启用实时刷新

    CXtoolUiComponentProgress progress;
    progress.Init();
    progress.SetPrompt(strPrompt);
    progress.SetProgress(0);
    m_progressBuilder.AddComponent(progress);
}

// --- 更新阶段（循环调用）---
void UpdateProgress(int iProgress)
{
    if (nullptr != m_progressBuilder.GetComponent(0))
    {
        // 取出 → 修改 → 写回
        CXtoolUiComponentProgress progress =
            *(static_cast<const CXtoolUiComponentProgress*>(m_progressBuilder.GetComponent(0)));
        progress.SetProgress(iProgress);
        m_progressBuilder.SetComponent(0, progress);
        m_progressBuilder.Show();
    }
}
```

### 6.5 加载状态页面（非阻塞）

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("系统初始化");
builder.ActiveRT(true);  // 非阻塞，Show 后立即返回

CXtoolUiComponentLoad loadIndicator;
loadIndicator.SetText("正在读取数据，请稍候...");
builder.AddComponent(loadIndicator);

builder.Show();  // 显示后立即返回，后台继续执行
// ... 执行耗时操作 ...
```

### 6.6 表单输入：SuperListPro + Input + ComboBox

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("信息录入");

CXtoolUiComponentSuperListPro formPro;
formPro.Init(0);
formPro.SetTitle("请填写以下信息");
CXtoolUiComponentSuperListPro::tagRowObject formRow;
CXtoolUiComponentText labelText;
CXtoolUiComponentInput inputField;
CXtoolUiComponentComboBox comboField;

// 文本输入行
formRow.Init();
labelText.Init();
labelText.SetAlign("left");
labelText.SetText("识别号码");
formRow.AddComponent(labelText);
inputField.Init(1);  // cid=1
inputField.SetText("");
formRow.AddComponent(inputField);
formPro.AddRowObject(formRow);

// 下拉选择行
formRow.Init();
labelText.Init();
labelText.SetAlign("left");
labelText.SetText("类型选择");
formRow.AddComponent(labelText);
comboField.Init(2);  // cid=2
comboField.AddOption("类型 A");
comboField.AddOption("类型 B");
comboField.SetText(comboField.GetOption(0));
formRow.AddComponent(comboField);
formPro.AddRowObject(formRow);

formPro.SetWidthList({40, 60});
builder.AddComponent(formPro);

builder.AddButton(0x10, "确认");
builder.AddButton(0x20, "取消");

while (true)
{
    WORD wKey = builder.Show();
    if (KEY_ESC == wKey || 0x20 == wKey) break;
    if (0x10 == wKey)
    {
        // 从 SuperListPro 中读取用户输入
        auto* pForm = static_cast<const CXtoolUiComponentSuperListPro*>(builder.GetComponent(0));
        if (pForm)
        {
            // 读取文本输入
            auto* pRow0 = pForm->GetRowObject(0);
            auto* pInput = static_cast<const CXtoolUiComponentInput*>(pRow0->GetComponent(1));
            string strInputValue = pInput->GetText();

            // 读取下拉选择
            auto* pRow1 = pForm->GetRowObject(1);
            auto* pCombo = static_cast<const CXtoolUiComponentComboBox*>(pRow1->GetComponent(1));
            int iSelectedIndex = pCombo->GetSelectedIndex();
        }
        break;
    }
}
```

### 6.7 多选列表（CHECK 模式）

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("多选操作");

CXtoolUiComponentSelectBox checkBox;
checkBox.Init();
checkBox.AddTitle("请勾选需要的项目");

vector<string> items = {"项目 A", "项目 B", "项目 C", "项目 D"};
for (int i = 0; i < items.size(); ++i)
{
    CXtoolUiComponentSelectBox::tagRowObject row;
    row.radiusId = i;  // CHECK 模式下每项独立
    row.selectionType = CXtoolUiComponentSelectBox::SELECTION_TYPE_CHECK;
    row.vctTexts.push_back(items[i]);
    row.vecChoicesState = {CXtoolUiComponentSelectBox::CHOICE_NONE};
    checkBox.AddRowObject(i, row);
}
checkBox.SetColWidth({85, 15});
builder.AddComponent(checkBox);

builder.AddButton(0x10, "确认");

while (true)
{
    WORD wKey = builder.Show();
    if (KEY_ESC == wKey) break;
    if (0x10 == wKey)
    {
        vector<string> selectedItems;
        auto* pBox = static_cast<const CXtoolUiComponentSelectBox*>(builder.GetComponent(0));
        if (pBox)
        {
            for (int i = 0; i < items.size(); ++i)
            {
                auto* pRow = pBox->GetRowObject(i);
                if (pRow->vecChoicesState[0] == CXtoolUiComponentSelectBox::CHOICE_SELECTED)
                {
                    selectedItems.push_back(items[i]);
                }
            }
        }
        break;
    }
}
```

### 6.8 动态更新表格内容

```cpp
CCodeUiBuilder builder;
builder.Init();
builder.SetTitle("状态监控");

// 初始创建空表格
CXtoolUiComponentSuperListPro tablePro;
tablePro.Init(0);
tablePro.SetWidthList({50, 50});
builder.AddComponent(tablePro);

builder.AddButton(0x10, "刷新");
builder.AddButton(0x20, "退出");

while (true)
{
    // 取出 → 重建内容 → 写回
    auto* pTable = static_cast<const CXtoolUiComponentSuperListPro*>(builder.GetComponent(0));
    if (pTable)
    {
        CXtoolUiComponentSuperListPro updatedTable = *pTable;
        updatedTable.Clear();

        CXtoolUiComponentSuperListPro::tagRowObject row;
        CXtoolUiComponentText cell;
        row.Init();
        cell.SetText("当前值");
        row.AddComponent(cell);
        char buf[16];
        sprintf(buf, "%d", rand() % 100);
        cell.SetText(buf);
        row.AddComponent(cell);
        updatedTable.AddRowObject(row);
        updatedTable.SetWidthList({50, 50});

        builder.SetComponent(0, updatedTable);
    }

    WORD wKey = builder.Show();
    if (KEY_ESC == wKey || 0x20 == wKey) break;
    // 0x10(刷新) 继续循环
}
```

---

## 7. 关键使用模式总结

| 模式 | 要点 |
|------|------|
| **组件读取** | `GetComponent()` 返回 `const` 基类指针，需 `static_cast` 转为具体类型后拷贝使用 |
| **组件更新** | 取出拷贝 → 修改 → `SetComponent(index, ...)` 写回 |
| **进度条** | builder 作为成员变量持有，`ActiveRT(true)` + `EnableKeyEsc(false)` + 循环 `SetComponent` + `Show()` |
| **加载页** | `ActiveRT(true)` + `CXtoolUiComponentLoad` + 单次 `Show()`，非阻塞 |
| **SelectBox 读取** | Show 返回按钮 id 后，GetComponent → static_cast → GetRowObject → 检查 `vecChoicesState[0]` |
| **表单输入** | SuperListPro 行内嵌 Input/ComboBox，Show 后通过 GetRowObject → GetComponent 读取值 |
| **列宽设置** | `SetWidthList({w1, w2, ...})` 或 `SetColWidth({w1, w2, ...})`，数值为百分比，总和应为 100 |
| **按钮 ID** | 自定义整数（如 0x10、0x20），Show() 返回对应 ID 标识用户点击 |
