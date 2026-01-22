import duckdb

class DBManager:
    def __init__(self, db_path=":memory:"):
        self.con = duckdb.connect(db_path)

    def execute_query(self, query):
        try:
            return self.con.sql(query).df()
        except Exception as e:
            return str(e)
    
    def get_connection(self):
        return self.con