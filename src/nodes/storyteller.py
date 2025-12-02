from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

from .basenode import basenode
from state.state import State
from tools import encyclo_reader, chengyulist
from prompts import STORY_PROMPT, ENCYCLO_PROMPT

class storyteller(basenode):

    def __init__(self, llm):
        super().__init__(llm, "storyteller")

    def chengyu_checker(self, chengyu: str) -> bool:
        return chengyu in chengyulist

    def teller(self, state: State) -> State:
        chengyu_input = state["chengyu"]
        if not self.chengyu_checker(chengyu_input):
            raise ValueError("请输入一个真实存在的成语")
        
        encyclo_content = encyclo_reader(chengyu_input)
        # encyclo_reader若返回有效故事背景，则直接基于背景生成故事；否则fall back
        if encyclo_content:
            messages = [
                {"role": "system", "content": ENCYCLO_PROMPT.format(chengyu=chengyu_input, encyclo_content=encyclo_content)}
            ]
            self.log_info("查询到成语背景，基于成语背景生成故事")
            #encyclo_reader.py被我设置为pass，所以此处默认走else分支，即基于模型知识生成故事
        else:
            messages = [
                {"role": "system", "content": STORY_PROMPT},
                {"role": "user", "content": chengyu_input}
            ]
            self.log_info("查询不到成语背景，直接基于模型知识生成故事")

        response = str(self.llm.invoke(messages))
        self.log_info(f"生成故事全文: {response}")

        updated_state = state.copy()
        updated_state["chengyu"] = chengyu_input
        updated_state["story"] = response
        if encyclo_content:
            updated_state["wiki"] = encyclo_content
        return updated_state



