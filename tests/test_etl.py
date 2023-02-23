from tests.test_sql_queries import (
    show_tables_fron_test_db,
    get_rooms_query,
    get_students_query,
)


def test_reorder_students_correct_order(etl_obj, raw_students_df, stg_students_df):
    df_tested = etl_obj.reorder_students_columns(raw_students_df)
    assert all(df_tested.columns == stg_students_df.columns)


def test_reorder_rooms_correct_order(etl_obj, raw_rooms_df, stg_rooms_df):
    df_tested = etl_obj.reorder_rooms_columns(raw_rooms_df)
    assert all(df_tested.columns == stg_rooms_df.columns)


def test_check_if_tables_exists(etl_obj):
    etl_obj.create_tables()
    assert len(etl_obj.db.query(show_tables_fron_test_db)) == 2


def test_load_to_db(running_etl, df_paths):
    running_etl.load_to_db(df_paths["stg"]["students"], df_paths["stg"]["rooms"])
    assert len(running_etl.db.query(get_students_query)) == 5
    assert len(running_etl.db.query(get_rooms_query)) == 5
