import os
import pandas as pd
import re

def sanitize_column_name(col_name):
    # Remove special characters and spaces, convert to snake_case
    clean = re.sub(r'[^a-zA-Z0-9]', '_', col_name.strip())
    clean = re.sub(r'_+', '_', clean)
    return clean.lower().strip('_')

def load_data_and_get_schema(db_manager, data_dir="data"):
    """
    Loads all CSVs in data_dir into DuckDB and returns a schema string.
    """
    schema_info = []
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        return "No data directory found."

    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_dir, filename)
            table_name = filename.replace(".csv", "").replace(" ", "_").replace("-", "_").lower()
            
            # Load CSV to analyze headers first for sanitization
            try:
                df = pd.read_csv(file_path)
                df.columns = [sanitize_column_name(c) for c in df.columns]
                
                # Register in DuckDB
                db_manager.get_connection().register(table_name, df)
                
                # Get schema info
                cols = df.columns.tolist()
                dtypes = df.dtypes.to_dict()
                col_desc = ", ".join([f"{k} ({v})" for k,v in dtypes.items()])
                
                schema_info.append(f"Table Name: {table_name}\nColumns: {col_desc}\n")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    return "\n".join(schema_info)