from typing import List, Optional
from typing_extensions import TypedDict


class ScriptFrame(TypedDict):
    text: str                  # 分镜文案
    user_modified: bool        # 用户是否修改 True/False
    keep: bool                 # 用户是否选择保留此分镜 True/False 或用于流式交互

class CartoonFrame(TypedDict):
    img_url: Optional[str]     # 生成的图片的url或路径，初始为None
    prompt: str                # 生成该图片的prompt（可为分镜文案或用户修改内容）
    user_modified: bool        # 用户是否修改生成图的内容 True/False
    keep: bool                 # 用户是否选择保留此漫画格 True/False

class State(TypedDict):
    chengyu: str
    story: str
    script: List[ScriptFrame]          # 分镜脚本，用户可修改或选择保留
    cartoon: List[CartoonFrame]        # 漫画分镜对应图片和内容，用户可修改或选择保留
    pic_num: int                       # 图片数量，等于分镜数量（len(script) == len(cartoon) >= 4）
    style: str                         # 用户自选图片风格，例如"国风"、"水墨"等，由前端传入
