import os

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
DB = os.environ["DATABASE"]
USER = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

pg_connection_dict = {
    "host": HOST,
    "port": PORT,
    "db": DB,
    "user": USER,
    "password": PASSWORD,
}


class DatabaseConfig:
    """
    Generates the connection string for a PostgreSQL database from a dictionary of parameters

    """

    def __init__(self, pg_connection_dict: dict = pg_connection_dict):
        """
        Sets connection parameters for a DatabaseConfig instance

        """
        self.db = pg_connection_dict["db"]
        self.port = pg_connection_dict["port"]
        self.host = pg_connection_dict["host"]
        self.user = pg_connection_dict["user"]
        self.password = pg_connection_dict["password"]

    def get_conn_string(self):
        """
        Returns a PostgreSQL connection string as URI

        """
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
