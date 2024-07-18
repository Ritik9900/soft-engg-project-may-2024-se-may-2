<template>
    <div class="coding-container">
      <h3>Coding Question</h3>
      <div class="question-container">
        <p><strong>Q:</strong> {{ question }}</p>
        <h4>Test Cases:</h4>
        <ul>
          <li v-for="(testCase, index) in parsedTestCases" :key="index">
            <strong>Input:</strong> {{ testCase.input }} <br />
            <strong>Expected Output:</strong> {{ testCase.output }}
          </li>
        </ul>
        <textarea v-model="answer" placeholder="Type your answer here..." rows="10" cols="50"></textarea>
        <button @click="submitAnswer">Submit</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CodingView',
    props: {
      question: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        answer: ''
      };
    },
    computed: {
      parsedTestCases() {
        try {
          return JSON.parse(this.question.test_cases);
        } catch (e) {
          console.error('Error parsing test cases:', e);
          return [];
        }
      }
    },
    methods: {
      async submitAnswer() {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/submissions`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              code: this.answer,
              coding_question_id: this.question.id
            })
          });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          console.log(data)
          alert('Answer submitted successfully!');
        } catch (error) {
          console.error('Error submitting answer:', error);
          alert('Failed to submit answer. Please try again.');
        }
      }
    }
  };
  </script>
  
  <style>
  .coding-container {
    padding: 20px;
  }
  
  .question-container {
    background: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  
  button {
    margin-top: 10px;
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  