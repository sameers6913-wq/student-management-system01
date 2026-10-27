import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from pathlib import Path

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the main project's .env file
load_dotenv(BASE_DIR / ".env")


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("AZURE_DB_HOST"),
            user=os.getenv("AZURE_DB_USER"),
            password=os.getenv("AZURE_DB_PASSWORD"),
            database=os.getenv("AZURE_DB_NAME"),
            port=int(os.getenv("AZURE_DB_PORT", 3306))
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection error:", e)

    return None