// Lightweight, dependency-free quiz component shared across lessons.
//
// Markup contract:
//   <div class="quiz-question">
//     <p class="prompt">...</p>
//     <ul class="quiz-options">
//       <li><button class="quiz-option" data-correct="true">...</button></li>
//       <li><button class="quiz-option" data-correct="false">...</button></li>
//     </ul>
//     <p class="quiz-feedback" aria-live="polite"></p>
//   </div>
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.quiz-question').forEach((question) => {
    const feedback = question.querySelector('.quiz-feedback');
    const options = question.querySelectorAll('.quiz-option');

    options.forEach((option) => {
      option.addEventListener('click', () => {
        const correct = option.dataset.correct === 'true';

        options.forEach((o) => o.classList.remove('is-correct', 'is-incorrect'));
        option.classList.add(correct ? 'is-correct' : 'is-incorrect');

        if (feedback) {
          feedback.textContent = correct ? 'Correct.' : 'Not quite — try another option.';
          feedback.classList.toggle('is-correct', correct);
          feedback.classList.toggle('is-incorrect', !correct);
        }

        // Lock the question once answered correctly; leave it open to retry otherwise.
        if (correct) {
          options.forEach((o) => { o.disabled = true; });
        }
      });
    });
  });
});
