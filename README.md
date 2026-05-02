# ComfyUI WWDM-AICD

ComfyUI 自定义节点集合，提供文本正则提取、JSON解析等功能。

## 节点列表

### TxtReg - 正则表达式提取

使用正则表达式从文本中提取、替换或分割内容。

**参数：**
- `text` - 输入文本
- `pattern` - 正则表达式模式
- `mode` - 处理模式：`extract_all` / `extract_group` / `replace` / `split` / `match_first`
- `group_index` - 分组索引
- `replacement` - 替换字符串
- `flags` - 正则标志：`i`(忽略大小写) `m`(多行) `s`(点匹配换行)
- `max_matches` - 最大匹配数量
- `dedupe` - 是否去重

**示例：**
```
输入: "订单号123，金额456元"
模式: \d+
结果: ["123", "456"]
```

### TxtRegSelect - 列表选择

对列表进行灵活选择，支持单选、多选、范围选择、条件过滤。

**参数：**
- `select_mode` - `all` / `single` / `multiple` / `range` / `filter` / `head_tail`
- `index` - 单选索引
- `indices` - 多选索引列表，如 "0,2,4"
- `filter_pattern` - 过滤匹配字符串
- `filter_mode` - `contains` / `not_contains` / `regex` / `starts` / `ends`

### JsonParser - JSON解析

解析JSON字符串，支持路径提取、按键名提取值、条件查询等。

**参数：**
- `mode` - 解析模式：
  - `auto` - 自动识别
  - `path` - 按路径提取
  - `keys` - 提取所有键名
  - `values` - 提取所有值
  - `extract_keys` - 按键名提取值（推荐）
  - `array_items` - 提取数组元素
  - `flatten` - 展平嵌套结构
  - `query` - 条件查询
- `path` - JSON路径，支持 `.key` 和 `[index]` 语法
- `extract_key_names` - 要提取的键名，多个用逗号分隔

**示例 - 按键名提取：**
```json
输入JSON:
{
  "ch1": {"姓名": "小美", "中文提示词": "一个美丽的女人"},
  "ch2": {"姓名": "小帅", "中文提示词": "一个帅气的男人"}
}

mode: extract_keys
extract_key_names: 中文提示词
结果: ["一个美丽的女人", "一个帅气的男人"]
```

### JsonBuilder - JSON构建

从键值对列表构建JSON字符串。

**参数：**
- `keys` - 键名列表
- `values` - 值列表
- `mode` - `object` / `array_of_objects` / `nested`

## 安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/wwsmiao/comfyui-wwdm-aicd.git
```

重启 ComfyUI 即可使用。

## 许可证

MIT License
