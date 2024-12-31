from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from dev import conn


app = Flask(__name__)




# 主页面
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_role = request.form.get('role')
        password = request.form.get('password')

        if user_role == 'student':
            if password == '123456':
                return jsonify({'redirect': url_for('')}) # 对应的前端
            else:
                return jsonify({'error': '学生密码错误！'}), 400
        elif user_role == 'admin':
            if password == '123456':
                return jsonify({'redirect': url_for('')}) # 对应的前端
            else:
                return jsonify({'error': '管理员密码错误！'}), 400
        elif user_role == 'teacher':
            if password == '123456':
                return jsonify({'redirect': url_for('')}) # 对应的前端
            else:
                return jsonify({'error': '教师密码错误！'}), 400

    return render_template('index.html')

# 学生面板路由
@app.route('/studentPage', methods=['GET'])
def student_dashboard():
    return render_template('studentPage.html')  # 显示学生选课页面



# 教师面板路由
@app.route('/teacherlogin', methods=['GET'])
def teacher_dashboard():
    return render_template('teacherlogin.html')  # 显示教师管理课程页面

# 后端API (连接js)

## 管理员管理课程部分
@app.route('/api/admin/course', methods=['POST'])
def add_course():
    data = request.get_json()
    cid = data.get('cid')
    cname = data.get('cname')
    chour = data.get('chour') # need to adjust

    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO courses (cid, chour, cname) 
        VALUES (%s, %s, %s)
    """, (cid, chour, cname))

    conn.commit()
    conn.close()

    return jsonify({"message": "课程添加成功"})

@app.route('/api/admin/course/<int:cid>', methods=['PUT'])
def edit_course(cid):
    data = request.get_json()
    cname = data.get('cname')
    chour = data.get('chour')

    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE courses
        SET cname = %s, chour = %s
        WHERE cid = %s
    """, (cname, chour, cid))

    conn.commit()
    conn.close()

    return jsonify({"message": "课程信息更新成功"})

@app.route('/api/admin/course/<int:cid>', methods=['DELETE'])
def delete_course(cid):
    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM courses WHERE cid = %s
    """, (cid,))

    conn.commit()
    conn.close()

    return jsonify({"message": "课程删除成功"})

@app.route('/api/admin/courses', methods=['GET'])
def search_courses():
    cname = request.args.get('cname', '')

    #conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM courses WHERE cname = %s
    """, ('%' + cname + '%',))
    
    courses = cursor.fetchall()
    conn.close()

    return jsonify(courses)

'''
@app.route('/api/admin/course/reset_password/<int:course_id>', methods=['POST'])
def reset_password(course_id):
    new_password = 'new_password'

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE course SET password = %s WHERE course_id = %s
    """, (new_password, course_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "密码已重置"})

@app.route('/api/admin/reset_all_passwords', methods=['POST'])
def reset_all_passwords():
    new_password = 'new_password'

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE course SET password = %s
    """, (new_password,))

    conn.commit()
    conn.close()

    return jsonify({"message": "所有课程的密码已重置"})
'''

## 管理员管理学生部分
# 添加学生接口
@app.route('/api/admin/student', methods=['POST'])
def add_student():
    data = request.get_json()
    student_id = data.get('id')
    name = data.get('name')
    gender = data.get('gender')
    birth_year = data.get('birthYear')
    major = data.get('major')
    enrollment_year = data.get('enrollmentYear')
    department = data.get('department')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student (student_id, name, gender, birth_year, major, enrollment_year, department)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (student_id, name, gender, birth_year, major, enrollment_year, department))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生添加成功"})

# 编辑学生信息接口
@app.route('/api/admin/student/<int:student_id>', methods=['PUT'])
def edit_student(student_id):
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    birth_year = data.get('birthYear')
    major = data.get('major')
    enrollment_year = data.get('enrollmentYear')
    department = data.get('department')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE student
        SET name = %s, gender = %s, birth_year = %s, major = %s, enrollment_year = %s, department = %s
        WHERE student_id = %s
    """, (name, gender, birth_year, major, enrollment_year, department, student_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生信息更新成功"})

# 删除学生信息接口
@app.route('/api/admin/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM student WHERE student_id = %s
    """, (student_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生删除成功"})

# 重置学生密码接口
@app.route('/api/admin/student/reset_password/<int:student_id>', methods=['POST'])
def reset_password(student_id):
    new_password = 'new_password'  # 设置新的密码，通常会用随机生成的密码或临时密码

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE student SET password = %s WHERE student_id = %s
    """, (new_password, student_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生密码已重置"})

# 重置所有学生密码接口
@app.route('/api/admin/reset_all_student_passwords', methods=['POST'])
def reset_all_student_passwords():
    new_password = 'new_password'  # 设置新的密码

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE student SET password = %s
    """, (new_password,))

    conn.commit()
    conn.close()

    return jsonify({"message": "所有学生的密码已重置"})

# 获取学生信息接口（可以进行分页和搜索）
@app.route('/api/admin/students', methods=['GET'])
def get_students():
    name = request.args.get('name', '')  # 用于搜索学生名字

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM student WHERE name LIKE %s
    """, ('%' + name + '%',))

    students = cursor.fetchall()
    conn.close()

    return jsonify(students)

## 管理员管理老师部分
# 获取教师列表（分页查询）
@app.route('/api/admin/teachers', methods=['GET'])
def get_teachers():
    page = int(request.args.get('page', 1))  # 页码
    per_page = int(request.args.get('per_page', 10))  # 每页显示多少教师

    offset = (page - 1) * per_page  # 分页偏移量

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM teacher LIMIT %s OFFSET %s
    """, (per_page, offset))

    teachers = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM teacher
    """)
    
    total_teachers = cursor.fetchone()['count']
    total_pages = (total_teachers // per_page) + (1 if total_teachers % per_page else 0)

    conn.close()

    return jsonify({
        'teachers': teachers,
        'current_page': page,
        'total_pages': total_pages,
    })

# 添加教师
@app.route('/api/admin/teacher', methods=['POST'])
def add_teacher():
    data = request.get_json()
    teacher_id = data.get('id')
    name = data.get('name')
    gender = data.get('gender')
    birth_year = data.get('birthYear')
    education = data.get('education')
    title = data.get('title')
    hire_year = data.get('hireYear')
    department = data.get('department')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teacher (teacher_id, name, gender, birth_year, education, title, hire_year, department)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (teacher_id, name, gender, birth_year, education, title, hire_year, department))

    conn.commit()
    conn.close()

    return jsonify({"message": "教师添加成功"})

# 编辑教师信息
@app.route('/api/admin/teacher/<int:teacher_id>', methods=['PUT'])
def edit_teacher(teacher_id):
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    birth_year = data.get('birthYear')
    education = data.get('education')
    title = data.get('title')
    hire_year = data.get('hireYear')
    department = data.get('department')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teacher
        SET name = %s, gender = %s, birth_year = %s, education = %s, title = %s, hire_year = %s, department = %s
        WHERE teacher_id = %s
    """, (name, gender, birth_year, education, title, hire_year, department, teacher_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "教师信息更新成功"})

# 删除教师
@app.route('/api/admin/teacher/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM teacher WHERE teacher_id = %s
    """, (teacher_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "教师删除成功"})

# 重置教师密码
@app.route('/api/admin/teacher/reset_password/<int:teacher_id>', methods=['POST'])
def reset_password(teacher_id):
    new_password = 'new_password'  # 可以设置为系统生成密码

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teacher SET password = %s WHERE teacher_id = %s
    """, (new_password, teacher_id))

    conn.commit()
    conn.close()

    return jsonify({"message": f"教师 {teacher_id} 密码已重置"})

# 重置所有教师密码
@app.route('/api/admin/reset_all_teacher_passwords', methods=['POST'])
def reset_all_passwords():
    new_password = 'new_password'  # 可以设置为系统生成密码

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teacher SET password = %s
    """, (new_password,))

    conn.commit()
    conn.close()

    return jsonify({"message": "所有教师密码已重置"})


## 学生选课部分
# 获取课程列表（分页查询）
@app.route('/api/student/courses', methods=['GET'])
def get_courses():
    page = int(request.args.get('page', 1))  # 页码
    per_page = int(request.args.get('per_page', 10))  # 每页显示多少课程

    offset = (page - 1) * per_page  # 分页偏移量

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM course LIMIT %s OFFSET %s
    """, (per_page, offset))

    courses = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM course
    """)
    
    total_courses = cursor.fetchone()['count']
    total_pages = (total_courses // per_page) + (1 if total_courses % per_page else 0)

    conn.close()

    return jsonify({
        'courses': courses,
        'current_page': page,
        'total_pages': total_pages,
    })

# 学生选课
@app.route('/api/student/select_course', methods=['POST'])
def select_course():
    data = request.get_json()
    course_id = data.get('course_id')
    student_id = data.get('student_id')

    # 检查课程是否已满
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM course WHERE course_id = %s
    """, (course_id,))

    course = cursor.fetchone()

    if not course:
        conn.close()
        return jsonify({"error": "课程不存在"}), 404

    if course['nownumber'] >= course['limit']:
        conn.close()
        return jsonify({"error": "课程人数已满，无法选课"}), 400

    # 检查学生是否已经选了这门课
    cursor.execute("""
        SELECT * FROM student_course WHERE student_id = %s AND course_id = %s
    """, (student_id, course_id))

    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "你已经选了这门课"}), 400

    # 选课操作
    cursor.execute("""
        INSERT INTO student_course (student_id, course_id)
        VALUES (%s, %s)
    """, (student_id, course_id))

    # 更新课程的现有人数
    cursor.execute("""
        UPDATE course SET nownumber = nownumber + 1 WHERE course_id = %s
    """, (course_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "选课成功"})

# 学生退课
@app.route('/api/student/drop_course', methods=['POST'])
def drop_course():
    data = request.get_json()
    course_id = data.get('course_id')
    student_id = data.get('student_id')

    conn = get_connection()
    cursor = conn.cursor()

    # 检查学生是否选了这门课
    cursor.execute("""
        SELECT * FROM student_course WHERE student_id = %s AND course_id = %s
    """, (student_id, course_id))

    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "你没有选这门课"}), 400

    # 退课操作
    cursor.execute("""
        DELETE FROM student_course WHERE student_id = %s AND course_id = %s
    """, (student_id, course_id))

    # 更新课程的现有人数
    cursor.execute("""
        UPDATE course SET nownumber = nownumber - 1 WHERE course_id = %s
    """, (course_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "退课成功"})

# 重置所有课程密码
@app.route('/api/admin/reset_all_course_passwords', methods=['POST'])
def reset_all_course_passwords():
    new_password = 'new_password'  # 可以设置为系统生成密码

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE course SET password = %s
    """, (new_password,))

    conn.commit()
    conn.close()

    return jsonify({"message": "所有课程密码已重置"})


## 老师管理课程
# 获取课程列表（分页查询）
@app.route('/api/teacher/courses', methods=['GET'])
def get_courses():
    page = int(request.args.get('page', 1))  # 页码
    per_page = int(request.args.get('per_page', 10))  # 每页显示多少课程

    offset = (page - 1) * per_page  # 分页偏移量

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM course LIMIT %s OFFSET %s
    """, (per_page, offset))

    courses = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM course
    """)
    
    total_courses = cursor.fetchone()['count']
    total_pages = (total_courses // per_page) + (1 if total_courses % per_page else 0)

    conn.close()

    return jsonify({
        'courses': courses,
        'current_page': page,
        'total_pages': total_pages,
    })

# 添加课程
@app.route('/api/teacher/course', methods=['POST'])
def add_course():
    data = request.get_json()
    course_id = data.get('id')
    name = data.get('name')
    teacher = data.get('teacher')
    credits = data.get('credits')
    semester = data.get('semester')
    course_type = data.get('type')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO course (course_id, course_name, teacher_name, credits, semester, course_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (course_id, name, teacher, credits, semester, course_type))

    conn.commit()
    conn.close()

    return jsonify({"message": "课程添加成功"})

# 编辑课程
@app.route('/api/teacher/course/<int:course_id>', methods=['PUT'])
def edit_course(course_id):
    data = request.get_json()
    name = data.get('name')
    teacher = data.get('teacher')
    credits = data.get('credits')
    semester = data.get('semester')
    course_type = data.get('type')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE course
        SET course_name = %s, teacher_name = %s, credits = %s, semester = %s, course_type = %s
        WHERE course_id = %s
    """, (name, teacher, credits, semester, course_type, course_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "课程信息更新成功"})

# 删除课程
@app.route('/api/teacher/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM course WHERE course_id = %s
    """, (course_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "课程删除成功"})

## 登出，只需实现一次即可
@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({"message": "成功退出"})



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)