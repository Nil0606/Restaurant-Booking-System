import mysql.connector
from mysql.connector import Error
from config import DATABASE  # Automatically import config


class DBConnect:

    def __init__(self):
        """
        Initialize DBConnect using DATABASE config from config.py
        """
        self.config = DATABASE
        self.conn = None
        self.connect()

    def connect(self):
        """Establish a MySQL connection."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            if self.conn.is_connected():
                print("✅ Database connection established successfully.")
        except Error as e:
            print(f"❌ Error connecting to database: {e}")
            self.conn = None

    def query_db(self, query, params=None, one=False):
        """
        Execute a SELECT query.
        :param query: SQL query string
        :param params: tuple/list of parameters
        :param one: if True, return only one record; else return all
        :return: one row (dict) or list of rows (list of dicts)
        """
        if not self.conn or not self.conn.is_connected():
            self.connect()

        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone() if one else cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"❌ Error executing query: {e}")
            return None

    def execute_query(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        :param query: SQL query string
        :param params: tuple/list of parameters
        :return: number of affected rows
        """
        if not self.conn or not self.conn.is_connected():
            self.connect()

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            self.conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            print(f"✅ Query executed successfully, {affected_rows} row(s) affected.")
            return affected_rows
        except Error as e:
            print(f"❌ Error executing query: {e}")
            self.conn.rollback()
            return 0

    def close(self):
        """Close the database connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("🔒 Database connection closed.")
