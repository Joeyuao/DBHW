Vue.component('Admin_teacher', {
  template: `
    <div>
      <div>
        <input type="text" placeholder="请输入姓名" v-model="searchName">
        <button @click="search">搜索</button>
        <button @click="showall">显示全部</button><br>
        <button @click="addTeacher">添加教师信息</button>
        <button @click="resetAllPasswords">账号密码重置</button>
        <button @click="logout">退出系统</button>
        <table>
          <thead>
            <tr>
              <th>教师编号</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>薪资</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="teacher in paginatedTeachers" :key="teacher.tid">
              <td>{{ teacher.tid }}</td>
              <td>{{ teacher.tname }}</td>
              <td>{{ teacher.email }}</td>
              <td>{{ teacher.salary }}</td>
              <td>
                <button @click="editTeacher(teacher)">修改</button>
                <button @click="deleteTeacher(teacher)">删除</button>
                <button @click="resetPassword(teacher)">修改密码</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div>
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>{{ currentPage }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
        <!-- 添加教师模态框 -->
        <div v-if="showAddModal" class="modal">
          <div class="modal-content">
            <h3>添加教师信息</h3>
            <input type="text" v-model="newTeacher.tid" placeholder="教师编号">
            <input type="text" v-model="newTeacher.tname" placeholder="姓名">
            <input type="text" v-model="newTeacher.email" placeholder="邮箱">
            <input type="number" v-model="newTeacher.salary" placeholder="薪资">
            <button @click="saveTeacher">保存</button>
            <button @click="showAddModal = false">关闭</button>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      teachers: [],
      issearch: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      newTeacher: {
        tid: '',
        tname: '',
        email: '',
        salary: null
      }
    };
  },
  computed: {
    filteredTeachers() {
      if (this.issearch) {
        return this.teachers.filter(teacher =>
          teacher.tname.includes(this.searchName)
        );
      } else {
        return this.teachers;
      }
    },
    paginatedTeachers() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredTeachers.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredTeachers.length / this.pageSize);
    }
  },
  methods: {
    fetchTeachers() {
      fetch('/api/admin/teachers')
        .then(response => response.json())
        .then(data => {
          this.teachers = data.teachers;
        });
    },
    showall() {
      this.issearch = false;
      this.fetchTeachers();
    },
    search() {
      this.issearch = true;
    },
    addTeacher() {
      this.showAddModal = true;
    },
    saveTeacher() {
      fetch('/api/admin/teachers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.newTeacher)
      })
      .then(response => response.json())
      .then(data => {
        this.showAddModal = false;
        this.newTeacher = { tid: '', tname: '', email: '', salary: null };
        this.fetchTeachers();
      });
    },
    editTeacher(teacher) {
      fetch(`/api/admin/teachers/${teacher.tid}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(teacher)
      })
      .then(response => response.json())
      .then(data => {
        this.fetchTeachers();
      });
    },
    deleteTeacher(teacher) {
      fetch(`/api/admin/teachers/${teacher.tid}`, {
        method: 'DELETE'
      })
      .then(response => response.json())
      .then(data => {
        this.fetchTeachers();
      });
    },
    resetPassword(teacher) {
      fetch(`/api/admin/teacher/reset_password/${teacher.tid}`, {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        alert(`教师 ${teacher.tname} 的密码已重置`);
      });
    },
    resetAllPasswords() {
      fetch('/api/admin/reset_all_teacher_passwords', {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        alert('所有教师的密码已重置');
      });
    },
    logout() {
      fetch('/api/logout', {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        alert('成功退出');
        window.location.href = '/';
      });
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
    }
  },
  mounted() {
    this.fetchTeachers();
  }
});