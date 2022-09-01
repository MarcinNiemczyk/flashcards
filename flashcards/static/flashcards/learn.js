const flashcards = document.querySelectorAll('.game-flashcard');

let currentFlashcardIndex = loadIndex();
loadFlashcard(currentFlashcardIndex);


flashcards.forEach((flashcard) => {
   flashcard.addEventListener('click', () => {
      if (flashcard.style.transform === 'rotateX(180deg)') {
         flashcard.style.transform = null;
      } else {
         flashcard.style.transform = 'rotateX(180deg)';
      }
   });
});

document.getElementById('prevButton').onclick = () => {
   if (currentFlashcardIndex > 0) {
      currentFlashcardIndex--;
      loadFlashcard(currentFlashcardIndex);
      localStorage.setItem('index', currentFlashcardIndex);
   }
}

document.getElementById('nextButton').onclick = () => {
   if (currentFlashcardIndex < flashcards.length - 1) {
      currentFlashcardIndex++;
      loadFlashcard(currentFlashcardIndex);

      // Let the user start from scratch after learning from all flashcards
      if (currentFlashcardIndex === flashcards.length - 1) {
         localStorage.setItem('index', '0');
      } else {
         localStorage.setItem('index', currentFlashcardIndex);
      }
   }
}

function loadIndex() {
   let index;
   if (localStorage.hasOwnProperty('index')) {
      index = parseInt(localStorage.getItem('index'));
      // Ensure index is correct
      try {
         flashcards[index].classList.contains('active');
      } catch(err) {
         localStorage.removeItem('index');
         return loadFlashcard(flashcards);
      }
   } else {
      localStorage.setItem('index', '0');
      index = 0;
   }
   return index;
}

function loadFlashcard(index) {
   resetFlashcards();
   flashcards[index].classList.add('active');
}

function resetFlashcards() {
   flashcards.forEach(flashcard => {
      flashcard.style.transform = null;
      flashcard.classList.remove('active');
   });
}