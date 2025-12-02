"""公共UI组件"""
import streamlit as st

def render_page_title(title: str = "成语连环画生成器", show_download: bool = False):
    """渲染页面标题
    
    Args:
        title: 标题文本
        show_download: 是否显示下载列（用于漫画页面）
    
    Returns:
        tuple: (col_title, col_other) 列对象
    """
    if show_download:
        col_title, col_download = st.columns([3, 1])
        with col_title:
            st.markdown(f'<div class="title-left">{title}</div>', unsafe_allow_html=True)
        return col_title, col_download
    else:
        col_title, col_space = st.columns([3, 1])
        with col_title:
            st.markdown(f'<div class="title-left">{title}</div>', unsafe_allow_html=True)
        return col_title, col_space

def navigate_to(step: str):
    """页面跳转
    
    Args:
        step: 目标步骤名称
    """
    st.session_state.step = step
    st.rerun()

def reset_state():
    """重置所有状态并返回输入页面"""
    keys_to_reset = ['step', 'chengyu', 'story', 'script', 'cartoon', 'error', 'selected_style', 'story_displayed']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.step = 'input'
    st.rerun()

