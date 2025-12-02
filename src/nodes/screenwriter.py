from typing import List
from .basenode import basenode
from prompts import SCREENWRITER_PROMPT 
from state.state import State, ScriptFrame

class screenwriter(basenode):
    """
    screenwriter节点：将故事文本(state['story'])转为分镜脚本列表，供前端（streamlit）编辑。
    系统保证分镜数量:[4,10]之间，结构见ScriptFrame。state见state.state。
    """

    def __init__(self, llm):
        super().__init__(llm, "screenwriter")

    def write_script(self, state: State) -> State:
        """
        根据state["story"]生成4~10个分镜, 填入state["script"]与state["pic_num"].
        - LLM每次输出如果不合格则自动重试，最多3次。
        - 超过10个分镜保留前10个。
        """
        story = state.get("story", "")
        if not story or not story.strip():
            self.log_error("story字段为空，无法生成分镜。")
            raise ValueError("story字段为空，无法生成分镜脚本。")

        max_tries = 3
        min_frames = 4
        max_frames = 10

        final_lines: List[str] = []
        for attempt in range(1, max_tries + 1):
            messages = [
                {"role": "system", "content": SCREENWRITER_PROMPT},
                {"role": "user", "content": story.strip()}
            ]
            try:
                response = str(self.llm.invoke(messages))
            except Exception as e:
                self.log_error(f"LLM生成分镜失败（第{attempt}次）: {e}")
                if attempt == max_tries:
                    raise
                continue

            self.log_info(f"LLM分镜输出(第{attempt}次):\n{response}")

            
            lines = [frag.strip() for frag in response.strip().split(' ') if frag.strip()]

            if len(lines) < min_frames:
                self.log_error(f"分镜数量{len(lines)} < {min_frames}，重试。")
                continue
            if len(lines) > max_frames:
                self.log_info(f"分镜数量{len(lines)} > {max_frames}，截取前{max_frames}个。")
                lines = lines[:max_frames]
            final_lines = lines
            break
        else:
            self.log_error("多次尝试后，生成的分镜数量仍不足4个。")
            raise ValueError("分镜数量不足4个，请检查输入或优化prompt。")

        scripts: List[ScriptFrame] = [
            {
                "text": text,
                "user_modified": False,
                "keep": True  # 默认保留，供前端调整
            }
            for text in final_lines
        ]

        updated_state = state.copy()
        updated_state["script"] = scripts
        updated_state["pic_num"] = len(scripts)
        return updated_state
