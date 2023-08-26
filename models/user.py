import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# 数据库配置
config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'dating_app'
}

def create_user(user_data):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    username = user_data['username']
    raw_password = user_data['password']
    hashed_password = generate_password_hash(raw_password, method='sha256')

    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_password))

    connection.commit()
    cursor.close()
    connection.close()

def check_user(username, password):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        stored_password = result[0]
        return check_password_hash(stored_password, password)

    return False
