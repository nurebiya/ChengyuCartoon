import os
import re
from dashscope import Generation
from typing import Optional, Dict, Any

class BaseLLM:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("BASE_API_KEY")
            if not api_key:
                raise ValueError("API Key未找到！请设置 BASE_API_KEY 环境变量或在初始化时提供")
        self.api_key = api_key
        self.model_name = model_name or os.getenv("BASE_MODEL")
        if not self.model_name:
            raise ValueError("模型名称未找到！请设置 BASE_MODEL 环境变量或在初始化时提供")
    
    def invoke(self, messages, result_format: str = 'message'):
        response = Generation.call(
            api_key=self.api_key,
            model=self.model_name,
            messages=messages,
            result_format=result_format
        )
        # 提取content内容，支持字典和对象两种格式
        content = None
        
        # 如果是字典格式
        if isinstance(response, dict):
            output = response.get('output', {})
            choices = output.get('choices', [])
            if choices and len(choices) > 0:
                message = choices[0].get('message', {})
                content = message.get('content', '')
        # 如果是对象格式
        elif hasattr(response, 'output'):
            output = response.output
            if hasattr(output, 'choices') and output.choices:
                if len(output.choices) > 0:
                    message = output.choices[0].message
                    if hasattr(message, 'content'):
                        content = message.content
        
        # 处理content：将\n替换为空格，合并多个连续空格
        if content:
            content = content.replace('\n', ' ').replace('\r', ' ')
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        
        # 兜底：如果无法提取content，返回字符串表示
        return str(response)