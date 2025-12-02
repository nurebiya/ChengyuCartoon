"""成语连环画生成器 - 主入口"""
import streamlit as st
from front import *


# 初始化
init_app()

# 应用样式
apply_styles()

# 路由分发
step = st.session_state.get('step', 'input')

if step == 'input':
    render_input_page()
elif step == 'story':
    render_story_page()
elif step == 'script':
    render_script_page()
elif step == 'style_selection':
    render_style_page()
elif step == 'cartoon':
    render_cartoon_page()
