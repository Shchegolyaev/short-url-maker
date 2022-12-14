import os


def check_db_connect():
    if (os.system(
            "pg_isready --dbname=postgres-fastapi --host=localhost "
            "--port=5432 --username=postgres") == 0):
        return "accepting connections"
    else:
        return "no response"
