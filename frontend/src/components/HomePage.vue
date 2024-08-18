<template>
  <div class="dashboard">
    <h1 class="dashboard-title">My Dashboard</h1>
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading your courses...</p>
    </div>
    <div v-else>
      <div class="courses-grid">
        <router-link v-for="course in filteredCourses" :key="course.id" :to="`/courses/${course.id}`" class="course-card">
          <div class="course-link">
            <div class="course-icon" :style="{ backgroundColor: getRandomColor() }">
              {{ course.name.charAt(0) }}
            </div>
            <div class="course-info">
              <h2 class="course-title">{{ course.name }}</h2>
              <p class="course-description">{{ truncateDescription(course.description) }}</p>
            </div>
            <div class="course-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'CourseDashboard',
  data() {
    return {
      courses: [],
      loading: true,
      searchQuery: '',
    };
  },
  computed: {
    filteredCourses() {
      return this.courses.filter(course => 
        course.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        course.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  mounted() {
    this.fetchCourses();
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await fetch('http://localhost:5000/api/courses');
        const data = await response.json();
        this.courses = data;
      } catch (error) {
        console.error('Error fetching courses:', error);
      } finally {
        this.loading = false;
      }
    },
    getRandomColor() {
      const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    truncateDescription(description) {
      return description.length > 100 ? description.slice(0, 97) + '...' : description;
    }
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

body {
  font-family: 'Poppins', sans-serif;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(to right, #ffecd2, #fcb69f);
}

.dashboard-title {
  font-size: 3.5rem;
  margin-bottom: 30px;
  text-align: center;
  color: #333;
  font-weight: 300;
}

.loading {
  text-align: center;
  padding: 40px 0;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.search-bar {
  margin-bottom: 30px;
}

.search-bar input {
  width: 100%;
  padding: 12px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.search-bar input:focus {
  outline: none;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.15);
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

.course-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 320px;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  align-items: center;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.course-link {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  text-decoration: none;
  color: inherit;
  padding: 20px;
}

.course-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
}

.course-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 20px;
}

.course-title {
  font-size: 1.25rem;
  margin-bottom: 10px;
  color: #333;
}

.course-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.course-arrow {
  color: #999;
  font-size: 1.2rem;
  transition: transform 0.3s ease, opacity 0.3s ease;
  margin-top: 15px;
  opacity: 0;
  transform: translateX(0);
}

.course-icon:hover {
  transform: scale(1.1);
}

.course-link:hover .course-arrow {
  transform: translateX(10px);
  opacity: 1;
}

@media (max-width: 768px) {
  .courses-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (max-width: 480px) {
  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
