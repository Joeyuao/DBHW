import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="school",
    auth_plugin='mysql_native_password'
)