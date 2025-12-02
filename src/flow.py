from langgraph.graph import StateGraph, END
from nodes import storyteller, screenwriter, cartoonist
from state import State


def graph(llm, img_llm):
    workflow = StateGraph(State)

    workflow.add_node("storyteller", storyteller(llm).teller)
    workflow.add_node("screenwriter", screenwriter(llm).write_script)
    workflow.add_node("cartoonist", cartoonist(llm, img_llm).generate_images)

    workflow.add_edge("storyteller", "screenwriter")
    workflow.add_edge("screenwriter", "cartoonist")
    workflow.add_edge("cartoonist", END)

    workflow.set_entry_point("storyteller")

    return workflow.compile()
