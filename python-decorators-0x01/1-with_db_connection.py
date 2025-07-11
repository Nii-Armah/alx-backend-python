import functools
import sqlite3

from typing import Callable


def with_db_connection(func: Callable) -> Callable:
    """Open and close a database connection for the given function."""
    @functools.wraps(func)
    def with_db_connections_wrapper(*args, **kwargs) -> list:
        conn = sqlite3.connect('users.db')
        result = func(conn, *args, **kwargs)
        conn.close()
        return result

    return with_db_connections_wrapper


@with_db_connection
def get_user_by_id(conn, user_id) -> list | None:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()


user = get_user_by_id(user_id=1)
print(user)
