from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from dev import conn


app = Flask(__name__)

# 主页面
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 学生登录页面
@app.route('/stulogin', methods=['GET'])
def stulogin():
    return render_template('stulogin.html')

# 教师登录页面
@app.route('/teachlogin', methods=['GET'])
def teachlogin():
    return render_template('teach.html')

# 管理员登录页面
@app.route('/Adminlogin', methods=['GET'])
def adminlogin():
    return render_template('Adminlogin.html')




# 后端API (连接js)

## 管理员管理课程部分
@app.route('/api/admin/courses', methods=['POST'])
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

@app.route('/api/admin/courses/<int:cid>', methods=['PUT'])
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

@app.route('/api/admin/courses/<int:cid>', methods=['DELETE'])
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
@app.route('/api/admin/students', methods=['POST'])
def add_student():
    data = request.get_json()
    sid = data.get('sid')
    sname = data.get('sname')
    email = data.get('email')
    grade = data.get('grade')
    dep = data.get('dep')
    
    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (sid, sname, email, grade, dep)
        VALUES (%s, %s, %s, %s, %s)
    """, (sid, sname, email, grade, dep))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生添加成功"})

# 编辑学生信息接口
@app.route('/api/admin/students/<int:sid>', methods=['PUT'])
def edit_student(sid):
    data = request.get_json()
    sid = data.get('sid')
    sname = data.get('sname')
    email = data.get('email')
    grade = data.get('grade')
    dep = data.get('dep')

    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET sname = %s, email = %s, grade = %s, dep = %s
        WHERE sid = %s
    """, (sname, email, grade, dep, sid))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生信息更新成功"})

# 删除学生信息接口
@app.route('/api/admin/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM students WHERE sid = %s
    """, (sid,))

    conn.commit()
    conn.close()

    return jsonify({"message": "学生删除成功"})

'''
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
'''

# 获取学生信息接口（可以进行分页和搜索）
@app.route('/api/admin/students', methods=['GET'])
def get_students():
    sname = request.args.get('sname', '')  # 用于搜索学生名字

    #conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM student WHERE sname LIKE %s
    """, ('%' + sname + '%',))

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

    #conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM teachers LIMIT %s OFFSET %s
    """, (per_page, offset))

    teachers = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM teachers
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
@app.route('/api/admin/teachers', methods=['POST'])
def add_teacher():
    data = request.get_json()
    tid = data.get('tid')
    tname = data.get('tname')
    email = data.get('email')
    salary = data.get('salary')
    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teachers (tid, tname, email, salary)
        VALUES (%s, %s, %s, %s, )
    """, (tid, tname, email, salary))

    conn.commit()
    conn.close()

    return jsonify({"message": "教师添加成功"})

# 编辑教师信息
@app.route('/api/admin/teachers/<int:tid>', methods=['PUT'])
def edit_teacher(tid):
    data = request.get_json()
    tid = data.get('tid')
    tname = data.get('tname')
    email = data.get('email')
    salary = data.get('salary')

    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teachers
        SET tname = %s, email = %s, salary = %s
        WHERE tid = %s
    """, (tname, email, salary, tid))

    conn.commit()
    conn.close()

    return jsonify({"message": "教师信息更新成功"})

# 删除教师
@app.route('/api/admin/teachers/<int:tid>', methods=['DELETE'])
def delete_teacher(tid):
    #conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM teachers WHERE tid = %s
    """, (tid,))

    conn.commit()
    conn.close()

    return jsonify({"message": "教师删除成功"})

'''
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
'''

## 学生选课部分
# 获取课程列表（分页查询）
@app.route('/api/students/courses', methods=['GET'])
def get_courses():
    page = int(request.args.get('page', 1))  # 页码
    per_page = int(request.args.get('per_page', 10))  # 每页显示多少课程

    offset = (page - 1) * per_page  # 分页偏移量

    #conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM courses LIMIT %s OFFSET %s
    """, (per_page, offset))

    courses = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM courses
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
@app.route('/api/students/select_course', methods=['POST'])
def select_course():
    cursor = conn.cursor(dictionary=True)

    data = request.get_json()
    no = data.get('no')
    sid = data.get('sid')
    tid = data.get('tid')
    cid = data.get('cid')
    #score = data.get('score')


    # 检查学生是否已经选了这门课
    cursor.execute("""
        SELECT * FROM choices WHERE sid = %s AND cid = %s
    """, (sid, cid))

    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "你已经选了这门课"}), 400

    # 选课操作
    cursor.execute("""
        INSERT INTO choices (no, sid, tid, cid)
        VALUES (%s, %s, %s, %s)
    """, (no, sid, tid, cid))

    conn.commit()
    conn.close()

    return jsonify({"message": "选课成功"})

# 学生退课
@app.route('/api/students/drop_course', methods=['POST'])
def drop_course():
    data = request.get_json()
    sid = data.get('sid')
    tid = data.get('tid')
    cid = data.get('cid')

    #conn = get_connection()
    cursor = conn.cursor()

    # 检查学生是否选了这门课
    cursor.execute("""
        SELECT * FROM choices WHERE sid = %s AND cid = %s
    """, (sid, cid))

    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "你没有选这门课"}), 400

    # 退课操作
    cursor.execute("""
        DELETE FROM choices WHERE sid = %s AND cid = %s
    """, (sid, cid))

    conn.commit()
    conn.close()

    return jsonify({"message": "退课成功"})

'''
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
'''

## 老师管理课程
# 获取学生列表（分页查询）
@app.route('/api/teachers/courses/<int:tid>', methods=['GET'])
def get_courses_tid(tid):
    page = int(request.args.get('page', 1))  # 页码
    per_page = int(request.args.get('per_page', 10))  # 每页显示多少课程

    offset = (page - 1) * per_page  # 分页偏移量

    #conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT sid FROM choices WHERE tid = %s LIMIT %s OFFSET %s
    """, (tid, per_page, offset))

    courses = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM choices
    """)
    
    total_courses = cursor.fetchone()['count']
    total_pages = (total_courses // per_page) + (1 if total_courses % per_page else 0)

    conn.close()

    return jsonify({
        'choicess': courses,
        'current_page': page,
        'total_pages': total_pages,
    })


## 登出，只需实现一次即可
@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({"message": "成功退出"})



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)