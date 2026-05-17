"""
ComfyUI 文本与字符串处理节点集
包含：连接、分割、截取、大小写转换、替换、修剪、模板、填充、搜索、统计、判断、列表操作等功能。
"""

import re
import random


# =========================================================================
# 1. TextConcat - 文本连接
# =========================================================================
class TextConcat:
    """
    文本连接节点

    功能说明：
        将多个文本字符串按分隔符连接成一个字符串。
        适用于拼接提示词、组合文本片段等场景。

    参数说明：
        str_a     - 输入文本 A
        str_b     - 输入文本 B
        separator - 连接分隔符（可选），如 "," / " " / "\\n"
        str_c     - 输入文本 C（可选）
        str_d     - 输入文本 D（可选）

    使用示例：
        示例1 - 逗号连接：
            str_a: "苹果"  str_b: "香蕉"  separator: ", "
            str_c: "橘子"
            结果: "苹果, 香蕉, 橘子"

        示例2 - 换行连接：
            str_a: "第一行"  str_b: "第二行"  separator: "\\n"
            结果: "第一行\\n第二行"

        示例3 - 无分隔符连接：
            str_a: "Hello"  str_b: "World"  separator: ""
            结果: "HelloWorld"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "str_a": ("STRING", {"multiline": True, "default": ""}),
                "str_b": ("STRING", {"multiline": True, "default": ""}),
                "separator": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {
                "str_c": ("STRING", {"multiline": True, "default": ""}),
                "str_d": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "concat"
    CATEGORY = "wwdm-aicd"

    def concat(self, str_a, str_b, separator, str_c="", str_d=""):
        parts = [s for s in [str_a, str_b, str_c, str_d] if s]
        return (separator.join(parts),)


# =========================================================================
# 2. TextSplit - 文本分割
# =========================================================================
class TextSplit:
    """
    文本分割节点

    功能说明：
        按指定分隔符将文本分割为字符串列表。
        与 TxtReg 的 split 模式不同，本节点使用普通字符串分割，无需正则知识。

    参数说明：
        text      - 输入文本
        delimiter - 分隔符（普通字符串，非正则）
        max_split - 最大分割次数（0=不限制）
        trim      - 是否去除每段的头尾空白

    使用示例：
        示例1 - 逗号分割：
            text: "苹果,香蕉,橘子,西瓜"
            delimiter: ","
            结果: ["苹果", "香蕉", "橘子", "西瓜"]

        示例2 - 限制分割次数：
            text: "a,b,c,d"
            delimiter: ","
            max_split: 2
            结果: ["a", "b", "c,d"]

        示例3 - 按换行分割：
            text: "第一行\\n第二行\\n第三行"
            delimiter: "\\n"
            结果: ["第一行", "第二行", "第三行"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "delimiter": ("STRING", {"multiline": False, "default": ","}),
                "max_split": ("INT", {"default": 0, "min": 0, "max": 10000}),
            },
            "optional": {
                "trim": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    RETURN_NAMES = ("parts",)
    FUNCTION = "split"
    CATEGORY = "wwdm-aicd"

    def split(self, text, delimiter, max_split=0, trim=True):
        if not text:
            return ([],)

        if not delimiter:
            return ([text],)

        if max_split > 0:
            parts = text.split(delimiter, max_split)
        else:
            parts = text.split(delimiter)

        if trim:
            parts = [p.strip() for p in parts]

        return (parts,)


# =========================================================================
# 3. TextSubstring - 子串截取
# =========================================================================
class TextSubstring:
    """
    子串截取节点

    功能说明：
        从文本中截取指定位置和长度的子串。
        适用于提取文本的固定位置信息、按位截断等场景。

    参数说明：
        text      - 输入文本
        start     - 起始位置（0-indexed，支持负数从末尾开始）
        length    - 截取长度（0=截取到末尾）
        clip_mode - 模式：
                    - start_len: 按起始位置+长度截取
                    - start_end: 按起始和结束位置截取（左闭右开）
                    - first_n: 取前 N 个字符
                    - last_n: 取后 N 个字符
        end       - 结束位置（clip_mode=start_end 时使用）

    使用示例：
        示例1 - 从第3位开始取5个字符：
            text: "HelloWorld"  start: 3  length: 5
            结果: "loWor"

        示例2 - 取前5个字符：
            text: "HelloWorld"  clip_mode: first_n  length: 5
            结果: "Hello"

        示例3 - 取后3个字符：
            text: "HelloWorld"  clip_mode: last_n  length: 3
            结果: "rld"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": -99999}),
                "length": ("INT", {"default": 0, "min": 0}),
                "clip_mode": (["start_len", "start_end", "first_n", "last_n"], {"default": "start_len"}),
                "end": ("INT", {"default": 0, "min": -99999}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("substring",)
    FUNCTION = "extract"
    CATEGORY = "wwdm-aicd"

    def extract(self, text, start=0, length=0, clip_mode="start_len", end=0):
        if not text:
            return ("",)

        if clip_mode == "first_n":
            return (text[:length] if length > 0 else text,)

        if clip_mode == "last_n":
            return (text[-length:] if length > 0 else text,)

        if clip_mode == "start_end":
            if end == 0:
                return (text[start:],)
            return (text[start:end],)

        # start_len mode
        if length == 0:
            return (text[start:],)
        return (text[start:start + length],)


# =========================================================================
# 4. TextCase - 大小写/命名法转换
# =========================================================================
class TextCase:
    """
    文本大小写与命名法转换节点

    功能说明：
        将文本转换为各种大小写格式或命名法。
        支持常见的大小写转换和编程命名风格。

    参数说明：
        text     - 输入文本
        case     - 转换模式：
                   - upper: 全大写
                   - lower: 全小写
                   - title: 首字母大写（每个单词）
                   - capitalize: 首句大写
                   - swapcase: 大小写翻转
                   - camel: 驼峰命名法（camelCase）
                   - pascal: 帕斯卡命名法（PascalCase）
                   - snake: 下划线命名法（snake_case）
                   - kebab: 连字符命名法（kebab-case）
                   - constant: 常量命名法（CONSTANT_CASE）
                   - sentence: 整句保留首单词大写

    使用示例：
        示例1 - 全大写：
            text: "hello world"  case: upper
            结果: "HELLO WORLD"

        示例2 - 驼峰命名：
            text: "hello world"  case: camel
            结果: "helloWorld"

        示例3 - 常量命名：
            text: "hello world"  case: constant
            结果: "HELLO_WORLD"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "case": (
                    ["upper", "lower", "title", "capitalize", "swapcase",
                     "camel", "pascal", "snake", "kebab", "constant", "sentence"],
                    {"default": "lower"},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "convert"
    CATEGORY = "wwdm-aicd"

    def convert(self, text, case):
        if not text:
            return ("",)

        if case == "upper":
            return (text.upper(),)
        elif case == "lower":
            return (text.lower(),)
        elif case == "title":
            return (text.title(),)
        elif case == "capitalize":
            return (text.capitalize(),)
        elif case == "swapcase":
            return (text.swapcase(),)
        elif case == "sentence":
            return (text[0].upper() + text[1:] if text else "",)
        elif case in ("camel", "pascal", "snake", "kebab", "constant"):
            # 用正则分词：按非字母数字分割
            words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$|\d)|\d+', text)
            words = [w.lower() for w in words]
            if case == "camel":
                return (words[0] + "".join(w.capitalize() for w in words[1:]),)
            elif case == "pascal":
                return ("".join(w.capitalize() for w in words),)
            elif case == "snake":
                return ("_".join(words),)
            elif case == "kebab":
                return ("-".join(words),)
            elif case == "constant":
                return ("_".join(w.upper() for w in words),)
        return (text,)


# =========================================================================
# 5. TextReplace - 字符串替换
# =========================================================================
class TextReplace:
    """
    字符串替换节点

    功能说明：
        执行简单的字符串查找替换。
        与 TxtReg 的 replace 模式不同，本节点使用普通字符串匹配，无需正则。

    参数说明：
        text       - 输入文本
        old_string - 被替换的字符串
        new_string - 替换成的字符串
        count      - 替换次数（0=替换全部）
        ignore_case - 是否忽略大小写

    使用示例：
        示例1 - 简单替换：
            text: "Hello World"  old_string: "World"  new_string: "ComfyUI"
            结果: "Hello ComfyUI"

        示例2 - 全部替换：
            text: "a-b-c-d"  old_string: "-"  new_string: "/"
            结果: "a/b/c/d"

        示例3 - 限制替换次数：
            text: "a-b-c-d"  old_string: "-"  new_string: "+"  count: 2
            结果: "a+b+c-d"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "old_string": ("STRING", {"multiline": False, "default": ""}),
                "new_string": ("STRING", {"multiline": False, "default": ""}),
                "count": ("INT", {"default": 0, "min": 0}),
            },
            "optional": {
                "ignore_case": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "replace"
    CATEGORY = "wwdm-aicd"

    def replace(self, text, old_string, new_string, count=0, ignore_case=False):
        if not text or not old_string:
            return (text,)

        if ignore_case:
            # 用正则实现忽略大小写的替换，count>0 时限制替换次数
            flags = re.IGNORECASE
            if count > 0:
                result = re.sub(re.escape(old_string), new_string, text, count=count, flags=flags)
            else:
                result = re.sub(re.escape(old_string), new_string, text, flags=flags)
            return (result,)

        if count > 0:
            return (text.replace(old_string, new_string, count),)
        return (text.replace(old_string, new_string),)


# =========================================================================
# 6. TextTrim - 文本修剪
# =========================================================================
class TextTrim:
    """
    文本修剪节点

    功能说明：
        去除文本头尾空白、合并多余空白、按行修剪等。

    参数说明：
        text       - 输入文本
        mode       - 修剪模式：
                     - trim: 去除头尾空白
                     - ltrim: 仅去除左侧空白
                     - rtrim: 仅去除右侧空白
                     - collapse: 合并所有连续空白为单个空格
                     - strip_lines: 每行去除头尾空白并移除空行
                     - remove_blank_lines: 仅移除空行
        chars      - 要移除的字符（可选，默认空白字符）

    使用示例：
        示例1 - 去除头尾：
            text: "  Hello World  "  mode: trim
            结果: "Hello World"

        示例2 - 合并空白：
            text: "Hello    World  你好"  mode: collapse
            结果: "Hello World 你好"

        示例3 - 按行处理并去空行：
            text: "  第一行  \\n  \\n  第二行  "  mode: strip_lines
            结果: "第一行\\n第二行"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "mode": (
                    ["trim", "ltrim", "rtrim", "collapse", "strip_lines", "remove_blank_lines"],
                    {"default": "trim"},
                ),
            },
            "optional": {
                "chars": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "trim"
    CATEGORY = "wwdm-aicd"

    def trim(self, text, mode, chars=""):
        if not text:
            return ("",)

        strip_chars = chars if chars else None

        if mode == "trim":
            return (text.strip(strip_chars),)
        elif mode == "ltrim":
            return (text.lstrip(strip_chars),)
        elif mode == "rtrim":
            return (text.rstrip(strip_chars),)
        elif mode == "collapse":
            return (re.sub(r'\s+', ' ', text).strip(),)
        elif mode == "strip_lines":
            lines = [l.strip() for l in text.split("\n")]
            lines = [l for l in lines if l]
            return ("\n".join(lines),)
        elif mode == "remove_blank_lines":
            lines = [l for l in text.split("\n") if l.strip()]
            return ("\n".join(lines),)

        return (text,)


# =========================================================================
# 7. TextTemplate - 模板格式化
# =========================================================================
class TextTemplate:
    """
    文本模板节点

    功能说明：
        使用占位符模板生成文本。支持 {0}, {1} 位置占位符和 {name} 命名占位符。
        用于构建带变量的提示词、格式化输出等场景。

    参数说明：
        template - 模板字符串，包含 {0}, {1} 或 {name} 占位符
        arg0     - 占位符 {0} 的值
        arg1     - 占位符 {1} 的值

    使用示例：
        示例1 - 位置占位符：
            template: "你好 {0}，你今天 {1} 吗？"
            arg0: "张三"  arg1: "吃饭"
            结果: "你好 张三，你今天 吃饭 吗？"

        示例2 - 重复使用占位符：
            template: "{0} + {0} = {1}"
            arg0: "1"  arg1: "2"
            结果: "1 + 1 = 2"

        示例3 - 命名占位符：
            template: "用户：{name}，年龄：{age}"
            arg0: "{name:张三,age:25}"
            结果: "用户：张三，年龄：25"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "default": ""}),
                "arg0": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "arg1": ("STRING", {"multiline": True, "default": ""}),
                "arg2": ("STRING", {"multiline": True, "default": ""}),
                "arg3": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "format"
    CATEGORY = "wwdm-aicd"

    def format(self, template, arg0, arg1="", arg2="", arg3=""):
        if not template:
            return ("",)

        args = (arg0, arg1, arg2, arg3)

        # 尝试命名占位符: {key}
        named_matches = re.findall(r'\{(\w+)\}', template)
        if named_matches:
            # 尝试从 arg0 解析 JSON 风格键值对
            for arg in args:
                if not arg:
                    continue
                pairs = re.findall(r'(\w+):\s*([^,}]+)', arg)
                if pairs:
                    kwargs = dict(pairs)
                    try:
                        return (template.format(**kwargs),)
                    except KeyError:
                        pass

        # 位置占位符: {0}, {1}
        try:
            return (template.format(*args),)
        except (IndexError, KeyError):
            # 如果占位符不够，用空字符串替换
            result = template
            for i, a in enumerate(args):
                result = result.replace(f"{{{i}}}", a)
            return (result,)


# =========================================================================
# 8. TextPad - 文本填充
# =========================================================================
class TextPad:
    """
    文本填充节点

    功能说明：
        将文本填充到指定宽度。适用于对齐输出、格式化表格等场景。

    参数说明：
        text      - 输入文本
        mode      - 填充模式：
                    - left: 左对齐（右侧填充）
                    - right: 右对齐（左侧填充）
                    - center: 居中对齐（两侧填充）
        width     - 目标宽度
        pad_char  - 填充字符，默认为空格

    使用示例：
        示例1 - 左对齐填充：
            text: "你好"  mode: left  width: 10  pad_char: "."
            结果: "你好......"

        示例2 - 右对齐填充：
            text: "123"  mode: right  width: 6  pad_char: "0"
            结果: "000123"

        示例3 - 居中对齐：
            text: "Hi"  mode: center  width: 9  pad_char: "-"
            结果: "---Hi----"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "mode": (["left", "right", "center"], {"default": "left"}),
                "width": ("INT", {"default": 20, "min": 1, "max": 9999}),
                "pad_char": ("STRING", {"multiline": False, "default": " "}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "pad"
    CATEGORY = "wwdm-aicd"

    def pad(self, text, mode, width, pad_char=" "):
        if not text:
            return ("",)

        pc = pad_char[0] if pad_char else " "

        if mode == "left":
            return (text.ljust(width, pc),)
        elif mode == "right":
            return (text.rjust(width, pc),)
        elif mode == "center":
            return (text.center(width, pc),)

        return (text,)


# =========================================================================
# 9. TextSearch - 文本搜索
# =========================================================================
class TextSearch:
    """
    文本搜索节点

    功能说明：
        在文本中搜索子串，支持统计出现次数、查找位置、判断是否包含等。

    参数说明：
        text       - 被搜索的文本
        search_for - 要搜索的字符串
        mode       - 搜索模式：
                     - contains: 是否包含（返回布尔字符串 "true"/"false"）
                     - count: 统计出现次数
                     - find_first: 返回第一次出现的位置（-1=未找到）
                     - find_all: 返回所有出现位置的列表
                     - find_lines: 返回包含搜索文本的所有行
        ignore_case - 是否忽略大小写
        output     - 输出格式（用于 find_all/find_lines 模式）

    使用示例：
        示例1 - 判断是否包含：
            text: "Hello World"  search_for: "World"  mode: contains
            结果: "true"

        示例2 - 统计出现次数：
            text: "abca bc ab"  search_for: "ab"  mode: count
            结果: "2"

        示例3 - 查找含关键词的行：
            text: "第一行\\n包含关键字\\n第三行"  search_for: "关键"  mode: find_lines
            结果: ["包含关键字"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "search_for": ("STRING", {"multiline": False, "default": ""}),
                "mode": (
                    ["contains", "count", "find_first", "find_all", "find_lines"],
                    {"default": "contains"},
                ),
            },
            "optional": {
                "ignore_case": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "search"
    CATEGORY = "wwdm-aicd"

    def search(self, text, search_for, mode, ignore_case=False):
        if not text or not search_for:
            if mode == "contains":
                return ("false",)
            elif mode == "count":
                return ("0",)
            elif mode == "find_first":
                return ("-1",)
            return ([],)

        if ignore_case:
            src_lower = text.lower()
            search_lower = search_for.lower()
            src = src_lower
            target = search_lower
        else:
            src = text
            target = search_for

        if mode == "contains":
            return ("true" if target in src else "false",)

        elif mode == "count":
            return (str(src.count(target)),)

        elif mode == "find_first":
            return (str(src.find(target)),)

        elif mode == "find_all":
            positions = []
            pos = 0
            while True:
                pos = src.find(target, pos)
                if pos == -1:
                    break
                positions.append(str(pos))
                pos += 1
            return (positions,)

        elif mode == "find_lines":
            lines = text.split("\n")
            matched = [l for l in lines if target in (l.lower() if ignore_case else l)]
            return (matched,)

        return (str(target in src),)


# =========================================================================
# 10. TextLength - 文本统计
# =========================================================================
class TextLength:
    """
    文本统计节点

    功能说明：
        统计文本的各种长度指标。返回整数和描述字符串。

    参数说明：
        text     - 输入文本
        output   - 输出内容：
                   - all: 返回所有统计信息
                   - char_count: 仅字符数
                   - word_count: 仅词数（按空格分割）
                   - line_count: 仅行数
                   - byte_size: 仅字节大小

    使用示例：
        示例1 - 全部统计：
            text: "Hello World 你好"
            结果: "字符数: 15 | 词数: 3 | 行数: 1 | 字节: 17"

        示例2 - 仅字符数：
            text: "Hello"  output: char_count
            结果: "5"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "output": (
                    ["summary", "char_count", "word_count", "line_count", "byte_size"],
                    {"default": "summary"},
                ),
            },
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("text", "char_count")
    FUNCTION = "measure"
    CATEGORY = "wwdm-aicd"

    def measure(self, text, output="summary"):
        if not text:
            if output == "summary":
                return ("字符数: 0 | 词数: 0 | 行数: 0 | 字节: 0", 0)
            return ("0", 0)

        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.split("\n"))
        byte_size = len(text.encode("utf-8"))

        if output == "summary":
            info = f"字符数: {char_count} | 词数: {word_count} | 行数: {line_count} | 字节: {byte_size}"
            return (info, char_count)
        elif output == "char_count":
            return (str(char_count), char_count)
        elif output == "word_count":
            return (str(word_count), char_count)
        elif output == "line_count":
            return (str(line_count), char_count)
        elif output == "byte_size":
            return (str(byte_size), char_count)

        return (f"字符数: {char_count}", char_count)


# =========================================================================
# 11. TextJudge - 文本判断
# =========================================================================
class TextJudge:
    """
    文本判断节点

    功能说明：
        对文本进行各种条件判断，返回布尔值（"true"/"false"）或比较结果字符串。

    参数说明：
        input_a    - 输入文本 A
        operator   - 判断操作符：
                     - equals: 是否相等
                     - not_equals: 是否不相等
                     - contains: A 是否包含 B
                     - not_contains: A 是否不包含 B
                     - starts_with: A 是否以 B 开头
                     - ends_with: A 是否以 B 结尾
                     - is_empty: A 是否为空
                     - not_empty: A 是否非空
                     - is_digit: A 是否仅数字
                     - is_alpha: A 是否仅字母
                     - is_alnum: A 是否仅字母数字
                     - length_gt: A 长度大于 N
                     - length_lt: A 长度小于 N
        input_b    - 输入文本 B/比较值（部分操作符不需要）
        invert     - 反转结果

    使用示例：
        示例1 - 判断相等：
            input_a: "hello"  operator: equals  input_b: "hello"
            结果: "true"

        示例2 - 判断是否为空：
            input_a: ""  operator: is_empty
            结果: "true"

        示例3 - 判断长度：
            input_a: "ComfyUI"  operator: length_gt  input_b: "5"
            结果: "true"  (因为 "ComfyUI" 长度为 7 > 5)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_a": ("STRING", {"multiline": True, "default": ""}),
                "operator": (
                    ["equals", "not_equals", "contains", "not_contains",
                     "starts_with", "ends_with",
                     "is_empty", "not_empty",
                     "is_digit", "is_alpha", "is_alnum",
                     "length_gt", "length_lt", "length_eq"],
                    {"default": "equals"},
                ),
            },
            "optional": {
                "input_b": ("STRING", {"multiline": False, "default": ""}),
                "invert": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("result", "boolean")
    FUNCTION = "judge"
    CATEGORY = "wwdm-aicd"

    def judge(self, input_a, operator, input_b="", invert=False):
        result = False

        if operator == "equals":
            result = input_a == input_b
        elif operator == "not_equals":
            result = input_a != input_b
        elif operator == "contains":
            result = input_b in input_a
        elif operator == "not_contains":
            result = input_b not in input_a
        elif operator == "starts_with":
            result = input_a.startswith(input_b)
        elif operator == "ends_with":
            result = input_a.endswith(input_b)
        elif operator == "is_empty":
            result = not input_a
        elif operator == "not_empty":
            result = bool(input_a)
        elif operator == "is_digit":
            result = input_a.isdigit()
        elif operator == "is_alpha":
            result = input_a.isalpha()
        elif operator == "is_alnum":
            result = input_a.isalnum()
        elif operator == "length_gt":
            try:
                result = len(input_a) > int(input_b)
            except ValueError:
                result = False
        elif operator == "length_lt":
            try:
                result = len(input_a) < int(input_b)
            except ValueError:
                result = False
        elif operator == "length_eq":
            try:
                result = len(input_a) == int(input_b)
            except ValueError:
                result = False

        if invert:
            result = not result

        return ("true" if result else "false", result)


# =========================================================================
# 12. ListOps - 列表操作
# =========================================================================
class ListOps:
    """
    列表操作节点

    功能说明：
        对字符串列表进行排序、反转、去重、随机打乱、分块等操作。
        通常与 TxtReg、TextSplit 等生成列表的节点配合使用。

    参数说明：
        items     - 输入列表
        operation - 操作模式：
                    - join: 将列表连接为单个字符串
                    - sort: 字母排序（升序）
                    - sort_desc: 字母排序（降序）
                    - reverse: 反转顺序
                    - dedupe: 去重（保留首次出现顺序）
                    - shuffle: 随机打乱
                    - chunk: 按指定大小分块
                    - flatten: 拍平嵌套列表
                    - unique: 去重（同 dedupe）
                    - sort_by_length: 按字符串长度排序
                    - take: 取前 N 个元素
        param     - 操作参数：
                    - join 模式：连接分隔符
                    - chunk 模式：每块元素数
                    - take/skip 模式：数量
        seed      - 随机种子（shuffle 模式，0=随机）

    使用示例：
        示例1 - 连接列表：
            items: ["a", "b", "c"]  operation: join  param: ", "
            结果: "a, b, c"

        示例2 - 排序：
            items: ["c", "a", "b"]  operation: sort
            结果: ["a", "b", "c"]

        示例3 - 随机打乱：
            items: ["1", "2", "3", "4", "5"]  operation: shuffle  seed: 42
            结果: ["3", "5", "1", "4", "2"]  (固定种子保证可复现)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "items": ("STRING", {"INPUT_IS_LIST": True}),
                "operation": (
                    ["join", "sort", "sort_desc", "reverse", "dedupe", "shuffle",
                     "chunk", "sort_by_length", "take", "skip"],
                    {"default": "join"},
                ),
            },
            "optional": {
                "param": ("STRING", {"multiline": False, "default": ","}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    RETURN_NAMES = ("result",)
    FUNCTION = "operate"
    CATEGORY = "wwdm-aicd"

    def operate(self, items, operation, param=",", seed=0):
        if not items:
            if operation == "join":
                return ([""],)
            return ([],)

        lst = list(items)

        if operation == "join":
            return ([param.join(lst)],)

        elif operation == "sort":
            return (sorted(lst),)

        elif operation == "sort_desc":
            return (sorted(lst, reverse=True),)

        elif operation == "reverse":
            return (list(reversed(lst)),)

        elif operation == "dedupe" or operation == "unique":
            seen = set()
            result = []
            for item in lst:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            return (result,)

        elif operation == "shuffle":
            rng = random.Random(seed) if seed else random
            rng.shuffle(lst)
            return (lst,)

        elif operation == "chunk":
            try:
                n = int(param)
            except ValueError:
                n = 2
            if n <= 0:
                n = 1
            chunks = []
            for i in range(0, len(lst), n):
                chunks.extend(lst[i:i + n])
            return (chunks,)

        elif operation == "sort_by_length":
            return (sorted(lst, key=len),)

        elif operation == "take":
            try:
                n = int(param)
            except ValueError:
                n = 1
            return (lst[:max(0, n)],)

        elif operation == "skip":
            try:
                n = int(param)
            except ValueError:
                n = 0
            return (lst[n:],)

        return (lst,)


# =========================================================================
# 13. TextFilterLines - 按行过滤
# =========================================================================
class TextFilterLines:
    """
    文本行过滤节点

    功能说明：
        对多行文本按行进行过滤。支持包含/排除匹配、前后缀匹配、正则匹配等。
        类似 grep 命令的简单实现。

    参数说明：
        text    - 输入的多行文本
        mode    - 过滤模式：
                  - grep: 保留匹配的行
                  - grep_v: 排除匹配的行
        pattern - 匹配字符串
        match   - 匹配方式：
                  - contains: 包含
                  - regex: 正则匹配
                  - starts: 行首匹配
                  - ends: 行尾匹配
                  - equals: 完全匹配
        ignore_case - 忽略大小写
        trim_lines  - 过滤前是否修剪每行空白

    使用示例：
        示例1 - Grep 过滤：
            text: "苹果\\n香蕉\\n葡萄\\n草莓"
            pattern: "莓"
            结果: ["草莓"]

        示例2 - 排除匹配：
            text: "error: file not found\\ninfo: loading\\nwarning: low disk"
            pattern: "error"  mode: grep_v
            结果: ["info: loading", "warning: low disk"]

        示例3 - 正则匹配：
            text: "123\\nabc\\n456\\ndef"
            pattern: "\\d+"  match: regex
            结果: ["123", "456"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "pattern": ("STRING", {"multiline": False, "default": ""}),
                "mode": (["grep", "grep_v"], {"default": "grep"}),
                "match": (
                    ["contains", "regex", "starts", "ends", "equals"],
                    {"default": "contains"},
                ),
            },
            "optional": {
                "ignore_case": ("BOOLEAN", {"default": False}),
                "trim_lines": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    RETURN_NAMES = ("lines",)
    FUNCTION = "filter_lines"
    CATEGORY = "wwdm-aicd"

    def filter_lines(self, text, pattern, mode, match, ignore_case=False, trim_lines=True):
        if not text:
            return ([],)

        lines = text.split("\n")
        if trim_lines:
            lines = [l.strip() for l in lines]
            lines = [l for l in lines if l]

        if not pattern:
            return (lines,)

        result = []
        for line in lines:
            src = line.lower() if ignore_case else line
            pat = pattern.lower() if ignore_case else pattern

            matched = False
            if match == "contains":
                matched = pat in src
            elif match == "regex":
                try:
                    flags = re.IGNORECASE if ignore_case else 0
                    matched = bool(re.search(pat, src, flags))
                except re.error:
                    matched = False
            elif match == "starts":
                matched = src.startswith(pat)
            elif match == "ends":
                matched = src.endswith(pat)
            elif match == "equals":
                matched = src == pat

            if (mode == "grep" and matched) or (mode == "grep_v" and not matched):
                result.append(line)

        if mode == "grep_v":
            return (result,)

        return (result,)


# =========================================================================
# 14. TextWrap - 文本折行
# =========================================================================
class TextWrap:
    """
    文本折行节点

    功能说明：
        将长文本按指定宽度折行。适用于格式化输出、限制行宽等场景。

    参数说明：
        text    - 输入文本
        width   - 每行最大字符数
        break_long_words - 是否打断长单词

    使用示例：
        示例1 - 基础折行：
            text: "这是一个很长的句子，需要被折行显示。"
            width: 10
            结果: ["这是一个很长", "的句子，需要", "被折行显示。"]

        示例2 - 英文折行：
            text: "Hello World This is a long text"
            width: 12
            结果: ["Hello World", "This is a", "long text"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "width": ("INT", {"default": 80, "min": 4, "max": 9999}),
                "break_long_words": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    RETURN_NAMES = ("lines",)
    FUNCTION = "wrap"
    CATEGORY = "wwdm-aicd"

    def wrap(self, text, width=80, break_long_words=True):
        if not text or width <= 0:
            return ([""],)

        lines = []
        for paragraph in text.split("\n"):
            if not paragraph:
                lines.append("")
                continue

            words = paragraph.split()
            if not words:
                lines.append("")
                continue

            current = words[0]
            for word in words[1:]:
                # 当前行 + 空格 + 新词 是否超宽
                if len(current) + 1 + len(word) <= width:
                    current += " " + word
                else:
                    # 如果单行放不下
                    if break_long_words:
                        while len(current) > width:
                            lines.append(current[:width])
                            current = current[width:]
                    lines.append(current)
                    current = word

            # 处理最后一行
            if break_long_words:
                while len(current) > width:
                    lines.append(current[:width])
                    current = current[width:]
            if current:
                lines.append(current)

        return (lines,)


# =========================================================================
# 15. TextRandom - 随机文本生成
# =========================================================================
class TextRandom:
    """
    随机文本生成节点

    功能说明：
        从多个候选项中选择一个或多个文本。适用于随机提示词选择、A/B 测试等。

    参数说明：
        option_a     - 选项 A
        option_b     - 选项 B
        option_c     - 选项 C（可选）
        option_d     - 选项 D（可选）
        option_e     - 选项 E（可选）
        count        - 选择数量（1=单选，>1=多选，0=全部）
        seed         - 随机种子（0=随机）
        output_mode  - list: 返回列表，single: 返回连接字符串

    使用示例：
        示例1 - 随机单选：
            option_a: "苹果"  option_b: "香蕉"  option_c: "橘子"
            结果: "香蕉"

        示例2 - 随机选两个：
            options: "苹果/香蕉/橘子/西瓜"
            count: 2
            结果: ["橘子", "西瓜"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "option_a": ("STRING", {"multiline": True, "default": ""}),
                "option_b": ("STRING", {"multiline": True, "default": ""}),
                "count": ("INT", {"default": 1, "min": 0, "max": 100}),
            },
            "optional": {
                "option_c": ("STRING", {"multiline": True, "default": ""}),
                "option_d": ("STRING", {"multiline": True, "default": ""}),
                "option_e": ("STRING", {"multiline": True, "default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "pick"
    CATEGORY = "wwdm-aicd"

    def pick(self, option_a, option_b, count=1, option_c="", option_d="", option_e="", seed=0):
        options = [s for s in [option_a, option_b, option_c, option_d, option_e] if s]

        if not options:
            return ([""],)

        rng = random.Random(seed) if seed else random

        if count <= 0 or count >= len(options):
            rng.shuffle(options)
            return (options,)

        picked = rng.sample(options, min(count, len(options)))
        return (picked,)


# =========================================================================
# 16. TextEscape - 文本转义/反转义
# =========================================================================
class TextEscape:
    """
    文本转义/反转义节点

    功能说明：
        对文本进行转义或反转义处理。适用于处理特殊字符、JSON 字符串等。

    参数说明：
        text - 输入文本
        mode - 操作模式：
               - escape_json: JSON 转义
               - unescape_json: JSON 反转义
               - escape_html: HTML 转义
               - unescape_html: HTML 反转义
               - escape_url: URL 编码
               - unescape_url: URL 解码
               - escape_unicode: Unicode 转义 (\\uXXXX)
               - unescape_unicode: Unicode 反转义
               - add_slashes: 添加反斜杠转义
               - strip_slashes: 去除反斜杠转义

    使用示例：
        示例1 - JSON 转义：
            text: '她说："你好"'  mode: escape_json
            结果: '她说：\"你好\"'

        示例2 - URL 编码：
            text: "你好世界"  mode: escape_url
            结果: "%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C"

        示例3 - HTML 转义：
            text: "<script>alert('xss')</script>"  mode: escape_html
            结果: "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "mode": (
                    ["escape_json", "unescape_json",
                     "escape_html", "unescape_html",
                     "escape_url", "unescape_url",
                     "escape_unicode", "unescape_unicode",
                     "add_slashes", "strip_slashes"],
                    {"default": "escape_json"},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "escape"
    CATEGORY = "wwdm-aicd"

    def escape(self, text, mode):
        if not text:
            return ("",)

        import html
        import urllib.parse

        if mode == "escape_json":
            import json
            return (json.dumps(text, ensure_ascii=False)[1:-1],)
        elif mode == "unescape_json":
            import json
            try:
                return (json.loads(f'"{text}"'),)
            except json.JSONDecodeError:
                return (text,)
        elif mode == "escape_html":
            return (html.escape(text, quote=True),)
        elif mode == "unescape_html":
            return (html.unescape(text),)
        elif mode == "escape_url":
            return (urllib.parse.quote(text, safe=""),)
        elif mode == "unescape_url":
            return (urllib.parse.unquote(text),)
        elif mode == "escape_unicode":
            return (text.encode("unicode_escape").decode("ascii"),)
        elif mode == "unescape_unicode":
            return (text.encode("ascii").decode("unicode_escape"),)
        elif mode == "add_slashes":
            escaped = text.replace("\\", "\\\\")
            escaped = escaped.replace("'", "\\'")
            escaped = escaped.replace('"', '\\"')
            escaped = escaped.replace("\n", "\\n")
            escaped = escaped.replace("\t", "\\t")
            escaped = escaped.replace("\r", "\\r")
            return (escaped,)
        elif mode == "strip_slashes":
            result = text.replace("\\n", "\n")
            result = result.replace("\\t", "\t")
            result = result.replace("\\r", "\r")
            result = result.replace("\\'", "'")
            result = result.replace('\\"', '"')
            result = result.replace("\\\\", "\\")
            return (result,)

        return (text,)


# =========================================================================
# 17. TextMultiConcat - 多路文本连接
# =========================================================================
class TextMultiConcat:
    """
    多路文本连接节点

    功能说明：
        同时连接多个输入源。与 TextConcat 不同，本节点接受任意字符串列表作为输入，
        适合连接多个上游节点的输出。

    参数说明：
        list_a    - 字符串列表 A
        list_b    - 字符串列表 B
        separator - 连接分隔符
        mode      - 连接模式：
                    - concat: 简单连接所有元素
                    - zip: 按位置配对连接（A[0] + sep + B[0], ...）
                    - cross: 笛卡尔积（所有 A × 所有 B）

    使用示例：
        示例1 - 简单连接：
            list_a: ["a", "b"]  list_b: ["1", "2"]  mode: concat  separator: ", "
            结果: ["a", "b", "1", "2"]

        示例2 - 配对连接：
            list_a: ["name", "age"]  list_b: ["张三", "25"]  mode: zip
            separator: ": "
            结果: ["name: 张三", "age: 25"]
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list_a": ("STRING", {"INPUT_IS_LIST": True}),
            },
            "optional": {
                "list_b": ("STRING", {"INPUT_IS_LIST": True}),
                "separator": ("STRING", {"multiline": False, "default": ""}),
                "mode": (["concat", "zip", "cross"], {"default": "concat"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    RETURN_NAMES = ("result",)
    FUNCTION = "merge"
    CATEGORY = "wwdm-aicd"

    def merge(self, list_a, list_b=None, separator="", mode="concat"):
        lst_a = list(list_a) if list_a else []
        lst_b = list(list_b) if list_b else []

        if mode == "concat":
            return (lst_a + lst_b,)

        elif mode == "zip":
            result = []
            for i in range(max(len(lst_a), len(lst_b))):
                a = lst_a[i] if i < len(lst_a) else ""
                b = lst_b[i] if i < len(lst_b) else ""
                result.append(a + separator + b)
            return (result,)

        elif mode == "cross":
            if not lst_b:
                return (lst_a,)
            result = []
            for a in lst_a:
                for b in lst_b:
                    result.append(a + separator + b)
            return (result,)

        return (lst_a,)
