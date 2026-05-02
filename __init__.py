from .nodes.txt_reg import TxtReg, TxtRegSelect, JsonParser, JsonBuilder
from .nodes.aichat_api import AIChatAPI

NODE_CLASS_MAPPINGS = {
    "TxtReg": TxtReg,
    "TxtRegSelect": TxtRegSelect,
    "JsonParser": JsonParser,
    "JsonBuilder": JsonBuilder,
    "AIChatAPI": AIChatAPI,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TxtReg": "Txt Reg",
    "TxtRegSelect": "Txt Reg Select",
    "JsonParser": "Json Parser",
    "JsonBuilder": "Json Builder",
    "AIChatAPI": "AI Chat API",
}
