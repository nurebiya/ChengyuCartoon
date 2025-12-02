"""故事生成页面"""
import streamlit as st
from nodes import storyteller
from front.utils import typewriter_effect, create_state
from front.config import app_logger
from front.components import render_page_title, navigate_to

def render():
    """渲染故事生成页面"""
    # 渲染页面标题
    render_page_title()
    
    # 生成故事
    if not st.session_state.story:
        with st.spinner("正在生成故事..."):
            try:
                app_logger.info(f"开始生成故事，成语: {st.session_state.chengyu}")
                init_state = create_state(style="国风插画")
                # 只运行storyteller节点
                storyteller_node = storyteller(st.session_state.llm)
                result_state = storyteller_node.teller(init_state)
                st.session_state.story = result_state.get("story", "")
                st.session_state.error = None
                app_logger.info(f"故事生成成功，长度: {len(st.session_state.story)} 字符")
            except Exception as e:
                st.session_state.error = str(e)
                app_logger.error(f"故事生成失败: {e}", exc_info=True)
                navigate_to('input')
    
    # 显示错误
    if st.session_state.error:
        st.error(f"生成出错: {st.session_state.error}")
        if st.button("返回重新输入"):
            st.session_state.error = None
            navigate_to('input')
    # 显示故事
    elif st.session_state.story:
        # 显示小标题"成语故事"
        st.markdown('<div class="story-subtitle">成语故事</div>', unsafe_allow_html=True)
        
        # 只在第一次显示时使用打字机效果，之后直接显示静态文本
        if 'story_displayed' not in st.session_state:
            story_container = st.empty()
            typewriter_effect(st.session_state.story, story_container)
            st.session_state.story_displayed = True
        else:
            # 已经显示过，直接显示静态文本，不再使用打字机效果
            st.markdown(f'<div class="story-container">{st.session_state.story}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("生成分镜", use_container_width=True):
            app_logger.info("用户点击生成分镜按钮")
            navigate_to('script')

