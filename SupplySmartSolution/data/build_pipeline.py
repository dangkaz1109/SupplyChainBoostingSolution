from data.data_engine import DataEngine # Correct absolute import

def build_bronze(engine: DataEngine, path, table_name):
    query = f"""
    CREATE OR REPLACE TABLE bronze_{table_name} AS
    SELECT * FROM read_csv_auto('{path}', ignore_errors=true);
    """
    engine.execute(query)
    return query

def build_silver(engine: DataEngine):
    query = f""
    engine.execute(query)
    
def build_gold(engine: DataEngine):
    query = f""
    engine.execute(query)
