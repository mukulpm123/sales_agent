Retail Insights Assistant (GenAI + Multi-Agent System)

📋 Overview
The Retail Insights Assistant is a GenAI-powered analytics solution designed to democratize access to sales data. It allows business users to ask natural language questions (e.g., "What were the top selling products in May?") and receive accurate, data-backed insights instantly.
The system utilizes a Multi-Agent Architecture orchestrated by LangGraph, performs high-speed data processing using DuckDB (OLAP), and leverages DeepSeek LLM for semantic understanding and insight generation.

✨ Key Features
Natural Language to SQL: Converts complex business questions into optimized DuckDB SQL queries.
Multi-Agent Reasoning:
Planner Agent: Analyzes the schema and determines which tables and columns are relevant.
Extractor Agent: Generates, cleans, and executes SQL queries.
Validator Agent: Interprets the raw data, validates the logic, and generates a human-readable summary.
Context Protection: Intelligent logic to truncate large datasets (e.g., limiting row previews) to prevent LLM Context Window overflows.
Thread-Safe Execution: Designed to handle Streamlit's threading model by managing isolated database connections per request.
Scalable Architecture: Built with a modular design allowing for easy migration from local CSVs to Cloud Data Warehouses.

📂 Directory Structure
code
Text
sales_agent/
├── data/                       # Raw CSV Data Files (Sales reports, Product masters)
├── src/                        # Source Code
│   ├── agents/                 # Agent Logic
│   │   ├── planner.py          # Schema mapping & intent resolution
│   │   ├── extractor.py        # SQL generation & execution
│   │   └── validator.py        # Data summarization & formatting
│   ├── engine/                 # Data Layer
│   │   ├── db_manager.py       # DuckDB connection handling
│   │   └── schema_loader.py    # Automatic schema inference
│   ├── prompts/                # System instructions & Prompt Engineering
│   └── utils/                  # Helper functions (LLM Factory)
├── app.py                      # Main Streamlit Application (Frontend)
├── requirements.txt            # Python Dependencies
├── scalability_roadmap.md      # Architecture design for 100GB+ scale
└── README.md                   # Project Documentation

🏗️ System Architecture
Frontend: Streamlit (Python-based UI).
Orchestration: LangGraph (Manages the state and flow between agents).
Inference Engine: DeepSeek-V3 (via OpenAI-compatible API).
Data Engine: DuckDB (In-memory SQL OLAP database).
🚀 Setup & Execution
1. Prerequisites
Python 3.10 or higher.
An API Key for DeepSeek (or an OpenAI-compatible provider).
2. Installation
Open your terminal in the project root (sales_agent/) and run:

# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

3. Configuration
Create a .env file in the root directory and add your API credentials:

DEEPSEEK_API_KEY=your_actual_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
4. Running the Application

streamlit run app.py
The application will open automatically in your default web browser at http://localhost:8501.

💡 Usage Examples
Once the app is running, try asking questions based on the provided sample data:
Sales Performance: "Show me the total sales amount from the Amazon report."
Product Insights: "Which SKU has the highest quantity sold in the Sale Report?"
Filtering: "List the distinct order IDs in the Amazon sale report." (The system automatically limits this to avoid crashing).
Comparisons: "Compare the total weight from May 2022 vs March 2021."

📈 Scalability (100GB+ Roadmap)
This project includes a detailed design for scaling from local CSVs to enterprise-level data processing.
Ingestion: Transition to Apache Kafka/Spark Streaming.
Storage: Migration from DuckDB to Snowflake/BigQuery.
Retrieval: Implementation of Vector Search (RAG) for unstructured metadata.
For the full technical strategy, please refer to scalability_roadmap.md included in the repository.

⚠️ Assumptions & Limitations
Data Source: The system currently ingests CSV files located in the data/ folder on startup.
Schema Inference: Column names are automatically sanitized to snake_case to ensure SQL compatibility.
Session Management: To ensure thread safety in the Streamlit environment, the DuckDB connection is refreshed for every new query. In a production environment, a persistent connection pool would be used.