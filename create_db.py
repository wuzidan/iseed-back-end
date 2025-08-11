import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

try:
    # 连接到MySQL服务器（不指定数据库）
    cnx = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = cnx.cursor()
    
    # 创建数据库（如果不存在）
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'")
    print(f"数据库 '{DB_NAME}' 创建成功或已存在")
    
    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("错误：用户名或密码不正确")
    elif err.errno == errorcode.ER_BAD_HOST_ERROR:
        print("错误：无法连接到MySQL服务器")
    else:
        print(f"错误：{err}")
    exit(1)

exit(0)