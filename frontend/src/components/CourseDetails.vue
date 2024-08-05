<template>
  <div class="course-container">
    <aside class="sidebar">
      <h1 class="course-title">{{ course.name }}</h1>
      <p class="course-description">{{ course.description }}</p>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading course content...</p>
      </div>
      <nav v-else class="course-nav">
        <div v-for="week in course.weeks" :key="week.id" class="week-item">
          <h2 @click="fetchLectures(week.id)" class="week-title" :class="{ active: selectedWeek === week.id }">
            Week {{ week.number }}
          </h2>
          <transition name="fade">
            <ul v-if="selectedWeek === week.id" class="lecture-list">
              <li v-for="(lecture, index) in week.lectures" :key="lecture.id" class="lecture-item">
                <button @click="selectLecture(lecture, week.coding_questions)" class="lecture-button" :class="{ active: selectedLecture === lecture }">
                  {{ week.number }}.{{ index + 1 }} {{ lecture.title }}
                </button>
              </li>
            </ul>
          </transition>
        </div>
      </nav>
    </aside>
    <main class="content">
      <div v-if="selectedLecture" class="lecture-content">
        <h2 class="lecture-title">{{ selectedLecture.title }}</h2>
        <div class="lecture-main">
          <div v-if="isVideoLecture(selectedLecture)" class="video-container">
            <iframe
              :src="`https://www.youtube.com/embed/${youtubeVideoId}`"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>
          <div v-else-if="isCodingLecture(selectedLecture)" class="coding-container">
            <CodingView :question="selectedCodingQuestion.content" />
          </div>
          <button @click="fetchLectureSummary" :class="isCodingLecture(selectedLecture) ? 'compare-button' : 'summary-button'">
            {{ isCodingLecture(selectedLecture) ? 'Compare AI' : 'Summary AI' }}
          </button>
          <div class="summary-container">
            <h3>{{ isCodingLecture(selectedLecture) ? 'AI Comparison' : 'AI Summary' }}</h3>
            <p>{{ lectureSummary }}</p>
          </div>
        </div>
      </div>
      <div v-else class="placeholder">
        <div class="course-info">
          <h2>Course Instructors:</h2>
          <p>Dr. Meenakshi D'Souza</p>
          <p>Department of Computer Science and Engineering, IIIT Bangalore</p>

          <h2>Course Support Team:</h2>
          <p>Dr. Arup Kumar Chattopadhyay (PhD)</p>
          <p>Course TA</p>
          <p>Afnan Ahmad</p>

          <h2>Study Material:</h2>
          <p>
            The learners are advised to make best use of the interaction sessions with the course support members to clarify their doubts.
          </p>
          <p>
            The primary study material for this course is the set of videos and assignments posted on the course page. The prescribed textbook for this course is:
          </p>
          <ul>
            <li>Paul Ammann and Jeff Offutt, Introduction to Software Testing, Cambridge University Press, 2008.</li>
            <li>Glenford J. Myers, The Art of Software Testing, Second edition, 2008.</li>
            <li>Paul C. Jorgensen, Software Testing: A Craftsman’s Approach, Fourth edition, CRC Press, 2014.</li>
            <li>Lisa Crispin and Janet Gregory, Agile Testing: A Practical Guide for Testers and Agile Teams, Addison-Wesley, 2009.</li>
            <li>Appropriate research papers on testing techniques, information regarding testing tools, as applicable.</li>
          </ul>
          <p>
            To know more about course syllabus, Instructors, and course contents, please click on the below link:
          </p>
          <a href="https://onlinedegree.iitm.ac.in/course_pages/BSCCS3002.html" target="_blank">Course Page</a>
          <p>
            Please click on the below tab to view the Course Specific Calendar:
          </p>
          <a href="https://calendar.google.com/calendar/u/0?cid=Y192ZzQ1Zjl0NHM1Z3VrZ2N0ZmwwZDl0Z2Q2c0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t" target="_blank">Course Calendar</a>
        </div>
      </div>
    </main>
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
      youtubeVideoId: null,
      lectureSummary: ''
    };
  },
  mounted() {
    this.fetchCourseDetails();
  },
  methods: {
    async fetchLectureSummary() {
      if (!this.youtubeVideoId) {
        console.error('No video lecture selected');
        return;
      }
      const videoUrl = `https://www.youtube.com/watch?v=${this.youtubeVideoId}`;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/lecture-summary', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ videoUrl })
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.lectureSummary = data.summary;
      } catch (error) {
        console.error('Error fetching lecture summary:', error);
      }
    },
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

<style scoped>
.course-container {
  display: flex;
  height: 100vh;
  font-family: 'Roboto', Arial, sans-serif;
  color: #333;
  background-color: #f8f9fa;
}

.sidebar {
  width: 320px;
  background: #ffffff;
  padding: 24px;
  border-right: 1px solid #e9ecef;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
}

.course-title {
  font-size: 1.8rem;
  margin-bottom: 12px;
  color: #212529;
  font-weight: 700;
}

.course-description {
  margin-bottom: 24px;
  color: #6c757d;
  font-size: 0.95rem;
  line-height: 1.5;
}

.loading {
  text-align: center;
  color: #6c757d;
}

.spinner {
  border: 3px solid #e9ecef;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.course-nav {
  margin-top: 24px;
}

.week-item {
  margin-bottom: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.week-title {
  font-size: 1.1rem;
  cursor: pointer;
  color: #495057;
  margin-bottom: 0;
  padding: 12px 16px;
  background-color: #e9ecef;
  transition: all 0.3s ease;
}

.week-title:hover, .week-title.active {
  color: #007bff;
  background-color: #dee2e6;
}

.lecture-list {
  list-style-type: none;
  padding: 8px 0;
  margin: 0;
}

.lecture-item {
  margin-bottom: 4px;
}

.lecture-button {
  background: none;
  border: none;
  color: #495057;
  cursor: pointer;
  font-size: 0.95rem;
  text-align: left;
  width: 100%;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

.lecture-button:hover, .lecture-button.active {
  background-color: #e9ecef;
  color: #007bff;
}

.content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

.lecture-content {
  background: #f8f9fa;
  padding: 24px;
  width: 100%;
}

.lecture-title {
  font-size: 1.6rem;
  margin-bottom: 24px;
  color: #212529;
  font-weight: 700;
}

.lecture-main {
  display: flex;
  justify-content: space-between;
}

.video-container {
  position: relative;
  width: 65%;
  background: #000;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.video-container::before {
  content: '';
  display: block;
  padding-top: 56.25%; /* 16:9 aspect ratio */
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.coding-container {
  position: relative;
  width: 65%;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 100%; /* Ensure it doesn't exceed container's width */
  margin: 0 auto;
}

.coding-container .editor {
  width: 100%;
  height: 300px; /* Adjust the height as needed */
  border: 1px solid #ccc;
}

.summary-container {
  width: 30%;
  margin-left: 2%;
  padding: 16px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  position: relative;
}

.summary-container .summary-button,
.summary-container .compare-button {
  position: absolute;
  top: 16px;
  right: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.summary-container .summary-button:hover,
.summary-container .compare-button:hover {
  background-color: #0056b3;
}

.summary-container h3 {
  font-size: 1.4rem;
  margin-bottom: 12px;
  color: #212529;
  font-weight: 600;
}

.summary-container p {
  color: #495057;
  font-size: 1rem;
  line-height: 1.5;
}

.placeholder {
  display: flex;
  color: #6c757d;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.placeholder img {
  margin-bottom: 24px;
  opacity: 0.6;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 768px) {
  .content {
    padding: 24px;
  }
  
  .lecture-content {
    max-width: 90%;
  }

  .lecture-main {
    flex-direction: column;
  }

  .video-container,
  .coding-container {
    width: 100%;
    margin-bottom: 16px;
  }

  .summary-container {
    width: 100%;
  }
}


</style>