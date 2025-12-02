from typing import List
import time
from .basenode import basenode
from state.state import State, ScriptFrame, CartoonFrame
from prompts import CARTOON_IMAGE_PROMPT 


# 候选漫画风格建议：
AVAILABLE_STYLES = [
    ("国风插画", "Chinese Traditional"),
    ("卡通彩绘", "Cartoon Color"),
    ("水墨丹青", "Ink Wash"),
    ("黑白线描", "Black & White Line Art"),
    ("简笔趣画", "Minimalist Doodle"),
    ("奇幻唯美", "Fantasy Art"),
]

class cartoonist(basenode):
    """
    cartoonist节点：根据 state["script"] 分镜脚本与 state["pic_num"] 生成漫画图片（img_url，图片url/path），
    并附加于 state["cartoon"][i]["img_url"] 字段。支持每帧独立生成或重生成，画面风格由 state["style"] 指定。

    可选风格（建议在前端radio或select展示）：
    1. 国风插画（Chinese Traditional）
    2. 卡通彩绘（Cartoon Color）
    3. 水墨丹青（Ink Wash）
    4. 黑白线描（Black & White Line Art）
    5. 简笔趣画（Minimalist Doodle）
    6. 奇幻唯美（Fantasy Art）
    可根据API实际能力增删。

    状态依赖说明：
    - 输入: state["script"]: List[ScriptFrame],  state["pic_num"]: int,  state["style"]: str
    - 输出: state["cartoon"]: List[CartoonFrame], 每帧[img_url]字段为图片url/path
    """
    def __init__(self, llm, image_generator):
        """
        image_generator: 必须实现 generate_image(prompt, style) -> str (图片URL)
        """
        super().__init__(llm, "cartoonist")
        self.image_generator = image_generator

    def generate_images(self, state: State) -> State:
        script: List[ScriptFrame] = state.get("script", [])
        pic_num: int = state.get("pic_num", len(script))
        # 风格映射（支持前端传中文或英文，后端可映射到API所需）
        style: str = state.get("style")


        # cartoon列表与script一一对应，长度一致
        cartoon: List[CartoonFrame] = state.get("cartoon", [])
        # 若cartoon未初始化或数量不同则重建，对应新版结构
        if not cartoon or len(cartoon) != len(script):
            cartoon = []
            for frame in script:
                cartoon.append({
                    "img_url": None,
                    "prompt": frame["text"],
                    "user_modified": False,
                    "keep": True
                })

        # 只对未生成（img_url字段为空）的帧生成图片
        for idx in range(min(pic_num, len(cartoon))):
            frame = cartoon[idx]
            # 已有图片且非空则跳过
            if frame.get("img_url"):
                continue
            text = frame.get("prompt") or script[idx]["text"]
            # 用prompt模板构造新描述
            # 先用style的APIname，后拼到prompt中
            style_api = style
            for zh, en in AVAILABLE_STYLES:
                if style == zh:
                    style_api = en
                    break
            # 添加重试机制：最多尝试3次，每次间隔1秒
            max_retries = 3
            img_url = None
            for attempt in range(1, max_retries + 1):
                try:
                    prompt_for_image = CARTOON_IMAGE_PROMPT.format(prompt=text, style=style_api)
                    img_url = self.image_generator.generate_image(prompt_for_image, style_api)
                    # 成功则跳出循环
                    if attempt > 1:
                        self.log_info(f"第{idx+1}帧图片生成成功（第{attempt}次尝试）")
                    break
                except Exception as e:
                    if attempt < max_retries:
                        self.log_info(f"第{idx+1}帧图片生成失败（第{attempt}次尝试），1秒后重试: {e}")
                        time.sleep(1)  # 等待1秒
                    else:
                        # 最后一次尝试也失败
                        self.log_error(f"第{idx+1}帧图片生成失败（已尝试{max_retries}次）: {e}")
                        img_url = None
            frame["img_url"] = img_url

        updated = state.copy()
        updated["cartoon"] = cartoon
        return updated

# - cartoon和script一一对应，结构按state.state.CartoonFrame为准。
# - 前端控制逐帧生成与重画逻辑；本函数只生成img_url==None的格。