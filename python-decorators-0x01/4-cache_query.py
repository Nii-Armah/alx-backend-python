import functools
import sqlite3
import time

from typing import Callable

query_cache = {}


def with_db_connection(func: Callable) -> Callable:
    """Open and close a database connection for the given function."""
    @functools.wraps(func)
    def with_db_connections_wrapper(*args, **kwargs) -> list:
        conn = sqlite3.connect('users.db')
        result = func(conn, *args, **kwargs)
        conn.close()
        return result

    return with_db_connections_wrapper


def cache_query(func: Callable) -> Callable:
    def cache_query_wrapper(conn, query) -> list:
        if query not in query_cache:
            query_cache[query] = func(conn, query)

        return query_cache[query]

    return cache_query_wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


users = fetch_users_with_cache(query='SELECT * FROM users')
users_again = fetch_users_with_cache(query='SELECT * FROM users')
