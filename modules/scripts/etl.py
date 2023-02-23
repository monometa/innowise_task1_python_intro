from __future__ import annotations

import pandas as pd
from modules.db.database import Database, DatabaseConfig
from modules.logs.set_logging_conf import logger
from modules.sql.sql_queries import (
    create_rooms_tables_query,
    create_students_tables_query,
    drop_rooms_table_query,
    drop_students_table_query,
    check_if_students_table_exists_query,
    check_if_rooms_table_exists_query,
)


STUDENTS_DATA_PATH = "./data/raw/students.json"
ROOMS_DATA_PATH = "./data/raw/rooms.json"

PROCESSED_STUDENTS_DATA_PATH = "./data/processed/processed_students.json"
PROCESSED_ROOMS_DATA_PATH = "./data/processed/processed_rooms.json"

STUDENTS_TABLE = "students"
ROOMS_TABLE = "rooms"


class ETLProcess:
    """
    Represents the ETL process of `students` and `rooms` JSON files

    Information from JSON files transform and load into the PostgreSQL database.

    """

    def __init__(self, database: Database):
        self.db_config = DatabaseConfig()
        logger.debug(self.db_config.__dict__)
        self.db = database(db_config=self.db_config)

    def reorder_students_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reorders columns of students dataframe

        """
        reordered_columns = ["id", "name", "sex", "room", "birthday"]
        df = df[reordered_columns]
        return df

    def reorder_rooms_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reorders columns of `rooms` dataframe

        """
        reordered_columns = ["id", "name"]
        df = df[reordered_columns]
        return df

    def transform_raw_data(self) -> None:
        """
        Transforms raw data in dataframes and saves thus data as processed df

        """
        df_students = pd.read_json(STUDENTS_DATA_PATH)
        df_rooms = pd.read_json(ROOMS_DATA_PATH)

        df_students = self.reorder_students_columns(df_students)
        df_rooms = self.reorder_rooms_columns(df_rooms)

        df_students.to_json(
            PROCESSED_STUDENTS_DATA_PATH, orient="records", date_format="iso"
        )
        df_rooms.to_json(PROCESSED_ROOMS_DATA_PATH, orient="records")

    def create_tables(self) -> None:
        """
        Creates new tables `rooms` and `students` in PostgreSQL if they don't exist

        """
        table_query_manager = {
            "rooms": {
                "create_query": create_rooms_tables_query,
                "check_query": check_if_rooms_table_exists_query,
            },
            "students": {
                "create_query": create_students_tables_query,
                "check_query": check_if_students_table_exists_query,
            },
        }
        for table, queries in table_query_manager.items():
            check = self.db.query(queries["check_query"])[0][0]
            if not check:
                self.db.execute(queries["create_query"])
                logger.info(f"Table {table} was created successfully")
            else:
                logger.info(f"Table {table} is already exists")

    def drop_tables(self) -> None:
        self.db.execute(drop_students_table_query)
        logger.info("Table `students` was dropped successfully")
        self.db.execute(drop_rooms_table_query)
        logger.info("Table `rooms` was dropped successfully")

    def load_to_db(self, students_path: str, rooms_path: str) -> None:
        """
        Loads processed `students` and `rooms` dataframes to PostgreSQL if tables are empty

        """
        df_rooms = pd.read_json(rooms_path, orient="records")
        df_students = pd.read_json(students_path, orient="records")
        self._append_to_table(df_rooms, ROOMS_TABLE)
        self._append_to_table(df_students, STUDENTS_TABLE)

    def _append_to_table(self, df: pd.DataFrame, table: str) -> None:
        """
        Appends rows to database table if the table is empty

        """
        if self._check_is_table_empty(table):
            df.to_sql(table, con=self.db.engine, if_exists="append", index=False)
            logger.debug(f"Rows were appended to `{table}` table")
        else:
            logger.debug(f"`{table}` table is not empty")

    def _check_is_table_empty(self, table: str) -> bool:
        """
        Checks if the table is empty

        """
        return self._count_table_rows(table) == 0

    def run(self) -> None:
        """
        Runs the an ETL process and executes extract, transform and load stages

        """
        self.transform_raw_data()
        self.create_tables()
        self.load_to_db(
            students_path=PROCESSED_STUDENTS_DATA_PATH,
            rooms_path=PROCESSED_ROOMS_DATA_PATH,
        )

    def extract_from_db(self, path: str, table: str, format) -> None:
        """
        Defines a function call to extract data from database based on the specified format

        """

        filepath = path + f".{format}"
        if format == "json":
            self._fetch_table_json(filepath, table)
        elif format == "xml":
            self._fetch_table_xml(filepath, table)

    def _fetch_table_json(self, path: str, table: str) -> None:
        """
        Extracts data from the database in the JSON format and saves to the specified path

        """
        with self.db.engine.begin() as conn:
            df = pd.read_sql_table(
                table_name=table, con=conn, parse_dates={"birthday": "%Y-%m-%d"}
            )
        df.to_json(path, orient="records", date_format="iso")
        logger.info(
            f"Data from {table} table is avaliable in the following path: {path}"
        )

    def _fetch_table_xml(self, path: str, table: str) -> None:
        """
        Extracts data from the database in the XML format and saves to the specified path

        """
        with self.db.engine.begin() as conn:
            df = pd.read_sql_table(
                table_name=table, con=conn, parse_dates={"birthday": "%Y-%m-%d"}
            )
        df.to_xml(path, index=None)
        logger.info(
            f"Data from {table} table is avaliable in the following path: {path}"
        )

    def _count_table_rows(self, table: str) -> int:
        """
        Gets total amount of rows in selected table

        """
        table_rows = int(self.db.query(f"""select count(id) from {table}""")[0][0])
        logger.debug(f"Table {table} has {table_rows} rows")
        return table_rows
