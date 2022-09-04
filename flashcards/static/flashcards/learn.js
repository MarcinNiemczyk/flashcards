const flashcards = document.querySelectorAll('.game-flashcard');

const settings = loadSettings();
let random = settings['random'];
let order = settings['order'];
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
      localStorage.setItem('index', currentFlashcardIndex);
   }
}

document.getElementById('resetProgress').onclick = () => {
   resetFlashcards();
}

document.getElementById('saveSettings').onclick = () => {
   if (document.getElementById('randomizeButton').checked) {
      updateRandomizeValue(true);
   } else {
      updateRandomizeValue(false);
   }
}

function loadIndex() {
   let index;
   if (localStorage.hasOwnProperty('index')) {
      index = parseInt(localStorage.getItem('index'));
      flashcards[index].classList.contains('active');
   } else {
      localStorage.setItem('index', '0');
      index = 0;
   }
   return index;
}

function loadSettings() {
   let random;
   let order;
   if (localStorage.getItem('random') === 'true') {
      random = Boolean(localStorage.getItem('random'));
      document.getElementById('randomizeButton').checked = true;
   } else {
      localStorage.setItem('random', 'false');
      random = false;
   }
   if (localStorage.hasOwnProperty('order')) {
      order = JSON.parse(localStorage.getItem('order'));
   } else {
      order = setOrder();
   }
   return {'random': random, 'order': order}
}

function loadFlashcard(index) {
   flashcards.forEach(flashcard => {
      flashcard.style.transform = null;
      flashcard.classList.remove('active');
   });
   flashcards[order[index]].classList.add('active');
}

function resetFlashcards() {
   localStorage.setItem('index', '0');
   currentFlashcardIndex = 0;
   loadFlashcard(0);
}

function updateRandomizeValue(value) {
   random = value;
   localStorage.setItem('random', value);
   if (value === true) {
      order = shuffle(order);
   } else {
      order = setOrder();
   }
   resetFlashcards();
}

function setOrder() {
   let order = [];
   for (let i = 0; i < flashcards.length; i++) {
      order.push(i);
   }
   localStorage.setItem('order', JSON.stringify(order));
   return order;
}

function shuffle(array) {
   // Fisher-Yates shuffle algorithm
   let currentIndex = array.length, randomIndex;

   while (currentIndex != 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
      [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
   }
   localStorage.setItem('order', JSON.stringify(array));
   return array;
}