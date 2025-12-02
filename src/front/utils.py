"""前端工具函数"""
import streamlit as st
import time
import io
import zipfile
import requests
from typing import List, Dict, Optional

def typewriter_effect(text: str, container):
    """打字机效果显示文本"""
    placeholder = container.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(f'<div class="story-container">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(0.01)  # 控制打字速度

def download_images(cartoon: List[Dict]):
    """下载所有漫画图片为zip文件"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, frame in enumerate(cartoon):
            img_url = frame.get("img_url")
            if img_url:
                try:
                    response = requests.get(img_url, timeout=30)
                    if response.status_code == 200:
                        zip_file.writestr(f"分镜_{idx+1}.png", response.content)
                except Exception as e:
                    st.error(f"下载第{idx+1}张图片失败: {e}")
    zip_buffer.seek(0)
    return zip_buffer

def create_state(
    include_story: bool = False, 
    include_script: bool = False, 
    include_cartoon: bool = False, 
    style: str = "国风插画",
    pic_num: Optional[int] = None
) -> dict:
    """创建标准化的state字典
    
    Args:
        include_story: 是否包含story字段
        include_script: 是否包含script字段
        include_cartoon: 是否包含cartoon字段
        style: 图片风格
        pic_num: 图片数量，如果为None则根据script长度自动计算
    
    Returns:
        dict: 标准化的state字典
    """
    state = {
        "chengyu": st.session_state.chengyu,
        "story": st.session_state.story if include_story else "",
        "script": st.session_state.script if include_script else [],
        "cartoon": st.session_state.cartoon if include_cartoon else [],
        "pic_num": pic_num if pic_num is not None else (len(st.session_state.script) if include_script else 4),
        "style": style
    }
    return state

