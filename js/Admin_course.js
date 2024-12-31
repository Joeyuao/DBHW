Vue.component('Admin_course', {
  template: `
    <div>
      <div>
        <input type="text" placeholder="请输入课程名称" v-model="searchName">
        <button @click="search">搜索</button>
        <button @click="showall">显示全部</button><br>
        <button @click="addCourse">添加课程信息</button>
        <button @click="resetAllPasswords">账号密码重置</button>
        <button @click="logout">退出系统</button>
        <table>
          <thead>
            <tr>
              <th>课程编号</th>
              <th>课程名称</th>
              <th>课时</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in paginatedCourses" :key="course.cid">
              <td>{{ course.cid }}</td>
              <td>{{ course.cname }}</td>
              <td>{{ course.chour }}</td>
              <td>
                <button @click="editCourse(course)">修改</button>
                <button @click="deleteCourse(course)">删除</button>
                <button @click="resetPassword(course)">修改密码</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div>
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>{{ currentPage }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
        <!-- 添加课程模态框 -->
        <div v-if="showAddModal" class="modal">
          <div class="modal-content">
            <h3>添加课程信息</h3>
            <input type="text" v-model="newCourse.cid" placeholder="课程编号">
            <input type="text" v-model="newCourse.cname" placeholder="课程名称">
            <input type="number" v-model="newCourse.chour" placeholder="课时">
            <button @click="saveCourse">保存</button>
            <button @click="showAddModal = false">关闭</button>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      courses: [], // 从后端获取的课程数据
      issearch: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      newCourse: {
        cid: '',
        cname: '',
        chour: null
      }
    };
  },
  computed: {
    filteredCourses() {
      if (this.issearch) {
        return this.courses.filter(course =>
          course.cname.includes(this.searchName)
        );
      } else {
        return this.courses;
      }
    },
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredCourses.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredCourses.length / this.pageSize);
    }
  },
  methods: {
    showall() {
      this.issearch = false;
    },
    search() {
      this.issearch = true;
    },
    addCourse() {
      this.showAddModal = true;
    },
    saveCourse() {
      // 调用后端 API 添加课程
      fetch('/api/admin/courses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.newCourse),
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert(data.message);
            this.fetchCourses(); // 重新获取课程列表
            this.showAddModal = false;
            this.newCourse = {
              cid: '',
              cname: '',
              chour: null
            };
          }
        })
        .catch(error => console.error('Error:', error));
    },
    editCourse(course) {
      // 调用后端 API 编辑课程
      const updatedCourse = {
        cid: course.cid,
        cname: prompt('请输入新的课程名称', course.cname),
        chour: prompt('请输入新的课时', course.chour)
      };

      if (updatedCourse.cname && updatedCourse.chour) {
        fetch(`/api/admin/courses/${course.cid}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updatedCourse),
        })
          .then(response => response.json())
          .then(data => {
            if (data.message) {
              alert(data.message);
              this.fetchCourses(); // 重新获取课程列表
            }
          })
          .catch(error => console.error('Error:', error));
      }
    },
    deleteCourse(course) {
      // 调用后端 API 删除课程
      if (confirm(`确定要删除课程 ${course.cname} 吗？`)) {
        fetch(`/api/admin/courses/${course.cid}`, {
          method: 'DELETE',
        })
          .then(response => response.json())
          .then(data => {
            if (data.message) {
              alert(data.message);
              this.fetchCourses(); // 重新获取课程列表
            }
          })
          .catch(error => console.error('Error:', error));
      }
    },
    resetPassword(course) {
      // 实现修改课程密码的逻辑
      alert(`重置 ${course.cname} 的密码`);
    },
    resetAllPasswords() {
      // 实现重置所有课程密码的逻辑
      alert('重置所有课程的密码');
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
    fetchCourses() {
      // 从后端获取课程列表
      fetch('/api/admin/courses')
        .then(response => response.json())
        .then(data => {
          this.courses = data;
        })
        .catch(error => console.error('Error:', error));
    }
  },
  mounted() {
    // 组件加载时获取课程列表
    this.fetchCourses();
  }
});