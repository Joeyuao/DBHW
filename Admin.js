Vue.component('Admin', {
  template: `
    <div>
      <h1>课程管理</h1>
      <h1>学生管理</h1>
      <h2>教师名单管理</h2>
      <input type="text" placeholder="请输入姓名" v-model="searchName">
      <button @click="search">搜索</button>
      <button @click="addTeacher">添加教师信息</button>
      <button @click="resetAllPasswords">账号密码重置</button>
      <button @click="logout">退出系统</button>
      <table>
        <thead>
          <tr>
            <th>教师编号</th>
            <th>姓名</th>
            <th>性别</th>
            <th>出生年份</th>
            <th>学历</th>
            <th>职称</th>
            <th>入职年份</th>
            <th>学院</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="teacher in paginatedTeachers" :key="teacher.id">
            <td>{{ teacher.id }}</td>
            <td>{{ teacher.name }}</td>
            <td>{{ teacher.gender }}</td>
            <td>{{ teacher.birthYear }}</td>
            <td>{{ teacher.education }}</td>
            <td>{{ teacher.title }}</td>
            <td>{{ teacher.hireYear }}</td>
            <td>{{ teacher.department }}</td>
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
          <input type="text" v-model="newTeacher.id" placeholder="教师编号">
          <input type="text" v-model="newTeacher.name" placeholder="姓名">
          <input type="text" v-model="newTeacher.gender" placeholder="性别">
          <input type="text" v-model="newTeacher.birthYear" placeholder="出生年份">
          <input type="text" v-model="newTeacher.education" placeholder="学历">
          <input type="text" v-model="newTeacher.title" placeholder="职称">
          <input type="text" v-model="newTeacher.hireYear" placeholder="入职年份">
          <input type="text" v-model="newTeacher.department" placeholder="学院">
          <button @click="saveTeacher">保存</button>
          <button @click="showAddModal = false">关闭</button>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      teachers: [
        { id: 1001, name: '刘丽', gender: '女', birthYear: '1990-03-08', education: '硕士', title: '副教授', hireYear: '2015-09-02', department: '设计系' },
        { id: 1002, name: '张立法', gender: '男', birthYear: '1984-07-02', education: '博士', title: '讲师', hireYear: '2015-09-02', department: '计算机系' },
        { id: 1003, name: '软康佳', gender: '男', birthYear: '1988-06-18', education: '硕士', title: '助教', hireYear: '2017-07-07', department: '计算机系' },
        { id: 1004, name: '林锡鹏', gender: '男', birthYear: '1996-09-02', education: '硕士', title: '普通教师', hireYear: '2015-09-02', department: '计算机系' }
      ],
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      newTeacher: {
        id: '',
        name: '',
        gender: '',
        birthYear: '',
        education: '',
        title: '',
        hireYear: '',
        department: ''
      }
    };
  },
  computed: {
    filteredTeachers() {
      return this.teachers.filter(teacher =>
        teacher.name.includes(this.searchName)
      );
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
    search() {
      // 搜索逻辑已经在计算属性中实现
    },
    addTeacher() {
      this.showAddModal = true;
    },
    saveTeacher() {
      this.teachers.push({ ...this.newTeacher });
      this.showAddModal = false;
      this.newTeacher = {
        id: '',
        name: '',
        gender: '',
        birthYear: '',
        education: '',
        title: '',
        hireYear: '',
        department: ''
      };
    },
    editTeacher(teacher) {
      // 实现编辑教师信息的逻辑
      alert(`编辑 ${teacher.name} 的信息`);
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
      alert(`重置 ${teacher.name} 的密码`);
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