import psycopg2
from suppliers.config2 import load_config

def create_table():
    create_table_command = """
    CREATE TABLE snake (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(100),
        score INT
    );

    """
    config2 = load_config()
    with psycopg2.connect(**config2) as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_command)

if __name__ == '__main__':
    create_table()