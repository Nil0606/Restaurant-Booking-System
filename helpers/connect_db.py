import os
from pathlib import Path
import sys
import MySQLdb
from MySQLdb import OperationalError, ProgrammingError

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from config import DATABASE  # Automatically import config


class DBConnect:

    def __init__(self):
        """
        Initialize DBConnect using DATABASE config from config.py
        """
        print("inside db")
        self.config = DATABASE
        print(f"{self.config}")
        self.conn = None
        self.connect()
        print("after connect")

    def connect(self):
        """Establish a MySQL connection."""
        try:
            print("inside connect")
            self.conn = MySQLdb.connect(
                host=self.config.get("host", "localhost"),
                user=self.config.get("user"),
                passwd=self.config.get("password"),
                db=self.config.get("database"),
                port=self.config.get("port", 3306),
                connect_timeout=5,
                charset="utf8mb4",
            )
            print("after connect")
            if self.conn:
                print("✅ Database connection established successfully.")
            else:
                print("Kantanadyo")
        except (OperationalError, ProgrammingError) as e:
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
        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, params or ())
            result = cursor.fetchone() if one else cursor.fetchall()
            cursor.close()
            return result
        except (OperationalError, ProgrammingError) as e:
            print(f"❌ Error executing query: {e}")
            return None

    def execute_query(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        :param query: SQL query string
        :param params: tuple/list of parameters
        :return: number of affected rows
        """
        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            self.conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            print(f"✅ Query executed successfully, {affected_rows} row(s) affected.")
            return affected_rows
        except (OperationalError, ProgrammingError) as e:
            print(f"❌ Error executing query: {e}")
            self.conn.rollback()
            return 0

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed.")
