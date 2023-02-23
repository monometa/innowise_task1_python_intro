get_ten_students_query = """
    SELECT id, name FROM students LIMIT 10
    """

get_students_query = """
    SELECT * FROM students
    """

get_rooms_query = """
    SELECT * FROM rooms
    """


students_amount_query = """
    SELECT count(*) FROM students
    """

show_all_tables_query = """
SELECT * FROM pg_catalog.pg_tables;
"""

show_tables_fron_test_db = """select * from pg_tables where schemaname='public';
"""
