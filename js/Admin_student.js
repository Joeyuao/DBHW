Vue.component('Admin_student', {
  template: `
    <div>
      <div>
        <input type="text" placeholder="请输入姓名" v-model="searchName">
        <button @click="search">搜索</button>
        <button @click="showall">显示全部</button><br>
        <button @click="addStudent">添加学生信息</button>
        <button @click="resetAllPasswords">账号密码重置</button>
        <button @click="logout">退出系统</button>
        <table>
          <thead>
            <tr>
              <th>学号</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>年级</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in paginatedStudents" :key="student.sid">
              <td>{{ student.sid }}</td>
              <td>{{ student.sname }}</td>
              <td>{{ student.email }}</td>
              <td>{{ student.grade }}</td>
              <td>
                <button @click="editStudent(student)">修改</button>
                <button @click="deleteStudent(student)">删除</button>
                <button @click="resetPassword(student)">修改密码</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div>
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>{{ currentPage }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
        <!-- 添加学生模态框 -->
        <div v-if="showAddModal" class="modal">
          <div class="modal-content">
            <h3>添加学生信息</h3>
            <input type="text" v-model="newStudent.sid" placeholder="学号">
            <input type="text" v-model="newStudent.sname" placeholder="姓名">
            <input type="text" v-model="newStudent.email" placeholder="邮箱">
            <input type="number" v-model="newStudent.grade" placeholder="年级">
            <input type="text" v-model="newStudent.dep" placeholder="学院">
            <button @click="saveStudent">保存</button>
            <button @click="showAddModal = false">关闭</button>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      students: [], // 从后端获取的学生数据
      issearch: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      newStudent: {
        sid: '',
        sname: '',
        email: '',
        grade: null,
        dep: ''
      }
    };
  },
  computed: {
    filteredStudents() {
      if (this.issearch) {
        return this.students.filter(student =>
          student.sname.includes(this.searchName)
        );
      } else {
        return this.students;
      }
    },
    paginatedStudents() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredStudents.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredStudents.length / this.pageSize);
    }
  },
  methods: {
    showall() {
      this.issearch = false;
    },
    search() {
      this.issearch = true;
    },
    addStudent() {
      this.showAddModal = true;
    },
    saveStudent() {
      // 调用后端 API 添加学生
      fetch('/api/admin/students', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.newStudent),
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert(data.message);
            this.fetchStudents(); // 重新获取学生列表
            this.showAddModal = false;
            this.newStudent = {
              sid: '',
              sname: '',
              email: '',
              grade: null,
              dep: ''
            };
          }
        })
        .catch(error => console.error('Error:', error));
    },
    editStudent(student) {
      // 调用后端 API 编辑学生信息
      const updatedStudent = {
        sid: student.sid,
        sname: prompt('请输入新的姓名', student.sname),
        email: prompt('请输入新的邮箱', student.email),
        grade: prompt('请输入新的年级', student.grade),
        dep: prompt('请输入新的学院', student.dep)
      };

      if (updatedStudent.sname && updatedStudent.email && updatedStudent.grade && updatedStudent.dep) {
        fetch(`/api/admin/students/${student.sid}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updatedStudent),
        })
          .then(response => response.json())
          .then(data => {
            if (data.message) {
              alert(data.message);
              this.fetchStudents(); // 重新获取学生列表
            }
          })
          .catch(error => console.error('Error:', error));
      }
    },
    deleteStudent(student) {
      // 调用后端 API 删除学生
      if (confirm(`确定要删除学生 ${student.sname} 吗？`)) {
        fetch(`/api/admin/students/${student.sid}`, {
          method: 'DELETE',
        })
          .then(response => response.json())
          .then(data => {
            if (data.message) {
              alert(data.message);
              this.fetchStudents(); // 重新获取学生列表
            }
          })
          .catch(error => console.error('Error:', error));
      }
    },
    resetPassword(student) {
      // 实现修改学生密码的逻辑
      alert(`重置 ${student.sname} 的密码`);
    },
    resetAllPasswords() {
      // 实现重置所有学生密码的逻辑
      alert('重置所有学生的密码');
    },
    logout() {
      // 实现退出系统的逻辑
      fetch('/api/logout', {
        method: 'POST',
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert(data.message);
            window.location.href = '/'; // 跳转到登录页面
          }
        })
        .catch(error => console.error('Error:', error));
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
    fetchStudents() {
      // 从后端获取学生列表
      fetch('/api/admin/students')
        .then(response => response.json())
        .then(data => {
          this.students = data;
        })
        .catch(error => console.error('Error:', error));
    }
  },
  mounted() {
    // 组件加载时获取学生列表
    this.fetchStudents();
  }
});