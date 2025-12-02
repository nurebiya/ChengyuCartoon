"""漫画生成页面"""
import streamlit as st
from nodes import cartoonist
from tools import merge_images_to_long
from front.utils import download_images, create_state
from front.config import app_logger
from front.components import render_page_title, reset_state

def render():
    """渲染漫画生成页面"""
    # 渲染页面标题（带下载列）
    col_title, col_download = render_page_title(show_download=True)
    
    # 下载按钮 - 只要有至少一张图片生成成功就显示
    with col_download:
        if st.session_state.cartoon:
            # 检查是否有成功生成的图片
            successful_images = [frame for frame in st.session_state.cartoon if frame.get("img_url")]
            if successful_images:
                # ZIP下载按钮
                try:
                    zip_buffer = download_images(st.session_state.cartoon)
                    st.download_button(
                        label="📥 下载所有图片",
                        data=zip_buffer,
                        file_name=f"{st.session_state.chengyu}_连环画.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"生成ZIP失败: {e}")
                    app_logger.error(f"生成ZIP失败: {e}", exc_info=True)
                
                # 长图下载按钮（放在下方）- 按需生成
                if 'long_image_buffer' not in st.session_state:
                    # 如果还没有生成长图，显示生成按钮
                    if st.button("📄 生成长图", use_container_width=True):
                        with st.spinner("正在生成长图..."):
                            try:
                                st.session_state.long_image_buffer = merge_images_to_long(st.session_state.cartoon)
                                app_logger.info("长图生成成功")
                                st.rerun()
                            except Exception as e:
                                st.error(f"生成长图失败: {e}")
                                app_logger.error(f"生成长图失败: {e}", exc_info=True)
                else:
                    # 如果已生成，显示下载按钮
                    st.download_button(
                        label="📄 下载长图",
                        data=st.session_state.long_image_buffer,
                        file_name=f"{st.session_state.chengyu}_连环画长图.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    # 提供重新生成按钮
                    if st.button("🔄 重新生成长图", use_container_width=True):
                        del st.session_state.long_image_buffer
                        st.rerun()
    
    # 生成漫画
    if not st.session_state.cartoon or not all(frame.get("img_url") for frame in st.session_state.cartoon):
        with st.spinner("正在生成漫画图片..."):
            try:
                style = st.session_state.selected_style or "国风插画"
                app_logger.info(f"开始生成漫画，成语: {st.session_state.chengyu}, 风格: {style}, 分镜数量: {len(st.session_state.script)}")
                current_state = create_state(
                    include_story=True,
                    include_script=True,
                    style=style,
                    pic_num=len(st.session_state.script)
                )
                cartoonist_node = cartoonist(st.session_state.llm, st.session_state.imgllm)
                result_state = cartoonist_node.generate_images(current_state)
                st.session_state.cartoon = result_state.get("cartoon", [])
                st.session_state.error = None
                success_count = sum(1 for frame in st.session_state.cartoon if frame.get("img_url"))
                app_logger.info(f"漫画生成完成，成功生成 {success_count}/{len(st.session_state.cartoon)} 张图片")
                # 生成完成后刷新页面以显示下载按钮
                st.rerun()
            except Exception as e:
                st.session_state.error = str(e)
                app_logger.error(f"生成漫画出错: {e}", exc_info=True)
                st.error(f"生成漫画出错: {e}")
    
    # 显示漫画
    if st.session_state.cartoon:
        st.markdown("### 生成的连环画")
        
        # 网格布局显示图片
        cols_per_row = 2
        for row_start in range(0, len(st.session_state.cartoon), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx, frame_idx in enumerate(range(row_start, min(row_start + cols_per_row, len(st.session_state.cartoon)))):
                with cols[col_idx]:
                    frame = st.session_state.cartoon[frame_idx]
                    img_url = frame.get("img_url")
                    
                    if img_url:
                        # 使用HTML和CSS在图片上添加序号标签
                        st.markdown(
                            f'''
                            <div class="image-container" style="position: relative; display: inline-block; width: 100%;">
                                <img src="{img_url}" style="width: 100%; display: block;" />
                                <div class="image-number-label">{frame_idx + 1}</div>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                        
                        # 重新生成按钮
                        if st.button(f"🔄 重新生成", key=f"regenerate_{frame_idx}", use_container_width=True):
                            # 重置该帧的图片
                            st.session_state.cartoon[frame_idx]["img_url"] = None
                            # 清除长图缓存，因为图片已改变
                            if 'long_image_buffer' in st.session_state:
                                del st.session_state.long_image_buffer
                            try:
                                current_state = create_state(
                                    include_story=True,
                                    include_script=True,
                                    include_cartoon=True,
                                    style=st.session_state.selected_style or "国风插画",
                                    pic_num=len(st.session_state.script)
                                )
                                cartoonist_node = cartoonist(st.session_state.llm, st.session_state.imgllm)
                                result_state = cartoonist_node.generate_images(current_state)
                                st.session_state.cartoon = result_state.get("cartoon", [])
                                st.rerun()
                            except Exception as e:
                                st.error(f"重新生成失败: {e}")
                    else:
                        st.info("图片生成中...")
    
    # 返回按钮
    col1, col2 = st.columns([4, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("返回重新开始", use_container_width=True):
            reset_state()

