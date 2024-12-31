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
      teachers: [
        { tid: 1001, tname: '刘丽', email: 'liuli@example.com', salary: 8000 },
        { tid: 1002, tname: '张立法', email: 'zhanglifa@example.com', salary: 9000 },
        { tid: 1003, tname: '软康佳', email: 'ruankangjia@example.com', salary: 7500 },
        { tid: 1024, tname: '林锡鹏', email: 'linxipeng@example.com', salary: 8500 }
      ],
      issearch: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      newTeacher: {
        tid: '',
        tname: '',
        email: '',
        salary: null // 初始化为 null 或 0
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
    showall() {
      this.issearch = false;
    },
    search() {
      this.issearch = true;
    },
    addTeacher() {
      this.showAddModal = true;
    },
    saveTeacher() {
      this.teachers.push({ ...this.newTeacher });
      this.showAddModal = false;
      this.newTeacher = {
        tid: '',
        tname: '',
        email: '',
        salary: null // 重置为 null 或 0
      };
    },
    editTeacher(teacher) {
      // 实现编辑教师信息的逻辑
      alert(`编辑 ${teacher.tname} 的信息`);
    },
    deleteTeacher(teacher) {
      // 实现删除教师信息的逻辑
      const index = this.teachers.indexOf(teacher);
      if (index !== -1) {
        this.teachers.splice(index, 1);
      }
    },
    resetPassword(teacher) {
      // 实现修改教师密码的逻辑
      alert(`重置 ${teacher.tname} 的密码`);
    },
    resetAllPasswords() {
      // 实现重置所有教师密码的逻辑
      alert('重置所有教师的密码');
    },
    logout() {
      // 实现退出系统的逻辑
      alert('退出系统');
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
  }
});