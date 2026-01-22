import pandas as pd
from langchain_core.messages import SystemMessage
from src.utils.llm_factory import get_deepseek_llm
from src.prompts.agent_prompts import VALIDATOR_SYSTEM_PROMPT

def validator_agent(state):
    print("--- DEBUG: Starting Validator Agent ---")
    question = state['question']
    sql_query = state['sql_query']
    data = state['data']
    
    # 1. Format Data for the LLM
    try:
        if isinstance(data, str):
            data_str = f"Error: {data}"
        elif isinstance(data, pd.DataFrame):
            if data.empty:
                data_str = "No results found."
            else:
                # Limit rows to prevent Context Window overflow
                if len(data) > 50:
                    print(f"--- DEBUG: Truncating data (Rows: {len(data)}) ---")
                    # Using to_string is safer than to_markdown (avoids tabulate dependency issues)
                    data_preview = data.head(50).to_string(index=False)
                    data_str = (
                        f"⚠️ DATA TRUNCATED: The query returned {len(data)} rows. "
                        f"Only the first 50 are shown below.\n\n"
                        f"{data_preview}"
                    )
                else:
                    data_str = data.to_string(index=False) 
        else:
            data_str = str(data)
    except Exception as e:
        print(f"--- DEBUG: Error formatting data: {e} ---")
        data_str = str(data)

    print("--- DEBUG: Data formatted. Calling DeepSeek LLM... ---")

    # 2. Call LLM
    try:
        llm = get_deepseek_llm()
        messages = [
            SystemMessage(content=VALIDATOR_SYSTEM_PROMPT.format(
                question=question,
                sql_query=sql_query,
                data=data_str
            ))
        ]
        
        response = llm.invoke(messages)
        print("--- DEBUG: LLM Response received ---")
        return {"final_answer": response.content}
        
    except Exception as e:
        print(f"--- DEBUG: LLM Failed: {e} ---")
        return {"final_answer": f"I found the data, but failed to summarize it. \n\n**Data:**\n{data_str}"}