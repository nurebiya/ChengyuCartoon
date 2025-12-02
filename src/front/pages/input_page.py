"""输入页面"""
import streamlit as st
from tools import chengyulist
from front.config import app_logger
from front.components import navigate_to

def render():
    """渲染输入页面"""
    # 初始输入页面
    st.markdown('<div class="main-title">成语连环画生成器</div>', unsafe_allow_html=True)
    
    # 居中内容 - 输入框更宽
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        chengyu_input = st.text_input(
            "请输入一个成语：",
            value="",
            key="input_chengyu",
            label_visibility="visible"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("开始生成", use_container_width=True):
            if chengyu_input.strip():
                # 验证成语是否存在
                if chengyu_input.strip() not in chengyulist:
                    st.error(f"“{chengyu_input.strip()}”不是成语哦，再换一个试试吧。")
                    app_logger.warning(f"用户输入了不存在的成语: {chengyu_input.strip()}")
                else:
                    st.session_state.chengyu = chengyu_input.strip()
                    st.session_state.error = None
                    app_logger.info(f"用户输入成语: {chengyu_input.strip()}")
                    navigate_to('story')
            else:
                st.warning("请输入一个成语")
                app_logger.warning("用户未输入成语")

