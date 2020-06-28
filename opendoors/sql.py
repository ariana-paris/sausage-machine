from configparser import ConfigParser
from logging import Logger

import mysql.connector
import sqlparse
from mysql.connector import Error


class SqlDb:
    def __init__(self, config: ConfigParser, logger: Logger):
        self.config = config
        self.logger = logger
        self.conn = mysql.connector.connect(**self.get_db_config())
        self.logger.info(f"Connected to MySQL database server at {self.config['Database']['host']} "
                         f"as {self.config['Database']['user']}")

    def get_db_config(self):
        if not (self.config.has_section('Database')
                and self.config['Database']['user']
                and self.config['Database']['host']
                and self.config.has_option('Database', 'password')):
            host = input("MySQL host name (eg: localhost):\n>> ")
            user = input("MySQL user name (eg: root):\n>> ")
            password = input("MySQL password:\n>> ")
            self.config['Database'] = {
                'host': host,
                'user': user,
                'password': password
            }
        return self.config['Database']

    def load_sql_file_into_db(self, edited_sql_path: str):
        cursor = self.conn.cursor()
        try:
            with open(edited_sql_path, "r") as f:
                stmts = sqlparse.format(f.read(), None, strip_comments=True)
                raw_statements = sqlparse.split(stmts)
                for statement in raw_statements:
                    cursor.execute(statement)
                self.conn.commit()
        except Error as error:
            self.logger.error(error)
        finally:
            cursor.close()

    def read_table_to_dict(self, database: str, tablename: str):
        cursor = self.conn.cursor(dictionary=True, buffered=True)
        cursor.execute(f"SELECT * FROM {database}.{tablename};")
        return cursor.fetchall()

    def execute_and_fetchall(self, database: str, statement: str):
        cursor = self.conn.cursor(dictionary=True, buffered=True)
        cursor.execute(f"USE {database}")
        cursor.execute(statement)
        self.conn.commit()
        return cursor.fetchall()

    def execute(self, database: str, statement: str):
        cursor = self.conn.cursor(dictionary=True, buffered=True)
        cursor.execute(f"USE {database}")
        cursor.execute(statement)
        self.conn.commit()

    def read_table_with_total(self, database: str, table_name: str):
        old_table = self.read_table_to_dict(database, table_name)
        current = 0
        total = len(old_table)
        return old_table, current, total
