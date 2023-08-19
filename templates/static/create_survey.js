// static/create_survey.js
const questionContainer = document.querySelector('.question-container');
const addQuestionButton = document.getElementById('add-question');

addQuestionButton.addEventListener('click', () => {
    alert('Button clicked')
    const newQuestion = document.createElement('div');
    newQuestion.className = 'question';
    newQuestion.innerHTML = `
        <label for="question">Survey Question:</label>
        <input type="text" name="question[]" required><br>
        <label for="options">Options (comma-separated):</label>
        <input type="text" name="options[]" required><br>
    `;
    questionContainer.appendChild(newQuestion);
});
