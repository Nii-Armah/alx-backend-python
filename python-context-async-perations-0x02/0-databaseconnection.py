import sqlite3

class DatabaseConnection:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchall())