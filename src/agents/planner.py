from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.llm_factory import get_deepseek_llm
from src.prompts.agent_prompts import PLANNER_SYSTEM_PROMPT

def planner_agent(state):
    schema = state['schema']
    question = state['question']
    
    llm = get_deepseek_llm()
    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT.format(schema=schema)),
        HumanMessage(content=question)
    ]
    
    response = llm.invoke(messages)
    return {"plan": response.content}