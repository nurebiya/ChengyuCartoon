import os
import sys

from pathlib import Path
from typing import Optional
import dashscope
from dashscope import MultiModalConversation

# 添加项目根目录到路径，以便导入logger
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from logs.logger import get_logger
except ImportError:
    # 如果导入失败，创建一个简单的logger
    import logging
    def get_logger(name: str):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger




class ImgLLM:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("IMG_API_KEY")
        self.model_name = model_name or os.getenv("IMG_MODEL") or "qwen-vl-plus"
        self.logger = get_logger("imgllm")

        if not self.api_key:
            raise ValueError("IMG_API_KEY 未找到，请设置环境变量或传参")

        dashscope.api_key = self.api_key
        self.logger.info(f"ImgLLM初始化完成，模型: {self.model_name}")

    def generate_image(self, prompt: str, style: Optional[str] = None) -> str:
        """
        使用 DashScope SDK 生成图片，返回图片URL
        """
        if not prompt:
            self.logger.error("图片生成prompt为空")
            raise ValueError("图片生成prompt不能为空")

        original_prompt = prompt
       
        messages = [{"role": "user", "content": [{"text": " "}]}]

        if style:
            messages[0]["content"][0]["text"] = f"{prompt} | style: {style}"
            self.logger.info(f"开始生成图片，风格: {style}")
        else:
            self.logger.info(f"开始生成图片，风格未指定")

        try:
            self.logger.debug(f"调用DashScope API，模型: {self.model_name}")
            response = MultiModalConversation.call(
                model = self.model_name,
                messages = messages
            )

            output = getattr(response, "output", None)
            if output is None:
                self.logger.error(f"DashScope返回的output为None，完整响应: {response}")
                raise RuntimeError(f"DashScope返回内容异常: output为None, response={response}")

            choice = output.get("choices")[0].get("message").get("content")[0]
            url = choice.get("image")

            if not url:
                self.logger.error(f"DashScope返回的图片url缺失, full content: {first_content}")
                raise RuntimeError(f"DashScope响应无图片URL: {first_content}")

            self.logger.info(f"图片生成成功，URL: {url}")
            return url

        except RuntimeError as e:
            self.logger.error(f"图片生成失败: {e}")
            raise
        except Exception as e:
            self.logger.error(f"DashScope生成图片异常: {e!r}", exc_info=True)
            raise RuntimeError(f"Qwen漫画图片生成失败, 详情: {e}") from e

