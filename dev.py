from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
def get_connection():
    """获取 PostgreSQL 数据库连接"""
    return psycopg2.connect(
        dbname="school",
        user="postgres",
        password="lyq20040510",
        host="localhost",
        port="5432"
    )
conn = get_connection()
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("select max(no) from choices;")
t=cur.fetchone()['max']
print(type(t))