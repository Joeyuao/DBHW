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
              <th>性别</th>
              <th>出生年份</th>
              <th>专业</th>
              <th>入学年份</th>
              <th>学院</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in paginatedStudents" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.name }}</td>
              <td>{{ student.gender }}</td>
              <td>{{ student.birthYear }}</td>
              <td>{{ student.major }}</td>
              <td>{{ student.enrollmentYear }}</td>
              <td>{{ student.department }}</td>
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
            <input type="text" v-model="newStudent.id" placeholder="学号">
            <input type="text" v-model="newStudent.name" placeholder="姓名">
            <input type="text" v-model="newStudent.gender" placeholder="性别">
            <input type="text" v-model="newStudent.birthYear" placeholder="出生年份">
            <input type="text" v-model="newStudent.major" placeholder="专业">
            <input type="text" v-model="newStudent.enrollmentYear" placeholder="入学年份">
            <input type="text" v-model="newStudent.department" placeholder="学院">
            <button @click="saveStudent">保存</button>
            <button @click="showAddModal = false">关闭</button>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      students: [
        { id: 2001, name: '张三', gender: '男', birthYear: '2000-05-12', major: '计算机科学', enrollmentYear: '2018-09-01', department: '计算机系' },
        { id: 2002, name: '李四', gender: '女', birthYear: '2000-08-25', major: '软件工程', enrollmentYear: '2018-09-01', department: '计算机系' },
        { id: 2003, name: '王五', gender: '男', birthYear: '1999-12-10', major: '电子工程', enrollmentYear: '2017-09-01', department: '电子工程系' },
        { id: 2004, name: '赵六', gender: '女', birthYear: '2001-03-03', major: '机械设计', enrollmentYear: '2019-09-01', department: '机械工程系' }
      ],
      issearch: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      newStudent: {
        id: '',
        name: '',
        gender: '',
        birthYear: '',
        major: '',
        enrollmentYear: '',
        department: ''
      }
    };
  },
  computed: {
    filteredStudents() {
      if (this.issearch) {
        return this.students.filter(student =>
          student.name.includes(this.searchName)
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
      this.students.push({ ...this.newStudent });
      this.showAddModal = false;
      this.newStudent = {
        id: '',
        name: '',
        gender: '',
        birthYear: '',
        major: '',
        enrollmentYear: '',
        department: ''
      };
    },
    editStudent(student) {
      // 实现编辑学生信息的逻辑
      alert(`编辑 ${student.name} 的信息`);
    },
    deleteStudent(student) {
      // 实现删除学生信息的逻辑
      const index = this.students.indexOf(student);
      if (index !== -1) {
        this.students.splice(index, 1);
      }
    },
    resetPassword(student) {
      // 实现修改学生密码的逻辑
      alert(`重置 ${student.name} 的密码`);
    },
    resetAllPasswords() {
      // 实现重置所有学生密码的逻辑
      alert('重置所有学生的密码');
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