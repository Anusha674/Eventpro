import mysql.connector
from config import Config


def get_db():
    """Get a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None


def close_db(conn):
    """Close database connection."""
    if conn and conn.is_connected():
        conn.close()


def execute_query(query, params=None, fetch=True):
    """Execute a query and return results."""
    conn = get_db()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Query error: {e}")
        conn.rollback()
        return None
    finally:
        close_db(conn)


def execute_many(query, data):
    """Execute a query with multiple data sets."""
    conn = get_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.executemany(query, data)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Query error: {e}")
        conn.rollback()
        return False
    finally:
        close_db(conn)
