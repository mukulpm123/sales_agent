import streamlit as st
import pandas as pd
from langgraph.graph import StateGraph, END
from typing import TypedDict, Any

# Internal imports
from src.engine.db_manager import DBManager
from src.engine.schema_loader import load_data_and_get_schema
from src.agents.planner import planner_agent
from src.agents.extractor import extractor_agent
from src.agents.validator import validator_agent

# --- PAGE CONFIGURATION (Must be the first Streamlit command) ---
st.set_page_config(page_title="DeepSeek Retail Analyst", layout="wide")

# 1. Define State
class AgentState(TypedDict):
    question: str
    schema: str
    db_manager: Any
    plan: str
    sql_query: str
    data: Any
    final_answer: str

# 2. Schema Caching (Safe to cache text, but NOT the DB connection)
@st.cache_resource
def get_cached_schema():
    # We create a temporary DB just to read headers, then close it
    temp_db = DBManager()
    schema_text = load_data_and_get_schema(temp_db)
    return schema_text

schema = get_cached_schema()

# 3. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_agent)
workflow.add_node("extractor", extractor_agent)
workflow.add_node("validator", validator_agent)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "extractor")
workflow.add_edge("extractor", "validator")
workflow.add_edge("validator", END)

app_graph = workflow.compile()

# --- UI LAYOUT ---
st.title("🤖 DeepSeek Retail Insights Agent")

# Sidebar
with st.sidebar:
    st.header("Debug Info")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.text_area("Table Schema", schema, height=300)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"]) # st.write is safer than markdown for complex text

# Input Handling
if prompt := st.chat_input("Ask about sales..."):
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Process
    with st.spinner("Analyzing..."):
        try:
            # Create a FRESH Database Connection for this request
            # This fixes the "White Screen" caused by threading locks
            current_db = DBManager()
            # Reload data into this fresh connection
            load_data_and_get_schema(current_db) 

            inputs = {
                "question": prompt,
                "schema": schema,
                "db_manager": current_db
            }

            # Run Graph
            result = app_graph.invoke(inputs)
            
            # Extract Output
            final_ans = result.get("final_answer", "No answer.")
            sql_debug = result.get("sql_query", "")
            data_debug = result.get("data", None)

            # 3. Show Assistant Message
            with st.chat_message("assistant"):
                st.write(final_ans)
                
                # Debug Dropdown
                with st.expander("See Details"):
                    st.write("SQL Executed:")
                    st.code(sql_debug, language="sql")
                    
                    st.write("Data Preview:")
                    if isinstance(data_debug, pd.DataFrame):
                        st.dataframe(data_debug.head(10))
                    else:
                        st.write(str(data_debug))

            # 4. Save to History
            st.session_state.messages.append({"role": "assistant", "content": final_ans})
            
            # Force a success message to the log
            print("--- UI UPDATE SUCCESSFUL ---")

        except Exception as e:
            st.error(f"System Error: {e}")
            print(f"ERROR: {e}")