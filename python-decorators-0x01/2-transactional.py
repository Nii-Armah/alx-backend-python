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


def transactional(func: Callable) -> Callable:
    """Make db transaction atomic."""
    @functools.wraps(func)
    def transactional_wrapper(conn, *args, **kwargs) -> None:
        try:
            func(conn, *args, **kwargs)
            conn.commit()
        except sqlite3.Error:
            conn.rollback()

    return transactional_wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email) -> None:
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET email = ? WHERE id = ?', (new_email, user_id))


update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
