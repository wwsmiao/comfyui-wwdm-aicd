# ComfyUI WWDM-AICD

ComfyUI 自定义节点集合，提供文本处理、正则提取、JSON 解析、AI 对话等功能。

**节点总数：22 个** | 类别：`wwdm-aicd`

---

## 目录

- [文本处理节点](#文本处理节点)
- [列表操作节点](#列表操作节点)
- [正则表达式节点](#正则表达式节点)
- [JSON 节点](#json-节点)
- [AI 节点](#ai-节点)

---

## 文本处理节点

### Text Concat — 文本连接

将多个文本字符串按分隔符连接成一个字符串。

**参数：**
- `str_a` / `str_b` / `str_c` / `str_d` — 输入文本
- `separator` — 连接分隔符，如 `,`、` `、`\n`

**示例：**
```
str_a: "苹果"  str_b: "香蕉"  separator: ", "  str_c: "橘子"
 → "苹果, 香蕉, 橘子"
```

---

### Text Split — 文本分割

按指定分隔符（非正则）将文本分割为字符串列表。

**参数：**
- `text` — 输入文本
- `delimiter` — 分隔符
- `max_split` — 最大分割次数（0=不限制）
- `trim` — 是否去除每段头尾空白

**示例：**
```
text: "苹果,香蕉,橘子"  delimiter: ","
 → ["苹果", "香蕉", "橘子"]

text: "a,b,c,d"  delimiter: ","  max_split: 2
 → ["a", "b", "c,d"]
```

---

### Text Substring — 子串截取

从文本中截取指定位置和长度的子串。

**参数：**
- `text` — 输入文本
- `clip_mode` — `start_len`（起止+长度）/ `start_end`（起止位置）/ `first_n`（前N个）/ `last_n`（后N个）
- `start` — 起始位置（支持负数）
- `length` — 截取长度（0=到末尾）
- `end` — 结束位置（start_end 模式）

**示例：**
```
text: "HelloWorld"  clip_mode: first_n  length: 5
 → "Hello"

text: "HelloWorld"  clip_mode: last_n  length: 3
 → "rld"
```

---

### Text Case — 大小写与命名法转换

将文本转换为各种大小写格式或编程命名风格。

**参数：**
- `text` — 输入文本
- `case` — 转换模式：
  - `upper` — 全大写
  - `lower` — 全小写
  - `title` — 单词首字母大写
  - `capitalize` — 首句大写
  - `swapcase` — 大小写翻转
  - `camel` — 驼峰命名（camelCase）
  - `pascal` — 帕斯卡命名（PascalCase）
  - `snake` — 下划线命名（snake_case）
  - `kebab` — 连字符命名（kebab-case）
  - `constant` — 常量命名（CONSTANT_CASE）
  - `sentence` — 首单词大写

**示例：**
```
text: "hello world"  case: upper → "HELLO WORLD"
text: "hello world"  case: camel → "helloWorld"
text: "hello world"  case: constant → "HELLO_WORLD"
```

---

### Text Replace — 字符串替换

执行简单字符串查找替换，无需正则知识。

**参数：**
- `text` — 输入文本
- `old_string` — 被替换的字符串
- `new_string` — 替换成的字符串
- `count` — 替换次数（0=全部）
- `ignore_case` — 是否忽略大小写

**示例：**
```
text: "Hello World"  old: "World"  new: "ComfyUI" → "Hello ComfyUI"
text: "a-b-c-d"      old: "-"      new: "/"      → "a/b/c/d"
text: "a-b-c-d"      old: "-"      new: "+"  count: 2 → "a+b+c-d"
```

---

### Text Trim — 文本修剪

去除文本头尾空白、合并多余空白、按行修剪。

**参数：**
- `text` — 输入文本
- `mode` — 修剪模式：
  - `trim` — 去除头尾空白
  - `ltrim` — 仅去除左侧
  - `rtrim` — 仅去除右侧
  - `collapse` — 合并连续空白为单空格
  - `strip_lines` — 每行修剪 + 移除空行
  - `remove_blank_lines` — 只移除空行
- `chars` — 要移除的字符（可选）

**示例：**
```
text: "  Hello World  "  mode: trim      → "Hello World"
text: "Hello    World"   mode: collapse  → "Hello World"
```

---

### Text Template — 模板格式化

使用占位符模板生成文本。支持 `{0}`, `{1}` 位置占位符。

**参数：**
- `template` — 模板字符串，包含 `{0}` `{1}` 等占位符
- `arg0` / `arg1` / `arg2` / `arg3` — 占位符值

**示例：**
```
template: "你好 {0}，你 {1} 吗？"
arg0: "张三"  arg1: "吃饭"
 → "你好 张三，你 吃饭 吗？"
```

---

### Text Pad — 文本填充

将文本填充到指定宽度，支持左/右/居中对齐。

**参数：**
- `text` — 输入文本
- `mode` — `left` / `right` / `center`
- `width` — 目标宽度
- `pad_char` — 填充字符（默认空格）

**示例：**
```
text: "123"  mode: right  width: 6  pad_char: "0"  → "000123"
text: "Hi"   mode: center width: 9  pad_char: "-"  → "---Hi----"
```

---

### Text Search — 文本搜索

在文本中搜索子串，支持统计、定位、行匹配。

**参数：**
- `text` — 被搜索的文本
- `search_for` — 要搜索的字符串
- `mode` — 搜索模式：
  - `contains` — 是否包含（返回 "true"/"false"）
  - `count` — 统计出现次数
  - `find_first` — 首次出现位置索引
  - `find_all` — 所有位置的索引列表
  - `find_lines` — 返回包含搜索文本的所有行
- `ignore_case` — 忽略大小写

**示例：**
```
text: "abc abc"  mode: count     search_for: "ab" → 2
text: "第1行\n关键行\n第3行"  mode: find_lines  search_for: "关键" → ["关键行"]
```

---

### Text Length — 文本统计

统计文本的字符数、词数、行数、字节大小。

**参数：**
- `text` — 输入文本
- `output` — `summary`（全部）/ `char_count` / `word_count` / `line_count` / `byte_size`

**输出：** `(STRING, INT)` — 文本描述 + 字符数

**示例：**
```
text: "Hello World 你好"
 → "字符数: 15 | 词数: 3 | 行数: 1 | 字节: 17", 15
```

---

### Text Judge — 文本判断

对文本进行各种条件判断，返回布尔结果。

**参数：**
- `input_a` — 输入文本 A
- `operator` — 操作符：
  - `equals` / `not_equals` — 相等/不等
  - `contains` / `not_contains` — 包含/不包含
  - `starts_with` / `ends_with` — 首/尾匹配
  - `is_empty` / `not_empty` — 是否为空
  - `is_digit` / `is_alpha` / `is_alnum` — 字符类型判断
  - `length_gt` / `length_lt` / `length_eq` — 长度比较
- `input_b` — 比较值/文本 B
- `invert` — 反转结果

**输出：** `(STRING, BOOLEAN)` — "true"/"false" + 布尔值

**示例：**
```
input_a: ""  operator: is_empty → "true", True
input_a: "hello"  operator: length_gt  input_b: "3" → "true", True
```

---

### Text Filter Lines — 文本行过滤

对多行文本按行进行 grep 式过滤。

**参数：**
- `text` — 多行文本
- `pattern` — 匹配字符串
- `mode` — `grep`（保留匹配行）/ `grep_v`（排除匹配行）
- `match` — 匹配方式：`contains` / `regex` / `starts` / `ends` / `equals`
- `ignore_case` — 忽略大小写
- `trim_lines` — 过滤前修剪空白

**示例：**
```
text: "苹果\n香蕉\n葡萄\n草莓"  pattern: "莓"  mode: grep
 → ["草莓"]

text: "error: 文件未找到\ninfo: 加载中\nwarning: 磁盘不足"
pattern: "error"  mode: grep_v
 → ["info: 加载中", "warning: 磁盘不足"]
```

---

### Text Wrap — 文本折行

将长文本按指定宽度折行为多行。

**参数：**
- `text` — 输入文本
- `width` — 每行最大字符数
- `break_long_words` — 是否打断长单词

**示例：**
```
text: "这是一个很长的句子"  width: 5
 → ["这是一", "个很长", "的句子"]
```

---

### Text Random — 随机文本选择

从多个候选项中随机选择一个或多个文本。

**参数：**
- `option_a` ~ `option_e` — 候选项
- `count` — 选择数量（1=单选，0=全部）
- `seed` — 随机种子（0=随机，>0=固定种子保证可复现）

**示例：**
```
option_a: "苹果"  option_b: "香蕉"  option_c: "橘子"
count: 1
 → 随机输出 ["苹果"] 或 ["香蕉"] 或 ["橘子"]
```

---

### Text Escape — 文本转义/反转义

对文本进行转义或反转义处理。

**参数：**
- `text` — 输入文本
- `mode` — 操作模式：
  - `escape_json` / `unescape_json` — JSON 转义/反转义
  - `escape_html` / `unescape_html` — HTML 转义/反转义
  - `escape_url` / `unescape_url` — URL 编码/解码
  - `escape_unicode` / `unescape_unicode` — Unicode 转义
  - `add_slashes` / `strip_slashes` — 反斜杠转义

**示例：**
```
text: '她说："你好"'  mode: escape_json
 → '她说：\"你好\"'

text: "<script>alert('xss')</script>"  mode: escape_html
 → "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
```

---

### Text Multi Concat — 多路文本连接

连接任意字符串列表。支持简单拼接、按位配对、笛卡尔积。

**参数：**
- `list_a` / `list_b` — 字符串列表输入
- `separator` — 连接分隔符
- `mode` — 连接模式：
  - `concat` — 简单连接所有元素
  - `zip` — 按位置配对连接（A[0]+sep+B[0], A[1]+sep+B[1]...）
  - `cross` — 笛卡尔积（A₀×B₀, A₀×B₁, A₁×B₀, A₁×B₁...）

**示例：**
```
list_a: ["name", "age"]  list_b: ["张三", "25"]  mode: zip  separator: ": "
 → ["name: 张三", "age: 25"]
```

---

## 列表操作节点

### List Ops — 列表操作

对字符串列表进行排序、反转、去重、随机打乱、分块等操作。

**参数：**
- `items` — 输入列表
- `operation` — 操作模式：
  - `join` — 连接为单个字符串（`param` 为分隔符）
  - `sort` / `sort_desc` — 字母排序/倒序
  - `reverse` — 反转顺序
  - `dedupe` / `unique` — 去重
  - `shuffle` — 随机打乱（可设 `seed`）
  - `chunk` — 按 `param` 大小分块
  - `sort_by_length` — 按字符串长度排序
  - `take` — 取前 N 个
  - `skip` — 跳过前 N 个

**示例：**
```
items: ["c", "a", "b"]  operation: sort
 → ["a", "b", "c"]

items: ["a", "b", "c"]  operation: join  param: ", "
 → "a, b, c"

items: ["1", "2", "3"]  operation: shuffle  seed: 42
 → ["3", "1", "2"]  (固定种子，可复现)
```

---

## 正则表达式节点

### Txt Reg — 正则表达式提取

使用正则表达式从文本中提取、替换或分割内容。

**参数：**
- `text` — 输入文本
- `pattern` — 正则表达式模式
- `mode` — 处理模式：
  - `extract_all` — 提取所有匹配项
  - `extract_group` — 提取指定分组
  - `replace` — 正则替换
  - `split` — 正则分割
  - `match_first` — 仅提取第一个匹配
- `group_index` — 分组索引
- `replacement` — 替换字符串
- `flags` — 正则标志：`i`(忽略大小写) `m`(多行) `s`(点匹配换行) `x`(详细模式) `a`(ASCII)
- `max_matches` — 最大匹配数（0=不限）
- `dedupe` — 是否去重
- `output_mode` — `list` / `join`

**示例：**
```
text: "订单号123，金额456元，数量789件"  pattern: "\d+"  mode: extract_all
 → ["123", "456", "789"]

text: "手机号13812345678"  pattern: "(\d{3})\d{4}(\d{4})"
mode: replace  replacement: "\1****\2"
 → ["手机号138****5678"]
```

---

### Txt Reg Select — 列表选择

对列表进行灵活选择，支持单选、多选、范围、条件过滤等。

**参数：**
- `items` — 输入列表
- `select_mode` — `all` / `single` / `multiple` / `range` / `filter` / `head_tail`
- `index` — 单选索引
- `indices` — 多选索引列表，如 "0,2,4"
- `filter_pattern` — 过滤匹配字符串
- `filter_mode` — `contains` / `not_contains` / `regex` / `starts` / `ends`

**示例：**
```
items: ["a", "b", "c", "d", "e"]  select_mode: range  start: 1  end: 3
 → ["b", "c", "d"]

items: ["apple", "banana", "apricot"]  select_mode: filter
filter_pattern: "ap"  filter_mode: contains
 → ["apple", "apricot"]
```

---

## JSON 节点

### Json Parser — JSON 解析

解析 JSON 字符串，支持路径提取、键值提取、数组操作、条件查询。

**参数：**
- `json_text` — JSON 字符串
- `mode` — 解析模式：
  - `auto` — 自动识别
  - `path` — 按路径提取（支持 `.key` 和 `[index]` 语法）
  - `keys` — 递归提取所有键名
  - `values` — 递归提取所有叶节点值
  - `extract_keys` — 按键名提取值（推荐，递归遍历）
  - `array_items` — 提取数组元素
  - `flatten` — 展平嵌套结构
  - `query` — 条件查询（支持 `==`/`!=`/`>`/`<`/`contains`/`starts`/`ends`）
- `path` — JSON 路径
- `extract_key_names` — 要提取的键名（多个用逗号分隔）

**示例 — 按键名提取：**
```json
{
  "ch1": {"姓名": "小美", "中文提示词": "一个美丽的女人"},
  "ch2": {"姓名": "小帅", "中文提示词": "一个帅气的男人"}
}
mode: extract_keys  extract_key_names: "中文提示词"
结果: ["一个美丽的女人", "一个帅气的男人"]
```

**示例 — 条件查询：**
```json
[{"name": "张三", "age": 20}, {"name": "李四", "age": 30}]
mode: query  path: "age>25"
结果: ['{"name": "李四", "age": 30}']
```

---

### Json Builder — JSON 构建

从键值对列表构建 JSON 字符串。

**参数：**
- `keys` — 键名列表
- `values` — 值列表
- `mode` — `object`（简单对象）/ `array_of_objects`（对象数组）/ `nested`（嵌套对象）

**示例：**
```
keys: ["name", "age", "city"]  values: ["张三", "25", "北京"]  mode: object
 → {"name": "张三", "age": "25", "city": "北京"}
```

---

## AI 节点

### AI Chat API — 远程 AI 对话

调用 DeepSeek / 通义千问 / 豆包 等大模型 API，支持图+文多模态输入。

**参数：**
- `provider` — 供应商：`deepseek` / `qwen` / `doubao`
- `api_key` — API 密钥
- `model` — 模型名（留空使用默认值）
- `system_prompt` — 系统提示词
- `user_prompt` — 用户提示词
- `max_tokens` — 最大生成 token 数
- `temperature` — 温度（0.0~2.0）
- `images` — 可选图片输入（IMAGE 张量）

**预配端点：**
| 供应商 | 端点 | 默认模型 |
|---|---|---|
| DeepSeek | `api.deepseek.com/v1` | `deepseek-chat` |
| 通义千问 | `dashscope.aliyuncs.com` (OpenAI 兼容) | `qwen-plus` |
| 豆包 | `ark.cn-beijing.volces.com` | `doubao-pro-32k` |

---

## 安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/wwsmiao/comfyui-wwdm-aicd.git
pip install -r comfyui-wwdm-aicd/requirements.txt
```

重启 ComfyUI 即可使用。所有节点在右键菜单中的 **`wwdm-aicd`** 类别下。

---

## 典型工作流

**文本处理管线：**
```
TxtReg (正则提取→列表)
    ↓
TxtRegSelect (筛选)
    ↓
JsonBuilder (结构化)
    ↓
TextTemplate (格式化输出)
```

**文本清洗：**
```
TextTrim (修剪空白)
    ↓
TextReplace (替换符号)
    ↓
TextCase (统一大小写)
    ↓
TextLength (验证长度)
```

**数据抽取：**
```
AIChatAPI (LLM 输出)
    ↓
TextFilterLines (按行过滤)
    ↓
TextSplit (分割)
    ↓
JsonParser (JSON 解析取字段)
```

---

## 许可证

MIT License
