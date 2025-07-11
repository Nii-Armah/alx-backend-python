import sqlite3
import functools
from typing import Callable

def log_queries(func: Callable) -> Callable:
    """Log db query"""
    @functools.wraps(func)
    def log_queries_wrapper(query, *args, **kwarg):
        print('Query:',  query)
        return func(query, *args, **kwarg)

    return log_queries_wrapper



@log_queries
def fetch_all_users(query: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results