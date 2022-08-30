let currentFlashcardIndex = 0;

const flashcards = document.querySelectorAll('.game-flashcard');
flashcards[currentFlashcardIndex].classList.add('active');

flashcards.forEach((flashcard) => {
   flashcard.addEventListener('click', () => {
      flashcard.classList.toggle('flipped');
   });
});

document.getElementById('prevButton').onclick = () => {
   if (currentFlashcardIndex > 0) {
      flashcards[currentFlashcardIndex].classList.remove('active');
      currentFlashcardIndex--;
      flashcards[currentFlashcardIndex].classList.add('active');
   }
}

document.getElementById('nextButton').onclick = () => {
   if (currentFlashcardIndex < flashcards.length - 1) {
      flashcards[currentFlashcardIndex].classList.remove('active');
      currentFlashcardIndex++;
      flashcards[currentFlashcardIndex].classList.add('active');
   }
}
