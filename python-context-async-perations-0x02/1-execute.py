import sqlite3


class ExecuteQuery:
    def __init__(self, db_name: str, query: str, param: int):
        self.db_name = db_name
        self.query = query
        self.param = param
        self.conn = None

    def __enter__(self):
        conn = sqlite3.connect(self.db_name)
        self.conn = conn
        cursor = conn.cursor()
        cursor.execute(self.query, (self.param, ))
        return cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


with ExecuteQuery(db_name='users.db', query='SELECT * FROM users WHERE age > ?', param=25) as result:
    print(result)