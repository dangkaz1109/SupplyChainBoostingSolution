import duckdb
import os

class DataEngine:
    def __init__(self, db_path="data/warehouse.duckdb"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.con = duckdb.connect(db_path)
        
    def execute(self, query):
        return self.con.execute(query)

    def close(self):
        self.con.close()