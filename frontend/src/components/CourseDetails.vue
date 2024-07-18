<template>
    <div class="container">
      <div class="sidebar">
        <h1 class="course-title">{{ course.name }}</h1>
        <p class="course-description">{{ course.description }}</p>
  
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else>
          <div v-for="week in course.weeks" :key="week.id" class="week">
            <h2 @click="fetchLectures(week.id)" class="week-title">Week {{ week.number }}</h2>
            <div v-if="selectedWeek === week.id">
              <div v-for="(lecture, index) in week.lectures" :key="lecture.id" class="lecture">
                <h3 class="lecture-title" @click="selectLecture(lecture, week.coding_questions)">
                  {{ week.number }}.{{ index + 1 }} {{ lecture.title }}
                </h3>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        <div v-if="selectedLecture">
          <h2>{{ selectedLecture.title }}</h2>
          <div v-if="isVideoLecture(selectedLecture)">
            <div class="video-container">
              <iframe
                :src="`https://www.youtube.com/embed/${youtubeVideoId}`"
                frameborder="0"
                allowfullscreen
              ></iframe>
            </div>
          </div>
          <div v-else-if="isCodingLecture(selectedLecture)">
            <CodingView :question="selectedCodingQuestion.content" />
          </div>
        </div>
        <div v-else class="placeholder">
          <p>Select a lecture to view its content.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  /* eslint-disable */
  import CodingView from './CodingView.vue';
  
  export default {
    name: 'CourseDetails',
    components: {
      CodingView
    },
    props: ['id'],
    data() {
      return {
        course: {
          weeks: []
        },
        loading: true,
        selectedWeek: null,
        selectedLecture: null,
        selectedCodingQuestion: null,
        youtubeVideoId: null
      };
    },
    mounted() {
      this.fetchCourseDetails();
    },
    methods: {
      async fetchCourseDetails() {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/courses/${this.id}`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          this.course = data;
        } catch (error) {
          console.error('Error fetching course details:', error);
        } finally {
          this.loading = false;
        }
      },
      async fetchLectures(weekId) {
        try {
          this.selectedWeek = weekId;
          const response = await fetch(`http://127.0.0.1:5000/api/weeks/${weekId}`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          this.course.weeks = this.course.weeks.map(week => {
            if (week.id === weekId) {
              return { ...week, lectures: data.lectures, coding_questions: data.coding_questions };
            }
            return week;
          });
        } catch (error) {
          console.error('Error fetching lectures:', error);
        }
      },
      selectLecture(lecture, codingQuestions) {
        this.selectedLecture = lecture;
        if (this.isVideoLecture(lecture)) {
          this.youtubeVideoId = this.extractYouTubeId(lecture.lecture_url);
          this.selectedCodingQuestion = null;
        } else if (this.isCodingLecture(lecture, codingQuestions)) {
          this.selectedCodingQuestion = this.getCodingQuestion(lecture, codingQuestions);
          this.youtubeVideoId = null;
        }
      },
      isVideoLecture(lecture) {
        return lecture.lecture_url && !this.isCodingLecture(lecture);
      },
      isCodingLecture(lecture, codingQuestions) {
        return lecture.title.toLowerCase().includes('graded programming assignment') || 
               (codingQuestions && codingQuestions.some(q => q.week_id === lecture.week_id));
      },
      getCodingQuestion(lecture, codingQuestions) {
        return codingQuestions.find(q => q.week_id === lecture.week_id);
      },
      extractYouTubeId(url) {
        const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
      }
    }
  };
  </script>
  
  <style>
  .container {
    display: flex;
    height: 100vh;
  }
  
  .sidebar {
    width: 300px;
    background: #f8f9fa;
    padding: 20px;
    border-right: 1px solid #ddd;
    overflow-y: auto;
  }
  
  .course-title {
    font-size: 1.5rem;
    margin-bottom: 10px;
  }
  
  .course-description {
    margin-bottom: 20px;
    color: #666;
  }
  
  .week {
    margin-bottom: 10px;
  }
  
  .week-title {
    font-size: 1.25rem;
    cursor: pointer;
    color: #007bff;
    margin-bottom: 5px;
  }
  
  .week-title:hover {
    text-decoration: underline;
  }
  
  .lecture {
    margin-left: 20px;
    cursor: pointer;
  }
  
  .lecture-title {
    font-size: 1rem;
    color: #333;
  }
  
  .lecture-title:hover {
    text-decoration: underline;
  }
  
  .content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
  }
  
  .video-container {
    position: relative;
    padding-bottom: 56.25%; /* 16:9 */
    height: 0;
    overflow: hidden;
    max-width: 100%;
    background: #000;
  }
  
  .video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  
  .question-container {
    background: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .placeholder {
    text-align: center;
    color: #999;
  }
  
  .loading {
    text-align: center;
    color: #999;
  }
  </style>
  