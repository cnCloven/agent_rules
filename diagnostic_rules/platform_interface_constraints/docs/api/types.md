# 基础类型 API 速查 (binary.h / type.h)

> **头文件**: `D:\work\platform\inc\binary.h`, `D:\work\platform\inc\type.h`
> 平台核心数据类型定义，所有头文件的基础依赖。

---

## 1. 基础类型定义 (type.h)

| 类型 | 底层类型 | 说明 |
|------|---------|------|
| `BYTE` | `unsigned char` | 单字节 |
| `WORD` | `unsigned short` | 双字节 |
| `DWORD` | `unsigned long` | 四字节 |
| `UINT` | `unsigned int` | 无符号整型 |
| `INT` | `int` | 有符号整型 |
| `SHORT` | `short` | 短整型 |
| `LONG` | `long` | 长整型 |
| `FLOAT` | `float` | 浮点 |
| `BOOL` | `int` | 布尔值（TRUE=1, FALSE=0） |
| `CHAR` | `char` | 字符 |

常量：`TRUE=1`, `FALSE=0`, `NULL=0`

文件头结构 FILEHEADER（32字节）：
```cpp
typedef struct {
    BYTE file_flag[6];     // 文件标志
    BYTE pass_flag;        // 密码标志
    BYTE make_ver;         // 制作版本
    BYTE reserved[7];      // 保留
    UINT id_count;         // 索引ID数量
    BYTE id_length;        // ID长度
    BYTE pass_byte[12];    // 密码字节
} FILEHEADER;
```

---

## 2. CBinary — 二进制数据类

### 2.1 构造

| 构造方式 | 说明 |
|---------|------|
| `CBinary()` | 空构造 |
| `CBinary(WORD len)` | 指定长度（填0） |
| `CBinary(const char* buf, WORD len)` | 从字符串缓冲构造 |
| `CBinary(BYTE* buf, WORD len)` | 从字节缓冲构造 |
| `CBinary(const CBinary&)` | 拷贝构造 |

### 2.2 运算符

| 运算符 | 说明 |
|--------|------|
| `operator=` | 赋值 |
| `operator+=` (CBinary / BYTE) | 追加 |
| `operator+` (CBinary / BYTE) | 拼接（返回新对象） |
| `operator[]` (WORD) | 下标访问（读/写） |
| `==`, `<`, `<=`, `>`, `>=` | 比较 |

### 2.3 方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `GetAt(WORD index)` | `BYTE` | 获取指定位置字节 |
| `SetAt(WORD index, BYTE val)` | `void` | 设置指定位置字节 |
| `GetSize()` | `WORD` | 获取数据长度 |
| `IsEmpty()` | `BOOL` | 是否为空 |
| `Empty()` | `void` | 清空 |
| `GetBuffer()` | `BYTE*` | 获取原始缓冲区指针 |
| `AsString()` | `const char*` | 转为C字符串（const） |
| `ToString()` | `TString` | 转为TString |
| `Add(BYTE val)` | `void` | 末尾追加一个字节 |
| `Append(BYTE* buf, WORD len)` | `void` | 追加缓冲区 |
| `Append(const char* buf, WORD len)` | `void` | 追加字符缓冲区 |
| `RemoveAt(WORD index, WORD count=1)` | `void` | 删除指定位置 |
| `InsertAt(WORD index, BYTE val, WORD count=1)` | `void` | 在指定位置插入 |
| `ReadBuffer(BYTE* buf, WORD start=0, WORD len=0xFFFF)` | `WORD` | 读取到缓冲区 |
| `WriteBuffer(const char* buf, WORD len)` | `WORD` | 从缓冲区写入 |
| `Init(const void* buf, WORD len)` | `void` | 重新初始化 |

成员变量（public）：`m_pData`（BYTE*）, `m_nSize`（WORD）

---

## 3. TString — 平台字符串类

### 3.1 构造

| 构造方式 | 说明 |
|---------|------|
| `TString()` | 空构造 |
| `TString(const char*)` | 从C字符串构造 |
| `TString(const TString&)` | 拷贝构造 |

### 3.2 运算符

| 运算符 | 说明 |
|--------|------|
| `operator=` (TString / char / const char*) | 赋值 |
| `operator+=` (TString / char / const char*) | 追加 |
| `operator+` | 拼接（friend，支持多种组合） |
| `operator[]` (WORD) | 下标访问 |
| `==`, `!=`, `<`, `>`, `<=`, `>=` | 比较（friend） |

### 3.3 方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `GetLength()` | `WORD` | 获取长度 |
| `IsEmpty()` | `BOOL` | 是否为空 |
| `Empty()` | `void` | 清空 |
| `AsString()` | `const char*` | 转为C字符串 |
| `Mid(WORD pos=0, WORD n=0xFFFF)` | `TString` | 子串提取 |
| `Find(char ch)` / `Find(const char*)` | `int` | 查找（返回位置，未找到-1） |
| `ReverseFind(char ch)` | `int` | 反向查找 |
| `Replace(const char* src, const char* dest)` | `int` | 替换 |
| `Compare(const TString&)` / `Compare(const char*)` | `int` | 区分大小写比较 |
| `CompareNoCase(const TString&)` / `CompareNoCase(const char*)` | `int` | 忽略大小写比较 |
| `TrimLeft()` / `TrimRight()` / `Trim()` | `void` | 去除空白 |
| `MakeUpper()` / `MakeLower()` | `void` | 大小写转换 |
| `Append(const char*)` | `void` | 追加字符串 |
| `Delete(WORD index, int count=1)` | `void` | 删除字符 |
| `Insert(WORD index, const char*)` | `void` | 插入字符串 |

---

## 4. CGroup<TYPE> — 模板容器类

类似 `std::vector` 的轻量容器，常用特化：
- `CBinaryGroup` = `CGroup<CBinary>`
- `CStringGroup` = `CGroup<TString>`
- `CDWordGroup` = `CGroup<DWORD>`

### 4.1 方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `GetSize()` / `size()` | `WORD` | 获取元素数量 |
| `empty()` | `BOOL` | 是否为空 |
| `Empty()` / `clear()` | `void` | 清空 |
| `Add(TYPE val)` / `push_back(TYPE val)` / `push(TYPE val)` | `void` | 添加元素 |
| `GetAt(WORD index)` | `TYPE` | 获取元素 |
| `SetAt(WORD index, TYPE val)` | `void` | 设置元素 |
| `operator[]` (WORD) | `TYPE` / `TYPE&` | 下标访问 |
| `RemoveAt(WORD index, WORD count=1)` | `void` | 删除元素 |
| `InsertAt(WORD index, TYPE val, WORD count=1)` | `void` | 插入元素 |
| `SetSize(WORD newSize)` | `void` | 设置大小 |
| `pop()` | `void` | 移除末尾（栈操作） |
| `top()` | `TYPE` | 获取末尾（栈操作） |
| `operator=` | `void` | 赋值 |

---

## 5. 典型使用示例

### CBinary
```cpp
// 构造
CBinary bin("\x22\xF1\x90", 3);
// 追加
bin += CBinary("\x01", 1);
bin.Add(0x02);
// 访问
BYTE b = bin[0];         // 0x22
bin.SetAt(1, 0xFF);
// 比较
if (bin == CBinary("\x22\xFF\x90\x01\x02", 5)) { ... }
```

### TString
```cpp
TString str = "Hello";
str += " World";
int pos = str.Find("World");    // 6
TString sub = str.Mid(6, 5);   // "World"
str.MakeUpper();                // "HELLO WORLD"
str.Replace("WORLD", "CLAUDE");
```

### CGroup
```cpp
CGroup<int> nums;
nums.Add(10);
nums.Add(20);
nums.Add(30);
for (int i = 0; i < nums.GetSize(); i++) {
    debug("%d", nums[i]);
}

CBinaryGroup binGroup;
binGroup.Add(CBinary("\x01\x02", 2));
binGroup.Add(CBinary("\x03\x04", 2));
```
