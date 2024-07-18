<template>
  <div class="container">
    <h1 class="title">Courses</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="courses-grid">
      <div v-for="course in courses" :key="course.id" class="course">
        <router-link :to="`/courses/${course.id}`" class="course-link">
          <h2 class="course-title">{{ course.name }}</h2>
          <p class="course-description">{{ course.description }}</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      courses: [],
      loading: true,
    };
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
  },
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  font-size: 2.5rem;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.loading {
  text-align: center;
  font-size: 1.5rem;
  color: #777;
}

.courses-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.course {
  flex: 1 1 calc(33.333% - 20px);
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.course:hover {
  transform: translateY(-10px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.course-link {
  display: block;
  padding: 20px;
  text-decoration: none;
  color: inherit;
}

.course-title {
  font-size: 1.25rem;
  margin-bottom: 10px;
  color: #333;
}

.course-description {
  font-size: 1rem;
  color: #666;
}

@media (max-width: 768px) {
  .course {
    flex: 1 1 calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .course {
    flex: 1 1 100%;
  }
}
</style>
