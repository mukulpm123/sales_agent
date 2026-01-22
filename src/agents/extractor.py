from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.llm_factory import get_deepseek_llm
from src.prompts.agent_prompts import EXTRACTOR_SYSTEM_PROMPT

def extractor_agent(state):
    schema = state['schema']
    question = state['question']
    db_manager = state['db_manager']
    
    llm = get_deepseek_llm(temperature=0)
    messages = [
        SystemMessage(content=EXTRACTOR_SYSTEM_PROMPT.format(schema=schema, question=question)),
        HumanMessage(content="Generate the SQL now.")
    ]
    
    sql_query = llm.invoke(messages).content.strip()
    
    # Cleanup markdown
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    print(f"DEBUG: Executing SQL: {sql_query}")
    
    # Execute
    df_result = db_manager.execute_query(sql_query)
    
    # --- PERFORMANCE FIX: Don't print huge dataframes to console ---
    if isinstance(df_result, str):
        print(f"DEBUG: Result Error: {df_result}")
    else:
        print(f"DEBUG: Result Shape: {df_result.shape}") 
        # Only print the first 3 rows to console for debugging
        print(df_result.head(3).to_string()) 
    # ---------------------------------------------------------------
    
    return {"sql_query": sql_query, "data": df_result}