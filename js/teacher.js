Vue.component('teacher', {
  template: `
    <div>
      <div>
        <input type="text" placeholder="请输入课程名称" v-model="searchName">
        <button @click="search">搜索</button>
        <button @click="showall">显示全部</button><br>
        <button @click="addCourse">添加我的课程</button>
        <button @click="logout">退出系统</button><br>
        <input type="checkbox" v-model="showMyCourse"> 显示我的课程
        <table>
          <thead>
            <tr>
              <th>编号</th>
              <th>学生ID</th>
              <th>教师ID</th>
              <th>课程ID</th>
              <th>分数</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in paginatedCourses" :key="course.no">
              <td>{{ course.no }}</td>
              <td>{{ course.sid }}</td>
              <td>{{ course.tid }}</td>
              <td>{{ course.cid }}</td>
              <td>{{ course.score }}</td>
              <td v-if="isMyCourse(course)">
                <button @click="editCourse(course)">修改</button>
                <button @click="deleteCourse(course)">删除</button>
              </td>
              <td v-else>
                <button style="color:white;background-color:gray;" @click="cannotEdit">修改</button>
                <button style="color:white;background-color:gray;" @click="cannotEdit">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div>
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>{{ currentPage }}/{{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
        <!-- 添加课程模态框 -->
        <div v-if="showAddModal" class="modal">
          <div class="modal-content">
            <h3>添加我的课程</h3>
            <input type="text" v-model="newCourse.id" placeholder="课程编号">
            <input type="text" v-model="newCourse.name" placeholder="课程名称">
            <input type="text" v-model="newCourse.credits" placeholder="学分">
            <input type="text" v-model="newCourse.semester" placeholder="开课学期">
            <input type="text" v-model="newCourse.type" placeholder="课程类型">
            <button @click="saveCourse">保存</button>
            <button @click="showAddModal = false">关闭</button>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      courses: [],
      issearch: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      showAddModal: false,
      showMyCourse: false, // 初始化为 false，显示全部课程
      newCourse: {
        id: '',
        name: '',
        teacher: '当前老师', // 替换为实际的老师名称
        credits: '',
        semester: '',
        type: ''
      }
    };
  },
  computed: {
    myCourses() {
      return this.courses.filter(course => course.teacher === '当前老师'); // 替换为实际的老师名称
    },
    filteredCourses() {
      if (this.issearch) {
        return this.currentCourses.filter(course =>
          course.name.includes(this.searchName)
        );
      } else {
        return this.currentCourses;
      }
    },
    currentCourses() {
      return this.showMyCourse ? this.myCourses : this.courses;
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
    fetchCourses() {
      const tid = 1; // 假设当前教师的ID是1
      fetch(`/api/teachers/courses/${tid}`)
        .then(response => response.json())
        .then(data => {
          this.courses = data.choicess;
          this.totalPages = data.total_pages;
        })
        .catch(error => {
          console.error('Error fetching courses:', error);
        });
    },
    search() {
      this.issearch = true;
    },
    showall() {
      this.issearch = false;
      this.showMyCourse = false; // 显示全部课程
    },
    addCourse() {
      this.showAddModal = true;
    },
    saveCourse() {
      fetch('/api/admin/courses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cid: this.newCourse.id,
          cname: this.newCourse.name,
          chour: this.newCourse.credits, // 假设学分对应学时
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert('课程添加成功');
            this.courses.push({ ...this.newCourse });
            this.showAddModal = false;
            this.newCourse = {
              id: '',
              name: '',
              teacher: '当前老师', // 替换为实际的老师名称
              credits: '',
              semester: '',
              type: ''
            };
          }
        })
        .catch(error => {
          console.error('Error adding course:', error);
        });
    },
    editCourse(course) {
      fetch(`/api/admin/courses/${course.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cname: course.name,
          chour: course.credits, // 假设学分对应学时
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert('课程信息更新成功');
          }
        })
        .catch(error => {
          console.error('Error updating course:', error);
        });
    },
    deleteCourse(course) {
      if (course.teacher === '当前老师') { // 替换为实际的老师名称
        fetch(`/api/admin/courses/${course.id}`, {
          method: 'DELETE',
        })
          .then(response => response.json())
          .then(data => {
            if (data.message) {
              alert('课程删除成功');
              const index = this.courses.indexOf(course);
              if (index !== -1) {
                this.courses.splice(index, 1);
              }
            }
          })
          .catch(error => {
            console.error('Error deleting course:', error);
          });
      } else {
        alert("不能删除别人的课程");
      }
    },
    logout() {
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
    },
    isMyCourse(course) {
      return course.teacher === '当前老师'; // 替换为实际的老师名称
    },
    cannotEdit() {
      alert("不能修改或删除别人的课程");
    }
  },
  mounted() {
    this.fetchCourses();
  }
});