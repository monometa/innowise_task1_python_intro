from modules.scripts.etl import ETLProcess
from modules.db.database import Database


def main():
    ETL = ETLProcess(database=Database)
    ETL.run()


if __name__ == "__main__":
    main()
