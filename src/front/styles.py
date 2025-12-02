"""古籍风格CSS样式"""
import streamlit as st

def apply_styles():
    """应用古籍风格CSS样式"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');
        
        .main {
            background: linear-gradient(to bottom, #f4e8d0, #e8dcc0);
            background-image: 
                radial-gradient(circle at 2px 2px, rgba(139, 69, 19, 0.15) 1px, transparent 0);
            background-size: 40px 40px;
        }
        
        .stApp {
            background: linear-gradient(to bottom, #f4e8d0, #e8dcc0);
        }
        
        h1 {
            font-family: 'Ma Shan Zheng', 'Noto Serif SC', serif;
            color: #8b4513;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            border-bottom: 3px solid #8b4513;
            padding-bottom: 10px;
        }
        
        .main-title {
            font-family: 'Ma Shan Zheng', 'Noto Serif SC', serif;
            color: #8b4513;
            font-size: 64px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            margin: 50px 0;
        }
        
        /* 成语故事小标题 */
        .story-subtitle {
            font-family: 'Ma Shan Zheng', 'Noto Serif SC', serif;
            color: #8b4513;
            font-size: 28px;
            font-weight: bold;
            margin: 20px 0 10px 0;
        }
        
        /* 修改spinner文字颜色为棕色 */
        .stSpinner > div {
            color: #8b4513 !important;
        }
        
        .stSpinner > div > div {
            color: #8b4513 !important;
        }
        
        /* 修改spinner文字 */
        div[data-testid="stSpinner"] {
            color: #8b4513 !important;
        }
        
        div[data-testid="stSpinner"] > div {
            color: #8b4513 !important;
        }
        
        /* 修改所有spinner相关文字 */
        .stSpinner label,
        .stSpinner span,
        .stSpinner div {
            color: #8b4513 !important;
        }
        
        /* 修改标题文字颜色 */
        .title-left {
            color: #8b4513 !important;
        }
        
        /* 居中容器 */
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            padding: 20px;
        }
        
        /* 确保输入框标签也是棕色 */
        label {
            color: #8b4513 !important;
        }
        
        /* 修改警告文字颜色 */
        .stAlert {
            color: #8b4513;
        }
        
        /* 分镜脚本标题和内容颜色 */
        h3 {
            color: #8b4513 !important;
        }
        
        /* 分镜脚本输入框样式 - 棕色边框、米色背景、棕色文字 */
        .stTextArea > div > div > textarea {
            color: #8b4513 !important;
            background-color: #faf5e8 !important;
            border: 2px solid #8b4513 !important;
            border-radius: 8px !important;
            font-family: 'Noto Serif SC', serif !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
            padding: 15px !important;
            overflow: hidden !important;
            resize: none !important;
        }
        
        /* 分镜输入框聚焦时的样式 */
        .stTextArea > div > div > textarea:focus {
            border-color: #8b4513 !important;
            box-shadow: 0 0 0 2px rgba(139, 69, 19, 0.2) !important;
            outline: none !important;
        }
        
        .stTextArea label {
            color: #8b4513 !important;
            font-family: 'Noto Serif SC', serif !important;
            font-weight: bold !important;
        }
        
        /* 返回按钮右下方定位 */
        .return-button-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .story-container {
            background: #faf5e8;
            border: 2px solid #8b4513;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 4px 4px 8px rgba(0,0,0,0.2);
            font-family: 'Noto Serif SC', serif;
            font-size: 18px;
            line-height: 2;
            color: #5c3a1f;
        }
        
        .script-box {
            background: #faf5e8;
            border: 2px solid #8b4513;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.15);
            font-family: 'Noto Serif SC', serif;
            color: #5c3a1f;
        }
        
        .cartoon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .cartoon-item {
            background: #faf5e8;
            border: 2px solid #8b4513;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.15);
        }
        
        .stButton>button {
            background-color: #8b4513;
            color: white;
            border: 2px solid #654321;
            border-radius: 5px;
            font-family: 'Noto Serif SC', serif;
            font-weight: bold;
        }
        
        .stButton>button:hover {
            background-color: #a0522d;
            border-color: #8b4513;
        }
        
        .stTextInput>div>div>input {
            background-color: #faf5e8;
            border: 2px solid #8b4513;
            color: #5c3a1f;
            font-family: 'Noto Serif SC', serif;
        }
        
        /* 分镜脚本框内文字颜色为白色 */
        .stTextArea textarea {
            color: white !important;
        }
        
        .stTextArea textarea::placeholder {
            color: rgba(255, 255, 255, 0.6) !important;
        }
        
        /* 图片序号标签样式 */
        .image-number-label {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: rgba(139, 69, 19, 0.9);
            color: white;
            padding: 6px 14px;
            border-radius: 6px;
            font-family: 'Noto Serif SC', serif;
            font-weight: bold;
            font-size: 18px;
            z-index: 10;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .title-left {
            font-family: 'Ma Shan Zheng', 'Noto Serif SC', serif;
            color: #8b4513 !important;
            font-size: 24px;
            margin-bottom: 20px;
        }
        
        /* 更通用的spinner文字样式 */
        [data-testid="stSpinner"] * {
            color: #8b4513 !important;
        }
        
        /* 确保所有spinner文字都是棕色 */
        .stSpinner * {
            color: #8b4513 !important;
        }
    </style>
    """, unsafe_allow_html=True)

