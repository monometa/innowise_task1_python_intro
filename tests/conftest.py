import pytest
import pandas as pd
from modules.db.database import Database, DatabaseConfig
from modules.scripts.etl import ETLProcess


RAW_STUDENTS_FILE = "./tests/test_data/processed_students.json"
RAW_ROOMS_FILE = "./tests/test_data/processed_rooms.json"

STG_STUDENTS_FILE = "./tests/test_data/processed_students.json"
STG_ROOMS_FILE = "./tests/test_data/processed_rooms.json"


@pytest.fixture
def df_paths():

    paths = {
        "raw": {
            "students": RAW_STUDENTS_FILE,
            "rooms": RAW_ROOMS_FILE,
        },
        "stg": {
            "students": STG_STUDENTS_FILE,
            "rooms": STG_ROOMS_FILE,
        },
    }
    return paths


@pytest.fixture
def db_session():
    db_config = DatabaseConfig()
    db = Database(db_config)
    yield db
    db.close()


@pytest.fixture
def stg_students_df():
    return pd.read_json(STG_STUDENTS_FILE)


@pytest.fixture
def stg_rooms_df():
    return pd.read_json(STG_ROOMS_FILE)


@pytest.fixture
def raw_students_df():
    return pd.read_json(RAW_STUDENTS_FILE)


@pytest.fixture
def raw_rooms_df():
    return pd.read_json(RAW_ROOMS_FILE)


@pytest.fixture
def test_connection_string():
    return "postgresql://admin:admin@postgres:5432/test"


@pytest.fixture
def etl_obj(test_connection_string, mocker):
    """Set up mock DB"""
    mocker.patch.object(
        DatabaseConfig, "get_conn_string", return_value=test_connection_string
    )
    etl_obj = ETLProcess(Database)
    return etl_obj


@pytest.fixture
def running_etl(etl_obj):
    etl_obj.create_tables()
    yield etl_obj
    etl_obj.drop_tables()
