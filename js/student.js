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
                <th>课程编号</th>
                <th>课程名称</th>
                <th>授课教师</th>
                <th>学分</th>
                <th>开课学期</th>
                <th>课程类型</th>
                <th>已选/上限人数</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in paginatedCourses" :key="course.id">
                <td>{{ course.id }}</td>
                <td>{{ course.name }}</td>
                <td>{{ course.teacher }}</td>
                <td>{{ course.credits }}</td>
                <td>{{ course.semester }}</td>
                <td>{{ course.type }}</td>
                <td>{{ course.nownumber }}/{{ course.limit }}</td>
                <td>
                  <button v-if="!selectedCourses.includes(course.id)" @click="selectCourse(course)">选课</button>
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
        courses: [
          { id: 3001, name: '数据结构', teacher: '张老师', credits: 3, semester: '2023秋季', nownumber: 99, limit: 100, type: '必修' },
          { id: 3002, name: '操作系统', teacher: '李老师', credits: 4, semester: '2023秋季', nownumber: 99, limit: 100, type: '必修' },
          { id: 3003, name: '计算机网络', teacher: '王老师', credits: 3, semester: '2023春季', nownumber: 99, limit: 100, type: '选修' },
          { id: 3004, name: '数据库原理', teacher: '赵老师', credits: 3, semester: '2023春季', nownumber: 99, limit: 100, type: '必修' }
        ],
        issearch: false,
        isSearchSelected: false,
        searchName: '',
        currentPage: 1,
        pageSize: 5,
        selectedCourses: [],
        newCourse: {
          id: '',
          name: '',
          teacher: '',
          credits: '',
          semester: '',
          nownumber: 0,
          limit: 100,
          type: ''
        }
      };
    },
    computed: {
      selectedCoursesList() {
        return this.selectedCourses.map(courseId => {
          return this.courses.find(course => course.id === courseId);
        }).filter(course => course !== undefined);
      },
      filteredCourses() {
        let final_courses = this.courses;
        if (this.isSearchSelected) {
          final_courses = this.selectedCoursesList;
        }
        if (this.issearch) {
          return final_courses.filter(course =>
            course.name.includes(this.searchName)
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
      showall() {
        this.issearch = false;
      },
      search() {
        this.issearch = true;
      },
      selectCourse(course) {
        if (course.nownumber >= course.limit) {
          alert('课程人数已满，无法选课');
        } else {
          alert('选课成功');
          course.nownumber++;
          if (!this.selectedCourses.includes(course.id)) {
            this.selectedCourses.push(course.id);
          }
        }
      },
      dropCourse(course) {
        if (this.selectedCourses.includes(course.id)) {
          alert('退课成功');
          this.selectedCourses.splice(this.selectedCourses.indexOf(course.id), 1);
          course.nownumber--;
        } else {
          alert('你没有选这门课');
        }
      },
      resetAllPasswords() {
        alert('重置所有课程的密码');
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
      }
    }
  });