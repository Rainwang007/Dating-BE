import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='1wjtEFEL',
        database='dating_app'
    )

    if connection.is_connected():
        print("Successfully connected to MySQL database")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
