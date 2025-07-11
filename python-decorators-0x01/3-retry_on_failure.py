import functools
import sqlite3
import time

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


def retry_on_failure(*, retries=0, delay=0):
    """Handle retrying of and delaying of transaction execution."""

    def decorator(func):
        @functools.wraps(func)
        def retry_on_failure_wrapper(*args, **kwargs):
            transient_errors = ['locked', 'busy', 'i/o error', 'too many open files']

            try:
                time.sleep(delay)
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                error_msg = str(e).lower()
                if any(word in error_msg for word in transient_errors):
                    for _ in range(retries):
                        try:
                            time.sleep(delay)
                            return func(*args, **kwargs)
                        except sqlite3.OperationalError:
                            continue

                raise e

        return retry_on_failure_wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute('select * from users')
    return cursor.fetchall()


users = fetch_users_with_retry()
print(users)
