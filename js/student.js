Vue.component('student', {
  template: `
    <div>
      <div>
        <input type="text" placeholder="请输入课程名称" v-model="searchName">
        <button @click="search">搜索</button>
        <button @click="showall">显示全部</button>
        <button @click="resetAllPasswords">账号密码重置</button>
        <button @click="logout">退出系统</button><br>
        <input type="checkbox" v-model="isSearchSelected"> 显示已选课程
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
              <td>
                <button v-if="!selectedCourses.includes(course.cid)" @click="selectCourse(course)">选课</button>
                <button v-else @click="dropCourse(course)">退课</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div>
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>{{ currentPage }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      courses: [],
      issearch: false,
      isSearchSelected: false,
      searchName: '',
      currentPage: 1,
      pageSize: 5,
      selectedCourses: [],
      studentId: 1 // 假设当前学生的ID是1
    };
  },
  computed: {
    selectedCoursesList() {
      return this.selectedCourses.map(courseId => {
        return this.courses.find(course => course.cid === courseId);
      }).filter(course => course !== undefined);
    },
    filteredCourses() {
      let final_courses = this.courses;
      if (this.isSearchSelected) {
        final_courses = this.selectedCoursesList;
      }
      if (this.issearch) {
        return final_courses.filter(course =>
          course.cid.toString().includes(this.searchName)
        );
      } else {
        return final_courses;
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
    fetchCourses() {
      fetch(`/api/students/courses?page=${this.currentPage}&per_page=${this.pageSize}`)
        .then(response => response.json())
        .then(data => {
          this.courses = data.courses;
          this.totalPages = data.total_pages;
        })
        .catch(error => {
          console.error('Error fetching courses:', error);
        });
    },
    showall() {
      this.issearch = false;
      this.fetchCourses();
    },
    search() {
      this.issearch = true;
      this.fetchCourses();
    },
    selectCourse(course) {
      fetch('/api/students/select_course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sid: this.studentId,
          cid: course.cid,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            alert(data.error);
          } else {
            alert('选课成功');
            this.selectedCourses.push(course.cid);
          }
        })
        .catch(error => {
          console.error('Error selecting course:', error);
        });
    },
    dropCourse(course) {
      fetch('/api/students/drop_course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sid: this.studentId,
          cid: course.cid,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            alert(data.error);
          } else {
            alert('退课成功');
            this.selectedCourses.splice(this.selectedCourses.indexOf(course.cid), 1);
          }
        })
        .catch(error => {
          console.error('Error dropping course:', error);
        });
    },
    resetAllPasswords() {
      alert('重置所有课程的密码');
    },
    logout() {
      alert('退出系统');
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchCourses();
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchCourses();
      }
    }
  },
  mounted() {
    this.fetchCourses();
  }
});