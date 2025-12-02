import logging
import os
from datetime import datetime
from pathlib import Path

# 确保logs目录存在
LOG_DIR = Path(__file__).parent
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(node_name: str = "app") -> logging.Logger:
    """
    为每个节点设置独立的logger
    
    Args:
        node_name: 节点名称，如 storyteller, screenwriter, cartoonist
        
    Returns:
        配置好的Logger对象
    """
    logger = logging.getLogger(node_name)
    
    # 如果logger已经有handler，直接返回（避免重复添加）
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # 日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件handler - 按日期和节点名称分类
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOG_DIR / f"{node_name}_{today}.log"
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # 控制台handler - 只显示INFO及以上级别
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(node_name: str) -> logging.Logger:
    """
    获取指定节点的logger，如果不存在则创建
    
    Args:
        node_name: 节点名称
        
    Returns:
        Logger对象
    """
    return setup_logger(node_name)

