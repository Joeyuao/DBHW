import psycopg2

# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(
    host="localhost",  # 数据库主机地址
    user="postgres",       # 数据库用户名
    password="lyq20040510",       # 数据库密码
    database="school"  # 数据库名称
)