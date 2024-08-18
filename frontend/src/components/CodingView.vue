<template>
  <div>
    <div v-if="codingQuestion">
      <h2>Coding Question</h2>
      <p>{{ codingQuestion.content }}</p>
      <div id="editor" class="editor"></div>
      <div class="button-container">
        <button @click="runCode" class="btn btn-primary">Run Code</button>
        <button @click="submitCode" class="btn btn-success">Submit Code</button>
        <button @click="compareAI" class="btn btn-info">Compare AI</button>
        <div v-if="codeFeedback" class="comapre-ai-output">
          <h3>AI Feedback</h3>
          <p>{{ codeFeedback }}</p>
        </div>
        <transition name="fade">
          <div v-if="showPopup" class="popup">{{ popupMessage }}</div>
        </transition>
      </div>
      <h3>Test Cases</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Input</th>
            <th>Expected Output</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(testCase, index) in testCases" :key="index">
            <td>{{ testCase.input }}</td>
            <td>{{ testCase.output }}</td>
            <td :class="{'text-success': results[index] === 'Correct', 'text-danger': results[index] !== 'Correct'}">
              {{ results[index] }}
            </td>
          </tr>
        </tbody>
      </table>
      <div id="output" class="output">{{ output }}</div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      editor: null,
      codingQuestion: null,
      testCases: [],
      results: [],
      output: '',
      popupMessage: '',
      showPopup: false,
      codeFeedback: '',
      submissionId: null,
      questionId: 1  // Set the ID of the coding question you want to fetch
    };
  },
  async mounted() {
    // Fetch the coding question
    await this.fetchCodingQuestion();

    // Initialize Ace Editor
    this.editor = window.ace.edit("editor");
    this.editor.setTheme("ace/theme/light");
    this.editor.session.setMode("ace/mode/python");

    // Enable language tools
    window.ace.require("ace/ext/language_tools");
    this.editor.setOptions({
      enableBasicAutocompletion: true,
      enableLiveAutocompletion: true,
      enableSnippets: true
    });
  },
  methods: {
    async compareAI() {
      try {
        const response = await fetch('http://127.0.0.1:5000/compare-ai', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            submission_id: this.submissionId
          })
        });
        const result = await response.json();
        if (response.ok) {
          this.codeFeedback = result.code_feedback;
        } else {
          this.showPopupMessage(`Error: ${result.error}`);
        }
      }catch (error) {
        console.error('Error comparing AI:', error);
        this.showPopupMessage(`Error: ${error.message}`);
      }
    },
    async fetchCodingQuestion() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/coding_question/${this.questionId}`);
        const data = await response.json();
        this.codingQuestion = data;
        this.testCases = JSON.parse(data.test_cases);  // Assuming test cases are stored as JSON
        this.results = Array(this.testCases.length).fill('Not Executed');
      } catch (error) {
        console.error('Error fetching coding question:', error);
      }
    },
    async runCode() {
      const code = this.editor.getValue();
      try {
        const response = await fetch('http://127.0.0.1:5000/run_code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            code: code,
            test_cases: JSON.stringify(this.testCases)
          })
        });
        const result = await response.json();
        if (response.ok) {
          this.results = result;
          this.showPopupMessage("Code executed successfully.");
        } else {
          this.showPopupMessage(`Error: ${result.error}`);
        }
      } catch (e) {
        console.error('Error running code:', e);
        this.showPopupMessage(`Error: ${e.message}`);
      }
    },
    async submitCode() {
      const code = this.editor.getValue();
      try {
        // Send the code to the backend for storage
        const response = await fetch('http://127.0.0.1:5000/submit_code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            code: code,
            coding_question_id: this.codingQuestion.id
          })
        });
        const result = await response.json();
        if (response.ok) {
          this.submissionId = result.id;
        
          this.showPopupMessage(result.message);
        } else {
          this.showPopupMessage(`Error: ${result.error}`);
        }
      } catch (e) {
        console.error('Error submitting code:', e);
        this.showPopupMessage(`Error: ${e.message}`);
      }
    },
    showPopupMessage(message) {
      this.popupMessage = message;
      this.showPopup = true;
      setTimeout(() => {
        this.showPopup = false;
      }, 3000); // Hide the popup after 3 seconds
    }
  }
};
</script>

<style scoped>
body {
  font-family: 'Poppins', sans-serif;
}

h2 {
  color: #333;
  font-weight: 600;
  margin-bottom: 16px;
}

p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 24px;
}

.editor {
  height: 300px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 20px;
}

.button-container {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  position: relative;
}

.compare-ai-output {
  margin-top: 20px;
  padding: 15px;
  background-color: #f0f8ff;
  border: 1px solid #007bff;
  border-radius: 8px;
}

.btn {
  margin-right: 10px;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 500;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background-color: #007bff;
}

.btn-success {
  background-color: #28a745;
}

.btn-info {
  background-color: #17a2b8;
}

.btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.table {
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 0.75rem;
  vertical-align: top;
}

.table thead th {
  vertical-align: bottom;
  border-bottom: 2px solid #dee2e6;
}

.text-success {
  color: #28a745 !important;
  background-color: #e6f4ea !important;
}

.text-danger {
  color: #dc3545 !important;
  background-color: #f8d7da !important;
}

.output {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  background-color: #f8f9fa;
  color: #333;
}

.popup {
  margin-left: 10px;
  background-color: #9bc7f6;
  color: #2e1818;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: opacity 0.3s ease;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>