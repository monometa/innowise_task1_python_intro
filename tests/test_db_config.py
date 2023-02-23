from modules.db.db_conf import pg_connection_dict


def test_pg_conn_dict_is_not_empty():
    assert len(pg_connection_dict) != 0


def test_pg_conn_dict_containts_correct_number_of_params():
    assert len(pg_connection_dict) == 5


def test_pg_conn_dict_values_consist_of_strings_only():
    assert all(isinstance(value, str) for value in pg_connection_dict.values())
