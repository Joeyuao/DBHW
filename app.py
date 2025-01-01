from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 session 管理

# 模拟的用户数据
users = {
    "teacher": {"username": "t1", "password": "t123", "role": "teacher", "courses": []},
    "student": {"username": "s1", "password": "s123", "role": "student", "courses": []},
    "admin": {"username": "a1", "password": "a123", "role": "admin"}
}

# 模拟的课程数据
courses = {
    "course1": {"name": "Mathematics", "teacher": "t1"},
    "course2": {"name": "Physics", "teacher": "t1"},
    "course3": {"name": "Chemistry", "teacher": "t2"}
}

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
        return redirect(url_for('home'))

    teacher_username = session['username']
    teacher_courses = {cid: course for cid, course in courses.items() if course['teacher'] == teacher_username}

    if request.method == 'POST':
        if 'add_course' in request.form:
            course_name = request.form['course_name']
            course_id = f"course{len(courses) + 1}"
            courses[course_id] = {"name": course_name, "teacher": teacher_username}
        elif 'delete_course' in request.form:
            course_id = request.form['course_id']
            if course_id in teacher_courses:
                del courses[course_id]
            else:
                return "删除失败，请检查课程 ID"

    return render_template('teacher_dashboard.html', courses=teacher_courses)

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))

    student = users['student']
    if request.method == 'POST':
        if 'enroll' in request.form:
            course_id = request.form['course_id']
            if course_id in courses and course_id not in student['courses']:
                student['courses'].append(course_id)
        elif 'drop' in request.form:
            course_id = request.form['course_id']
            if course_id in student['courses']:
                student['courses'].remove(course_id)

    enrolled_courses = {cid: courses[cid] for cid in student['courses']}
    available_courses = {cid: course for cid, course in courses.items() if cid not in student['courses']}

    return render_template('student_dashboard.html', enrolled_courses=enrolled_courses, available_courses=available_courses)

@app.route('/admin_dashboard')
def admin_dashboard():
    return "管理员仪表盘"

if __name__ == '__main__':
    app.run(debug=True)