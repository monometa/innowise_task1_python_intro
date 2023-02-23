create_students_tables_query = """
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name VARCHAR (50),
        sex VARCHAR (1),
        room INTEGER REFERENCES rooms (id) ON DELETE SET NULL,
        birthday date
    );
    """
create_rooms_tables_query = """
    CREATE TABLE rooms (
        id INTEGER PRIMARY KEY,
        name VARCHAR (30)
    );
    """

check_if_students_table_exists_query = (
    "select exists(select * from information_schema.tables where table_name='students')"
)

check_if_rooms_table_exists_query = (
    "select exists(select * from information_schema.tables where table_name='rooms')"
)

drop_students_table_query = """
    DROP TABLE students;
"""

drop_rooms_table_query = """
    DROP TABLE rooms;
"""
