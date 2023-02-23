from modules.db.db_conf import DatabaseConfig, pg_connection_dict
from modules.db.database import Database
from tests.test_sql_queries import students_amount_query
import pytest


pg_connection_dict_invalid = pg_connection_dict.copy()
pg_connection_dict_invalid["user"] = "non-valid-user"


def test_db_connection_with_correct_credits(db_session):
    assert db_session.connection


def test_query_returns_data_from_db(db_session):
    assert len(db_session.query("""SELECT pid FROM pg_stat_activity""")) != 0


def test_database_if_provided_wrong_config():
    with pytest.raises(SystemExit):
        Database(DatabaseConfig(pg_connection_dict_invalid))


def test_students_total_amount_equality(db_session):
    assert db_session.query(students_amount_query)[0][0] == 10000
