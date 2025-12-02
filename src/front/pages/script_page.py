"""分镜脚本页面"""
import streamlit as st
from nodes import screenwriter
from front.config import app_logger
from front.components import render_page_title, navigate_to
from front.utils import create_state

def render():
    """渲染分镜脚本页面"""
    # 渲染页面标题
    render_page_title()
    
    # 生成分镜
    if not st.session_state.script:
        with st.spinner("正在生成分镜脚本..."):
            try:
                app_logger.info(f"开始生成分镜脚本，成语: {st.session_state.chengyu}")
                current_state = create_state(include_story=True, style="国风插画")
                screenwriter_node = screenwriter(st.session_state.llm)
                result_state = screenwriter_node.write_script(current_state)
                st.session_state.script = result_state.get("script", [])
                st.session_state.error = None
                app_logger.info(f"分镜生成成功，分镜数量: {len(st.session_state.script)}")
            except Exception as e:
                st.session_state.error = str(e)
                app_logger.error(f"生成分镜出错: {e}", exc_info=True)
                st.error(f"生成分镜出错: {e}")
    
    # 显示可编辑的分镜
    if st.session_state.script:
        st.markdown("### 分镜脚本（可编辑）")
        edited_script = []
        for i, frame in enumerate(st.session_state.script):
            # 根据文本长度动态计算高度，确保内容全部显示
            text_length = len(frame.get("text", ""))
            # 估算需要的行数：每行约30-40个字符，加上一些余量
            estimated_lines = max(3, (text_length // 35) + 2)
            # 每行高度约22px（14px字体 + 1.6行高）
            calculated_height = min(200, estimated_lines * 22)
            
            edited_text = st.text_area(
                f"分镜 {i+1}",
                value=frame.get("text", ""),
                key=f"script_{i}",
                height=int(calculated_height),
                label_visibility="visible"
            )
            edited_script.append({
                "text": edited_text,
                "user_modified": edited_text != frame.get("text", ""),
                "keep": True
            })
        
        st.session_state.script = edited_script
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("开始生成漫画", use_container_width=True):
            app_logger.info("用户点击开始生成漫画按钮")
            navigate_to('style_selection')

