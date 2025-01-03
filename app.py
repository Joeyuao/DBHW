from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 session 管理

# 模拟的用户数据
users = {
    "teacher": {"username": "t1", "password": "t123", "role": "teacher", "courses": []},
    "student": {"username": "867650681", "password": "s123", "role": "student", "courses": []},#s1
    "admin": {"username": "a1", "password": "a123", "role": "admin"}
}

def get_connection():
    """获取 PostgreSQL 数据库连接"""
    return psycopg2.connect(
        dbname="local_1",
        user="postgres",
        password="20040417",
        host="localhost",
        port="5432"
    )
conn = get_connection()
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("select max(no) from choices;")
no=cur.fetchone()['max']+1
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
        WHERE students.sid = %s;
    """, (username,))
    enrolled_courses = cur.fetchall()

    # # 查询所有课程+老师 fuck,老师太多了，不好展示
    cur.execute("""
    WITH ranked_courses AS (
        SELECT
            courses.cid, courses.cname, courses.hour, courses.leastgrade, teachers.tname,teachers.tid,
            ROW_NUMBER() OVER (PARTITION BY courses.cname ORDER BY RANDOM()) AS rn
        FROM courses
        LEFT JOIN choices ON courses.cid = choices.cid
        LEFT JOIN teachers ON choices.tid = teachers.tid
    )
    SELECT cid, cname, hour, leastgrade, tname,tid
    FROM ranked_courses
    WHERE rn = 1;
    """)
    all_courses = cur.fetchall()

    cur.close()
    conn.close()

    # 将课程信息传递给模板
    return render_template('student_dashboard.html', enrolled_courses=enrolled_courses, all_courses=all_courses)

@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    global no
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))  # 如果未登录或不是学生，重定向到登录页

    sid = request.form['sid']
    cid = request.form['cid']
    tid = request.form['tid']
    leastgrade = request.form['leastgrade']
    # 学生年级
    # student_grade = request.form['leastgrade']
    conn = get_connection()
    cur = conn.cursor()

    # 检查是否已经选过该课程
    cur.execute("SELECT * FROM choices WHERE sid = %s AND cid = %s", (sid, cid))
    if cur.fetchone():
        flash('您已经选过该课程！', 'error')
    else:
        cur.execute("SELECT * FROM students WHERE sid = %s", (sid,))
        grade = cur.fetchone()  # 获取查询结果的第一行
        print("Grade:", grade)
        grade_value = 0
        if grade:
            grade_value = grade[3]  # 提取 leastgrade 字段的值
            print("Grade:", grade_value)
        else:
            print("No grade found for sid:", sid)
        # 插入选课记录
        print("leastgrade",leastgrade,"grade_value",grade_value)
        if int(leastgrade) > int(grade_value):
            flash('您的年级不足以选该课程！', 'error')
        else:
            print("sid",sid,"tid",tid,"cid",cid)
            cur.execute("INSERT INTO choices (no,sid, tid, cid, score) VALUES (%s,%s, %s, %s, %s)", (no,sid, tid, cid, 0))
            no=no+1
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
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))  # 如果未登录或不是管理员，重定向到登录页

    username = session['username']
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # 查询全部选课信息
    cur.execute("""
        SELECT * from choices;
    """)
    choices = cur.fetchall()

    cur.close()
    conn.close()

    # 将选课信息传递给模板
    return render_template('admin_dashboard.html', choices = choices)

if __name__ == '__main__':
    app.run(debug=True)
"""
select courses.cid, courses.cname, courses.hour,courses.leastgrade,teachers.tname,teachers.tid
from courses courses
left join choices on courses.cid = choices.cid
left join teachers on choices.tid = teachers.tid;
"""
# 老师可以改分数
# 学生可以选课、退课


#低于最低年级的学生不能选课
#没实现的：
# 加一个学分到课程表
#密码哈希