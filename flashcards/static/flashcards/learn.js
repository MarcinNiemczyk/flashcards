const flashcards = document.querySelectorAll('.game-flashcard');

let currentFlashcardIndex = loadFlashcard();


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
      flashcards[currentFlashcardIndex].style.transform = null;
      flashcards[currentFlashcardIndex].classList.remove('active');
      currentFlashcardIndex--;
      flashcards[currentFlashcardIndex].classList.add('active');
      localStorage.setItem('index', currentFlashcardIndex);
   }
}

document.getElementById('nextButton').onclick = () => {
   if (currentFlashcardIndex < flashcards.length - 1) {
      flashcards[currentFlashcardIndex].style.transform = null;
      flashcards[currentFlashcardIndex].classList.remove('active');
      currentFlashcardIndex++;
      flashcards[currentFlashcardIndex].classList.add('active');
      // Let the user start from beginning after learning from all flashcards
      if (currentFlashcardIndex === flashcards.length - 1) {
         localStorage.setItem('index', '0');
      } else {
         localStorage.setItem('index', currentFlashcardIndex);
      }
   }
}


function loadFlashcard() {
   let index;
   if (localStorage.hasOwnProperty('index')) {
      index = parseInt(localStorage.getItem('index'));
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
   flashcards[index].classList.add('active');

   return index;
}