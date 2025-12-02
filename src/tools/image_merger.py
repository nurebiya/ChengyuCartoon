import io
import requests
from typing import List, Dict
from PIL import Image


def merge_images_to_long(cartoon: List[Dict]) -> io.BytesIO:
    """
    将所有漫画图片垂直拼接成长图
    
    Args:
        cartoon: 漫画帧列表，每个元素包含 img_url 字段
        
    Returns:
        BytesIO: 拼接后的长图字节流
        
    Raises:
        ValueError: 如果没有可用的图片
        Exception: 图片下载或处理失败
    """
    images = []
    
    # 下载所有图片
    for idx, frame in enumerate(cartoon):
        img_url = frame.get("img_url")
        if img_url:
            try:
                response = requests.get(img_url, timeout=30)
                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    images.append(img)
            except Exception as e:
                raise Exception(f"下载第{idx+1}张图片失败: {e}")
    
    if not images:
        raise ValueError("没有可用的图片")
    
    # 计算总高度和最大宽度
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    
    # 创建新图片（白色背景）
    merged_image = Image.new('RGB', (max_width, total_height), color='white')
    
    # 垂直拼接
    current_height = 0
    for img in images:
        # 如果图片宽度不一致，居中放置
        if img.width < max_width:
            x_offset = (max_width - img.width) // 2
            merged_image.paste(img, (x_offset, current_height))
        else:
            merged_image.paste(img, (0, current_height))
        current_height += img.height
    
    # 转换为字节流
    output = io.BytesIO()
    merged_image.save(output, format='PNG')
    output.seek(0)
    return output

