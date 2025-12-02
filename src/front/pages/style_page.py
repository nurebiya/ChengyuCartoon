"""风格选择页面"""
import streamlit as st
from front.components import render_page_title, navigate_to

def render():
    """渲染风格选择页面"""
    # 渲染页面标题
    render_page_title()
    
    st.markdown("### 请选择漫画风格")
    
    style_options = [
        "国风插画",
        "卡通彩绘",
        "水墨丹青",
        "黑白线描",
        "简笔趣画",
        "奇幻唯美"
    ]
    
    cols = st.columns(3)
    for idx, style in enumerate(style_options):
        with cols[idx % 3]:
            if st.button(style, key=f"style_{idx}", use_container_width=True):
                st.session_state.selected_style = style
                navigate_to('cartoon')
    
    # 返回按钮移到右下方
    col1, col2 = st.columns([4, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("返回", use_container_width=True):
            navigate_to('script')

