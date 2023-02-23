from argparse import ArgumentParser
from modules.scripts.etl import ETLProcess, STUDENTS_TABLE, ROOMS_TABLE
from modules.logs.set_logging_conf import logger
from pathvalidate.argparse import validate_filepath_arg
from modules.db.database import Database

# TO-DO: find an alternative for https://github.com/thombashi/pathvalidate or undestand why this package doesn't work


def main():

    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--students",
        type=validate_filepath_arg,
        help="select a folder in which to place the `students` data",
    )
    parser.add_argument(
        "-r",
        "--rooms",
        type=validate_filepath_arg,
        help="select a folder in which to place the `rooms` data",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["xml", "json"],
        help="select output format of data: json or xml",
        required=True,
    )
    args = parser.parse_args()

    if args.students is None and args.rooms is None:
        parser.error("At least `students` or `rooms` parameter required")

    logger.debug(f"Args params: {args.students}, {args.rooms}, {args.format}")

    requested_tables = {
        STUDENTS_TABLE: args.students,
        ROOMS_TABLE: args.rooms,
    }

    format = args.format
    etl = ETLProcess(Database)
    for table, path in requested_tables.items():
        if path:
            etl.extract_from_db(path, table, format)
        else:
            logger.debug(f"The path for {table} table wasn't provided")


if __name__ == "__main__":
    main()
