from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 session 管理

# 模拟的用户数据
users = {
    "teacher": {"username": "t1", "password": "t123", "role": "teacher", "courses": []},
    "student": {"username": "s1", "password": "s123", "role": "student", "courses": []},
    "admin": {"username": "a1", "password": "a123", "role": "admin"}
}

def get_connection():
    """获取 PostgreSQL 数据库连接"""
    return psycopg2.connect(
        dbname="school",
        user="postgres",
        password="lyq20040510",
        host="localhost",
        port="5432"
    )

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # 检查用户名、密码和角色
        if role in users and users[role]["username"] == username and users[role]["password"] == password:
            session['username'] = username
            session['role'] = role
            if role == "teacher":
                return redirect(url_for('teacher_dashboard'))
            elif role == "student":
                return redirect(url_for('student_dashboard'))
            elif role == "admin":
                return redirect(url_for('admin_dashboard'))
        else:
            return "登录失败，请检查用户名、密码和角色"
    return render_template('login.html')

@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'username' not in session or session['role'] != 'teacher':
        return redirect(url_for('home'))  # 如果未登录或不是教师，重定向到登录页

    username = session['username']
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # 查询该教师教授的课程及学生成绩
    cur.execute("""
        SELECT students.sid, students.sname, courses.cid, cname, score
        FROM teachers
        LEFT JOIN choices ON teachers.tid = choices.tid
        LEFT JOIN courses ON choices.cid = courses.cid
        LEFT JOIN students ON choices.sid = students.sid
        WHERE teachers.tname = %s;
    """, (username,))
    courses = cur.fetchall()

    cur.close()
    conn.close()

    # 将课程信息传递给模板
    return render_template('teacher_dashboard.html', courses=courses)

@app.route('/update_score', methods=['POST'])
def update_score():
    if 'username' not in session or session['role'] != 'teacher':
        return redirect(url_for('home'))  # 如果未登录或不是教师，重定向到登录页

    sid = request.form['sid']
    cid = request.form['cid']
    new_score = request.form['score']

    conn = get_connection()
    cur = conn.cursor()

    # 更新学生成绩
    cur.execute("""
        UPDATE choices
        SET score = %s
        WHERE sid = %s AND cid = %s;
    """, (new_score, sid, cid))

    conn.commit()
    cur.close()
    conn.close()

    flash('成绩更新成功！', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))  # 如果未登录或不是学生，重定向到登录页

    username = session['username']
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # 查询该学生选修的课程
    cur.execute("""
        SELECT courses.cid, courses.cname, courses.hour, choices.score
        FROM students
        JOIN choices ON students.sid = choices.sid
        JOIN courses ON choices.cid = courses.cid
        WHERE students.sname = %s;
    """, (username,))
    enrolled_courses = cur.fetchall()

    # 查询所有课程
    cur.execute("SELECT * FROM courses")
    all_courses = cur.fetchall()

    cur.close()
    conn.close()

    # 将课程信息传递给模板
    return render_template('student_dashboard.html', enrolled_courses=enrolled_courses, all_courses=all_courses)

@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))  # 如果未登录或不是学生，重定向到登录页

    sid = request.form['sid']
    cid = request.form['cid']

    conn = get_connection()
    cur = conn.cursor()

    # 检查是否已经选过该课程
    cur.execute("SELECT * FROM choices WHERE sid = %s AND cid = %s", (sid, cid))
    if cur.fetchone():
        flash('您已经选过该课程！', 'error')
    else:
        # 插入选课记录
        cur.execute("INSERT INTO choices (sid, cid, score) VALUES (%s, %s, %s)", (sid, cid, 0))
        conn.commit()
        flash('选课成功！', 'success')

    cur.close()
    conn.close()
    return redirect(url_for('student_dashboard'))

@app.route('/drop_course', methods=['POST'])
def drop_course():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))  # 如果未登录或不是学生，重定向到登录页

    sid = request.form['sid']
    cid = request.form['cid']

    conn = get_connection()
    cur = conn.cursor()

    # 删除选课记录
    cur.execute("DELETE FROM choices WHERE sid = %s AND cid = %s", (sid, cid))
    conn.commit()

    cur.close()
    conn.close()
    flash('退课成功！', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/admin_dashboard')
def admin_dashboard():
    return "管理员仪表盘"

if __name__ == '__main__':
    app.run(debug=True)