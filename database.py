import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="7S8a6mir@12",
            database="student_management1",
            use_pure=True,
            connection_timeout=10
        )

        if connection.is_connected():
            print("Connected to LOCAL MySQL successfully!")
            return connection

    except Error as e:
        print("LOCAL MySQL connection error:", e)

    return None