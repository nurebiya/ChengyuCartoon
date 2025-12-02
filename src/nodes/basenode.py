import sys
import os

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from abc import ABC, abstractmethod
from pathlib import Path
from llms.base import BaseLLM
from state.state import State

# 添加项目根目录到路径，以便导入logger
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from logs.logger import get_logger
except ImportError:
    # 如果导入失败，创建一个简单的logger
    import logging
    def get_logger(node_name: str):
        logger = logging.getLogger(node_name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger



class basenode(ABC):

    def __init__(self, llm: BaseLLM, node_name: str = ""):

        self.llm = llm
        self.node_name = node_name or self.__class__.__name__
        # 为每个节点创建独立的logger
        self.logger = get_logger(self.node_name)
    

    def log_info(self, message: str):
        """记录信息日志"""
        self.logger.info(message)

    def log_error(self, message: str):
        """记录错误日志"""
        self.logger.error(message)
    
    def log_debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(message)
    
    def log_warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(message)


