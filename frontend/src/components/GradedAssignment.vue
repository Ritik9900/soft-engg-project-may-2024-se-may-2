<template>
  <div class="quiz">
    <h2>Grading Assignment</h2>
    <div v-for="(question, index) in questions" :key="index" class="question">
      <p>{{ question.text }}</p>
      <div v-for="(option, optionIndex) in question.options" :key="optionIndex">
        <label
          :class="{
            correct: submitted && selectedAnswers[index] === optionIndex && isCorrect(index, optionIndex),
            incorrect: submitted && selectedAnswers[index] === optionIndex && !isCorrect(index, optionIndex)
          }"
          :disabled="submitted"
        >
          <input
            type="radio"
            :name="'question_' + index"
            :value="optionIndex"
            v-model="selectedAnswers[index]"
            :disabled="submitted"
          />
          {{ option }}
        </label>
      </div>
    </div>
    <button @click="submit">Submit</button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const questions = ref([
      {
        text: 'It is a way of breaking the complexity of the system into manageable parts.',
        options: ['True', 'False'],
        correctAnswerIndex: 0
      },
      {
        text: 'A software company wants to build a website for employee welfare...',
        options: ['External users', 'Internal users', 'Software or software components', 'Developers'],
        correctAnswerIndex: 1
      },
      // Add more questions as needed
    ]);

    const selectedAnswers = ref([]);
    const submitted = ref(false);

    const isCorrect = (questionIndex, optionIndex) => {
      return questions.value[questionIndex].correctAnswerIndex === optionIndex;
    };

    const submit = () => {
      if (confirm('Are you sure you want to submit your answers?')) {
        submitted.value = true;
      }
    };

    return {
      questions,
      selectedAnswers,
      submitted,
      isCorrect,
      submit
    };
  }
};
</script>

<style scoped>
.correct {
  color: green;
}

.incorrect {
  color: red;
}

.question {
  margin-bottom: 20px;
}

label {
  display: block;
  margin: 5px 0;
}

input[disabled] {
  cursor: not-allowed;
}
</style>
