import psycopg2
from sqlalchemy import create_engine
from modules.logs.set_logging_conf import logger
from modules.db.db_conf import DatabaseConfig
import sys


class Database:
    """
    Allows to establish a connection with a PostgreSQL database and executes SQL queries

    Parameters
    ----------
    db_config : DatabaseConfig
                config class for initializing connection URI

    """

    def __init__(self, db_config: DatabaseConfig = DatabaseConfig):
        """
        Inits Database with received configuration

        Establishes a connection by psycopg2 and creates sqlalchemy engine

        """

        self.conn_string = db_config.get_conn_string()

        try:
            self._conn = psycopg2.connect(self.conn_string)
            if self._conn:
                logger.debug(f"Сonnection successfully established - {self._conn}")
        except (psycopg2.OperationalError) as e:
            logger.error(f"Connection failed: {e}")
            sys.exit(1)

        self._conn.autocommit = True
        self._cursor = self._conn.cursor()

        self.engine = create_engine(self.conn_string)

    @property
    def connection(self):
        """
        Gets a connection to PostgreSQL database

        """
        return self._conn

    @property
    def cursor(self):
        """
        Gets a cursor from connection to PostgreSQL database

        """
        return self._cursor

    def commit(self):
        """
        Commits changes to a PostgreSQL database

        """
        self.connection.commit()

    def close(self):
        """
        Closes current connection to PostgreSQL database

        """
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
