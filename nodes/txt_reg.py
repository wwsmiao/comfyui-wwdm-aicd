import re
import json
from typing import Any


class TxtReg:
    """
    正则表达式提取节点
    
    功能说明：
        使用正则表达式从文本中提取、替换或分割内容。
        支持多种匹配模式、分组提取、正则标志等功能。
    
    参数说明：
        text        - 输入文本（支持多行）
        pattern     - 正则表达式模式
        mode        - 处理模式：
                      - extract_all: 提取所有匹配项
                      - extract_group: 提取指定分组
                      - replace: 正则替换
                      - split: 正则分割
                      - match_first: 仅提取第一个匹配
        group_index - 分组索引（用于 extract_group 模式）
        replacement - 替换字符串（用于 replace 模式）
        output_mode - 输出格式：list（列表）或 join（连接为字符串）
        join_separator - 连接分隔符（output_mode=join 时使用）
        flags       - 正则标志：i(忽略大小写) m(多行) s(点匹配换行) x(详细模式)
        max_matches - 最大匹配数量（0表示不限制）
        dedupe      - 是否去重
    
    使用示例：
        示例1 - 提取所有数字：
            text: "订单号123，金额456元，数量789件"
            pattern: "\\d+"
            mode: extract_all
            结果: ["123", "456", "789"]
        
        示例2 - 提取邮箱域名（分组）：
            text: "联系邮箱：test@gmail.com 和 admin@qq.com"
            pattern: "@([\\w.]+)"
            mode: extract_group
            group_index: 0
            结果: ["gmail.com", "qq.com"]
        
        示例3 - 正则替换：
            text: "手机号13812345678和13987654321"
            pattern: "(\\d{3})\\d{4}(\\d{4})"
            mode: replace
            replacement: "\\1****\\2"
            结果: ["手机号138****5678和139****4321"]
        
        示例4 - 正则分割：
            text: "apple123banana456cherry"
            pattern: "\\d+"
            mode: split
            结果: ["apple", "banana", "cherry"]
        
        示例5 - 忽略大小写匹配：
            text: "Hello HELLO hello"
            pattern: "hello"
            mode: extract_all
            flags: i
            结果: ["Hello", "HELLO", "hello"]
        
        示例6 - 提取URL：
            text: "访问 https://example.com 或 http://test.org/page"
            pattern: "https?://[^\\s]+"
            mode: extract_all
            结果: ["https://example.com", "http://test.org/page"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "pattern": ("STRING", {"multiline": False, "default": r"\d+"}),
                "mode": (
                    ["extract_all", "extract_group", "replace", "split", "match_first"],
                    {"default": "extract_all"},
                ),
                "group_index": ("INT", {"default": 0, "min": 0}),
                "replacement": ("STRING", {"multiline": False, "default": ""}),
                "output_mode": (
                    ["list", "join"],
                    {"default": "list"},
                ),
                "join_separator": ("STRING", {"multiline": False, "default": ","}),
            },
            "optional": {
                "flags": ("STRING", {"multiline": False, "default": ""}),
                "max_matches": ("INT", {"default": 0, "min": 0}),
                "dedupe": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "process"
    CATEGORY = "wwdm-aicd"

    def _parse_flags(self, flags_str: str) -> int:
        """解析正则标志字符串"""
        flags = 0
        flag_map = {
            "i": re.IGNORECASE,
            "m": re.MULTILINE,
            "s": re.DOTALL,
            "x": re.VERBOSE,
            "a": re.ASCII,
        }
        for char in flags_str.lower():
            if char in flag_map:
                flags |= flag_map[char]
        return flags

    def process(
        self,
        text: str,
        pattern: str,
        mode: str,
        group_index: int,
        replacement: str,
        output_mode: str,
        join_separator: str,
        flags: str = "",
        max_matches: int = 0,
        dedupe: bool = False,
    ) -> tuple:
        if not text:
            return ([],) if output_mode == "list" else ([""],)

        if not pattern:
            return ([text],) if output_mode == "list" else ([text],)

        regex_flags = self._parse_flags(flags)

        try:
            compiled = re.compile(pattern, regex_flags)
        except re.error:
            return ([],) if output_mode == "list" else ([""],)

        result = []

        if mode == "extract_all":
            matches = compiled.findall(text)
            if max_matches > 0:
                matches = matches[:max_matches]
            result = [str(m) for m in matches]

        elif mode == "extract_group":
            matches = compiled.finditer(text)
            for i, match in enumerate(matches):
                if max_matches > 0 and i >= max_matches:
                    break
                groups = match.groups()
                if groups:
                    if 0 <= group_index < len(groups):
                        result.append(str(groups[group_index]))
                    elif group_index == 0 and groups[0]:
                        result.append(str(groups[0]))
                else:
                    result.append(match.group(0))

        elif mode == "replace":
            result = [compiled.sub(replacement, text)]

        elif mode == "split":
            parts = compiled.split(text)
            result = [p for p in parts if p]

        elif mode == "match_first":
            match = compiled.search(text)
            if match:
                result = [match.group(0)]
            else:
                result = []

        # 去重
        if dedupe and result:
            seen = set()
            unique_result = []
            for item in result:
                if item not in seen:
                    seen.add(item)
                    unique_result.append(item)
            result = unique_result

        if not result:
            return ([],) if output_mode == "list" else ([""],)

        if output_mode == "join":
            return ([join_separator.join(result)],)

        return (result,)


class TxtRegSelect:
    """
    列表选择节点
    
    功能说明：
        对列表进行灵活选择，支持单选、多选、范围选择、条件过滤等。
        通常与 TxtReg 节点配合使用，对正则提取结果进行筛选。
    
    参数说明：
        items          - 输入列表（接收上游节点的列表输出）
        select_mode    - 选择模式：
                         - all: 返回全部元素
                         - single: 返回单个元素
                         - multiple: 返回多个指定索引的元素
                         - range: 返回指定范围的元素
                         - filter: 条件过滤
                         - head_tail: 取头部和尾部元素
        index          - 单选索引（select_mode=single 时使用）
        indices        - 多选索引列表，如 "0,2,4"（select_mode=multiple 时使用）
        start_index    - 范围起始索引（select_mode=range 时使用）
        end_index      - 范围结束索引，闭区间（select_mode=range 时使用）
        filter_pattern - 过滤匹配字符串（select_mode=filter 时使用）
        filter_mode    - 过滤模式：
                         - contains: 包含
                         - not_contains: 不包含
                         - regex: 正则匹配
                         - starts: 开头匹配
                         - ends: 结尾匹配
        head_count     - 头部取N个元素
        tail_count     - 尾部取N个元素
    
    使用示例：
        示例1 - 单选第3个元素：
            items: ["a", "b", "c", "d", "e"]
            select_mode: single
            index: 2
            结果: ["c"]
        
        示例2 - 多选指定索引：
            items: ["a", "b", "c", "d", "e"]
            select_mode: multiple
            indices: "0,2,4"
            结果: ["a", "c", "e"]
        
        示例3 - 范围选择：
            items: ["a", "b", "c", "d", "e"]
            select_mode: range
            start_index: 1
            end_index: 3
            结果: ["b", "c", "d"]
        
        示例4 - 条件过滤（包含）：
            items: ["apple", "banana", "cherry", "apricot"]
            select_mode: filter
            filter_pattern: "ap"
            filter_mode: contains
            结果: ["apple", "apricot"]
        
        示例5 - 正则过滤：
            items: ["test123", "hello", "data456", "world"]
            select_mode: filter
            filter_pattern: "\\d+"
            filter_mode: regex
            结果: ["test123", "data456"]
        
        示例6 - 取头部和尾部：
            items: ["a", "b", "c", "d", "e"]
            select_mode: head_tail
            head_count: 2
            tail_count: 1
            结果: ["a", "b", "e"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "items": ("STRING", {"INPUT_IS_LIST": True}),
                "select_mode": (
                    ["all", "single", "multiple", "range", "filter", "head_tail"],
                    {"default": "all"},
                ),
                "index": ("INT", {"default": 0, "min": 0}),
                "indices": ("STRING", {"multiline": False, "default": "0,1,2"}),
                "start_index": ("INT", {"default": 0, "min": 0}),
                "end_index": ("INT", {"default": 0, "min": 0}),
            },
            "optional": {
                "filter_pattern": ("STRING", {"multiline": False, "default": ""}),
                "filter_mode": (["contains", "not_contains", "regex", "starts", "ends"], {"default": "contains"}),
                "head_count": ("INT", {"default": 1, "min": 0}),
                "tail_count": ("INT", {"default": 1, "min": 0}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "select"
    CATEGORY = "wwdm-aicd"

    def select(
        self,
        items: list,
        select_mode: str,
        index: int,
        indices: str,
        start_index: int,
        end_index: int,
        filter_pattern: str = "",
        filter_mode: str = "contains",
        head_count: int = 1,
        tail_count: int = 1,
    ) -> tuple:
        if not items:
            return ([],)

        length = len(items)

        if select_mode == "all":
            return (items,)

        if select_mode == "single":
            if 0 <= index < length:
                return ([items[index]],)
            return ([],)

        if select_mode == "multiple":
            selected = []
            for part in indices.split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    idx = int(part)
                    if 0 <= idx < length:
                        selected.append(items[idx])
                except ValueError:
                    continue
            return (selected,)

        if select_mode == "range":
            start = max(0, start_index)
            end = min(length - 1, end_index)
            if start > end:
                return ([],)
            return (items[start : end + 1],)

        if select_mode == "filter":
            if not filter_pattern:
                return (items,)
            filtered = []
            for item in items:
                if filter_mode == "contains":
                    if filter_pattern in item:
                        filtered.append(item)
                elif filter_mode == "not_contains":
                    if filter_pattern not in item:
                        filtered.append(item)
                elif filter_mode == "starts":
                    if item.startswith(filter_pattern):
                        filtered.append(item)
                elif filter_mode == "ends":
                    if item.endswith(filter_pattern):
                        filtered.append(item)
                elif filter_mode == "regex":
                    try:
                        if re.search(filter_pattern, item):
                            filtered.append(item)
                    except re.error:
                        pass
            return (filtered,)

        if select_mode == "head_tail":
            result = []
            if head_count > 0:
                result.extend(items[:head_count])
            if tail_count > 0:
                result.extend(items[-tail_count:] if tail_count <= length else items)
            return (result,)

        return (items,)


class JsonParser:
    """
    JSON解析节点
    
    功能说明：
        解析JSON字符串，支持路径提取、键值提取、数组操作、条件查询等功能。
        适用于API响应解析、配置文件读取、数据提取等场景。
    
    参数说明：
        json_text          - JSON格式字符串
        mode               - 解析模式：
                             - auto: 自动识别，返回所有值
                             - path: 按路径提取
                             - keys: 提取所有键名
                             - values: 提取所有值
                             - extract_keys: 按键名提取值（推荐）
                             - array_items: 提取数组元素
                             - flatten: 展平嵌套结构
                             - query: 条件查询
        path               - JSON路径，支持 .key 和 [index] 语法
        extract_key_names  - 要提取的键名列表，多个用逗号分隔（mode=extract_keys 时使用）
        array_index        - 数组索引（-1表示全部）
        key_filter         - 键名过滤字符串
        value_filter       - 值过滤字符串
        flatten_separator  - 展平时的分隔符
        output_mode        - 输出格式：list 或 join
        join_separator     - 连接分隔符
    
    路径语法：
        data.users[0].name  - 访问 data.users 数组第一个元素的 name
        response.result.items - 访问嵌套对象
        [0]                  - 访问数组第一个元素
    
    查询语法（mode=query）：
        name==张三          - 等于
        age>18             - 大于
        price<=100         - 小于等于
        email contains @   - 包含
        url starts http    - 开头匹配
    
    使用示例：
        示例1 - 自动提取值：
            json_text: {"name": "张三", "age": 25, "city": "北京"}
            mode: auto
            结果: ["张三", "25", "北京"]
        
        示例2 - 路径提取：
            json_text: {"data": {"users": [{"name": "张三"}, {"name": "李四"}]}}
            mode: path
            path: data.users
            结果: ['{"name": "张三"}', '{"name": "李四"}']
        
        示例3 - 提取数组特定元素：
            json_text: {"items": ["apple", "banana", "cherry"]}
            mode: array_items
            path: items
            array_index: 1
            结果: ["banana"]
        
        示例4 - 提取所有键：
            json_text: {"user": {"name": "张三", "profile": {"age": 25}}}
            mode: keys
            结果: ["user", "user.name", "user.profile", "user.profile.age"]
        
        示例5 - 条件查询：
            json_text: [{"name": "张三", "age": 20}, {"name": "李四", "age": 30}]
            mode: query
            path: age>25
            结果: ['{"name": "李四", "age": 30}']
        
        示例6 - 展平嵌套结构：
            json_text: {"user": {"name": "张三", "age": 25}}
            mode: flatten
            结果: ["user.name: 张三", "user.age: 25"]
        
        示例7 - 提取嵌套值：
            json_text: {"response": {"data": {"items": [{"id": 1}, {"id": 2}]}}}
            mode: path
            path: response.data.items[0].id
            结果: ["1"]
        
        示例8 - 按键名提取值（推荐）：
            json_text: {"ch1": {"姓名": "小美", "中文提示词": "一个美丽的女人"}, 
                        "ch2": {"姓名": "小帅", "中文提示词": "一个帅气的男人"}}
            mode: extract_keys
            extract_key_names: 中文提示词
            结果: ["一个美丽的女人", "一个帅气的男人"]
        
        示例9 - 提取多个键名的值：
            json_text: {"ch1": {"name": "张三", "age": 20}, "ch2": {"name": "李四", "age": 25}}
            mode: extract_keys
            extract_key_names: name,age
            结果: ["张三", "20", "李四", "25"]
        
        示例10 - 从嵌套数组中按键名提取：
            json_text: {"data": [{"name": "张三"}, {"name": "李四"}, {"name": "王五"}]}
            mode: extract_keys
            extract_key_names: name
            结果: ["张三", "李四", "王五"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_text": ("STRING", {"multiline": True, "default": ""}),
                "mode": (
                    ["auto", "path", "keys", "values", "extract_keys", "array_items", "flatten", "query"],
                    {"default": "auto"},
                ),
                "path": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {
                "extract_key_names": ("STRING", {"multiline": False, "default": ""}),
                "array_index": ("INT", {"default": -1, "min": -1}),
                "key_filter": ("STRING", {"multiline": False, "default": ""}),
                "value_filter": ("STRING", {"multiline": False, "default": ""}),
                "flatten_separator": ("STRING", {"multiline": False, "default": "."}),
                "output_mode": (["list", "join"], {"default": "list"}),
                "join_separator": ("STRING", {"multiline": False, "default": ","}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "parse"
    CATEGORY = "wwdm-aicd"

    def _get_by_path(self, data: Any, path: str) -> Any:
        """通过路径获取值，支持 . 和 [] 语法"""
        if not path:
            return data

        parts = re.split(r'\.|\[|\]', path)
        parts = [p for p in parts if p]

        current = data
        for part in parts:
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return None
                except ValueError:
                    return None
            else:
                return None
        return current

    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        """展平嵌套字典"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self._flatten_dict(item, f"{new_key}[{i}]", sep).items())
                    else:
                        items.append((f"{new_key}[{i}]", item))
            else:
                items.append((new_key, v))
        return dict(items)

    def _extract_all_values(self, data: Any, result: list) -> None:
        """递归提取所有值"""
        if isinstance(data, dict):
            for v in data.values():
                self._extract_all_values(v, result)
        elif isinstance(data, list):
            for item in data:
                self._extract_all_values(item, result)
        else:
            result.append(str(data))

    def _extract_all_keys(self, data: Any, result: list, prefix: str = "") -> None:
        """递归提取所有键"""
        if isinstance(data, dict):
            for k, v in data.items():
                full_key = f"{prefix}.{k}" if prefix else k
                result.append(full_key)
                self._extract_all_keys(v, result, full_key)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._extract_all_keys(item, result, f"{prefix}[{i}]")

    def _extract_values_by_key_names(self, data: Any, key_names: list, result: list) -> None:
        """按键名列表提取所有匹配的值（递归遍历）"""
        if isinstance(data, dict):
            for k, v in data.items():
                if k in key_names:
                    if isinstance(v, (dict, list)):
                        result.append(json.dumps(v, ensure_ascii=False))
                    else:
                        result.append(str(v))
                # 继续递归查找
                self._extract_values_by_key_names(v, key_names, result)
        elif isinstance(data, list):
            for item in data:
                self._extract_values_by_key_names(item, key_names, result)

    def _query_json(self, data: Any, query: str) -> list:
        """简单查询语法：key==value, key!=value, key>value 等"""
        result = []
        items = data if isinstance(data, list) else [data]

        for item in items:
            if not isinstance(item, dict):
                continue

            match = re.match(r'(\w+)\s*(==|!=|>|<|>=|<=|contains|starts|ends)\s*(.+)', query.strip())
            if not match:
                continue

            key, op, value = match.groups()
            val = item.get(key)

            if val is None:
                continue

            # 尝试数值比较
            try:
                num_val = float(val)
                num_query = float(value)
                if op == ">" and num_val > num_query:
                    result.append(item)
                elif op == "<" and num_val < num_query:
                    result.append(item)
                elif op == ">=" and num_val >= num_query:
                    result.append(item)
                elif op == "<=" and num_val <= num_query:
                    result.append(item)
                continue
            except (ValueError, TypeError):
                pass

            # 字符串比较
            str_val = str(val)
            if op == "==" and str_val == value:
                result.append(item)
            elif op == "!=" and str_val != value:
                result.append(item)
            elif op == "contains" and value in str_val:
                result.append(item)
            elif op == "starts" and str_val.startswith(value):
                result.append(item)
            elif op == "ends" and str_val.endswith(value):
                result.append(item)

        return result

    def parse(
        self,
        json_text: str,
        mode: str,
        path: str,
        extract_key_names: str = "",
        array_index: int = -1,
        key_filter: str = "",
        value_filter: str = "",
        flatten_separator: str = ".",
        output_mode: str = "list",
        join_separator: str = ",",
    ) -> tuple:
        if not json_text:
            return ([],) if output_mode == "list" else ([""],)

        # 解析JSON
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            return ([],) if output_mode == "list" else ([""],)

        result = []

        if mode == "auto":
            # 自动模式：根据数据类型返回
            if isinstance(data, dict):
                result = [str(v) for v in data.values()]
            elif isinstance(data, list):
                result = [str(item) for item in data]
            else:
                result = [str(data)]

        elif mode == "path":
            value = self._get_by_path(data, path)
            if value is None:
                result = []
            elif isinstance(value, list):
                result = [str(v) for v in value]
            elif isinstance(value, dict):
                result = [str(v) for v in value.values()]
            else:
                result = [str(value)]

        elif mode == "keys":
            self._extract_all_keys(data, result)
            if key_filter:
                result = [k for k in result if key_filter in k]

        elif mode == "values":
            self._extract_all_values(data, result)
            if value_filter:
                result = [v for v in result if value_filter in v]

        elif mode == "extract_keys":
            # 按键名提取值
            if extract_key_names:
                key_names = [k.strip() for k in extract_key_names.split(",") if k.strip()]
                self._extract_values_by_key_names(data, key_names, result)

        elif mode == "array_items":
            arr = self._get_by_path(data, path) if path else data
            if isinstance(arr, list):
                if array_index >= 0:
                    if array_index < len(arr):
                        item = arr[array_index]
                        if isinstance(item, dict):
                            result = [str(v) for v in item.values()]
                        else:
                            result = [str(item)]
                else:
                    result = [str(item) for item in arr]

        elif mode == "flatten":
            if isinstance(data, dict):
                flat = self._flatten_dict(data, sep=flatten_separator)
                result = [f"{k}: {v}" for k, v in flat.items()]
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, dict):
                        flat = self._flatten_dict(item, sep=flatten_separator)
                        result.append(json.dumps(flat, ensure_ascii=False))
                    else:
                        result.append(str(item))

        elif mode == "query":
            queried = self._query_json(data, path)
            for item in queried:
                if isinstance(item, dict):
                    result.append(json.dumps(item, ensure_ascii=False))
                else:
                    result.append(str(item))

        if not result:
            return ([],) if output_mode == "list" else ([""],)

        if output_mode == "join":
            return ([join_separator.join(result)],)

        return (result,)


class JsonBuilder:
    """
    JSON构建节点
    
    功能说明：
        从键值对列表构建JSON字符串，支持简单对象、对象数组、嵌套结构。
        适用于数据格式化、API请求构建、配置生成等场景。
    
    参数说明：
        keys         - 键名列表
        values       - 值列表
        mode         - 构建模式：
                       - object: 构建单个对象
                       - array_of_objects: 构建对象数组
                       - nested: 构建嵌套对象
        nested_path  - 嵌套路径（mode=nested 时使用）
    
    使用示例：
        示例1 - 构建简单对象：
            keys: ["name", "age", "city"]
            values: ["张三", "25", "北京"]
            mode: object
            结果: {"name": "张三", "age": "25", "city": "北京"}
        
        示例2 - 构建对象数组：
            keys: ["name", "age"]
            values: ["张三", "25"]
            mode: array_of_objects
            结果: [{"key": "name", "value": "张三"}, {"key": "age", "value": "25"}]
        
        示例3 - 构建嵌套对象：
            keys: ["name", "age"]
            values: ["张三", "25"]
            mode: nested
            nested_path: "user.profile"
            结果: {"user": {"profile": {"name": "张三", "age": "25"}}}
        
        示例4 - 从正则提取结果构建JSON：
            # 配合 TxtReg 使用
            TxtReg 提取数字 → TxtRegSelect 选择 → JsonBuilder 构建
            keys: ["order_id", "amount", "quantity"]
            values: ["123", "456", "789"]
            mode: object
            结果: {"order_id": "123", "amount": "456", "quantity": "789"}
        
        示例5 - 批量数据构建：
            keys: ["id", "title", "status"]
            values: ["001", "任务A", "完成"]
            mode: object
            结果: {"id": "001", "title": "任务A", "status": "完成"}
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keys": ("STRING", {"INPUT_IS_LIST": True}),
                "values": ("STRING", {"INPUT_IS_LIST": True}),
            },
            "optional": {
                "mode": (["object", "array_of_objects", "nested"], {"default": "object"}),
                "nested_path": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (False,)
    FUNCTION = "build"
    CATEGORY = "wwdm-aicd"

    def build(
        self,
        keys: list,
        values: list,
        mode: str = "object",
        nested_path: str = "",
    ) -> tuple:
        if not keys:
            return ("{}",)

        # 确保keys和values长度一致
        max_len = max(len(keys), len(values))
        keys = list(keys) + [""] * (max_len - len(keys))
        values = list(values) + [""] * (max_len - len(values))

        if mode == "object":
            result = dict(zip(keys, values))
            return (json.dumps(result, ensure_ascii=False, indent=2),)

        elif mode == "array_of_objects":
            result = [{"key": k, "value": v} for k, v in zip(keys, values)]
            return (json.dumps(result, ensure_ascii=False, indent=2),)

        elif mode == "nested":
            result = {}
            for key, value in zip(keys, values):
                if nested_path:
                    parts = nested_path.split(".")
                    current = result
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[parts[-1] if parts else key] = {key: value}
                else:
                    result[key] = value
            return (json.dumps(result, ensure_ascii=False, indent=2),)

        return ("{}",)
