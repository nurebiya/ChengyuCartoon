"""前端配置和初始化"""
import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加src目录到路径（因为所有模块都在src下）
src_root = Path(__file__).parent.parent
if str(src_root) not in sys.path:
    sys.path.insert(0, str(src_root))

from llms import BaseLLM, ImgLLM
from flow import graph

# 初始化应用日志
try:
    from logs.logger import get_logger
    app_logger = get_logger("app")
except ImportError:
    import logging
    app_logger = logging.getLogger("app")
    if not app_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'))
        app_logger.addHandler(handler)
        app_logger.setLevel(logging.INFO)

load_dotenv()

def init_app():
    """初始化应用：LLM、workflow和session state"""
    # 初始化LLM
    if 'llm' not in st.session_state:
        st.session_state.llm = BaseLLM(
            model_name=os.environ.get("BASE_MODEL"),
            api_key=os.environ.get("BASE_API_KEY"),
        )

    if 'imgllm' not in st.session_state:
        st.session_state.imgllm = ImgLLM(
            model_name=os.environ.get("IMG_MODEL"),
            api_key=os.environ.get("IMG_API_KEY"),
        )

    if 'workflow' not in st.session_state:
        st.session_state.workflow = graph(st.session_state.llm, st.session_state.imgllm)

    # 初始化session state
    if 'step' not in st.session_state:
        st.session_state.step = 'input'  # input, story, script, cartoon
    if 'chengyu' not in st.session_state:
        st.session_state.chengyu = ''
    if 'story' not in st.session_state:
        st.session_state.story = ''
    if 'script' not in st.session_state:
        st.session_state.script = []
    if 'cartoon' not in st.session_state:
        st.session_state.cartoon = []
    if 'error' not in st.session_state:
        st.session_state.error = None
    if 'selected_style' not in st.session_state:
        st.session_state.selected_style = None

# 直接导出logger，无需get_logger函数
# 页面中可以直接使用: from front.config import app_logger

