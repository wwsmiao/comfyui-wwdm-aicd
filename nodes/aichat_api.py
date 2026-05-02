import base64
import io
import requests
import torch
import numpy as np
from PIL import Image


API_BASES = {
    "deepseek": "https://api.deepseek.com/v1/chat/completions",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "doubao": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
}

DEFAULT_MODELS = {
    "deepseek": "deepseek-chat",
    "qwen": "qwen-plus",
    "doubao": "doubao-pro-32k",
}


def tensor_to_b64(image_tensor: torch.Tensor, quality: int = 85) -> str:
    img_np = (image_tensor.cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
    if img_np.shape[-1] == 4:
        img_np = img_np[:, :, :3]
    elif img_np.shape[-1] == 1:
        img_np = np.repeat(img_np, 3, axis=-1)
    img = Image.fromarray(img_np, "RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


class AIChatAPI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (["deepseek", "qwen", "doubao"], {"default": "deepseek"}),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "model": ("STRING", {"default": "", "multiline": False}),
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
                "user_prompt": ("STRING", {"multiline": True, "default": ""}),
                "max_tokens": ("INT", {"default": 2048, "min": 64, "max": 65536, "step": 64}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}),
            },
            "optional": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "chat"
    CATEGORY = "wwdm-aicd"

    def chat(
        self,
        provider: str,
        api_key: str,
        model: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
        images: torch.Tensor = None,
    ) -> tuple:
        if not api_key:
            raise ValueError("api_key is required")

        model = model or DEFAULT_MODELS.get(provider, "deepseek-chat")
        url = API_BASES[provider]

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        user_content = []

        if images is not None and images.size(0) > 0:
            imgs = images.cpu()
            if imgs.ndim == 3:
                imgs = imgs.unsqueeze(0)
            for i in range(imgs.size(0)):
                b64 = tensor_to_b64(imgs[i])
                user_content.append(
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                )

        if user_prompt:
            user_content.append({"type": "text", "text": user_prompt})
        elif not user_content:
            user_content.append({"type": "text", "text": ""})

        messages.append({"role": "user", "content": user_content})

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"API error {resp.status_code}: {resp.text}")

        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return (reply,)
