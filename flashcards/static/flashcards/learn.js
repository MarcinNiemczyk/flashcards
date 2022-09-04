const flashcards = document.querySelectorAll('.game-flashcard');

const id = window.location.pathname;
const settings = loadSettings();
let random = settings['random'];
let order = settings['order'];
let reverse = settings['reverse'];
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
      setLocalStorage('index', currentFlashcardIndex);
   }
}

document.getElementById('nextButton').onclick = () => {
   if (currentFlashcardIndex < flashcards.length - 1) {
      currentFlashcardIndex++;
      loadFlashcard(currentFlashcardIndex);
      setLocalStorage('index', currentFlashcardIndex);
   }
}

document.getElementById('resetProgress').onclick = () => {
   resetFlashcards();
}

document.getElementById('closeSettingsButton').onclick = () => {
   // Ensure cancel button doesnt save switch buttons state
   document.getElementById('randomizeButton').checked = random;
   document.getElementById('reverseButton').checked = reverse;
}

document.getElementById('saveSettings').onclick = () => {
   updateRandomizeValue(document.getElementById('randomizeButton').checked);
   updateReverseValue(document.getElementById('reverseButton').checked);
}

function loadIndex() {
   let index;
   if (checkLocalStorage('index')) {
      index = parseInt(getLocalStorage('index'));
      flashcards[index].classList.contains('active');
   } else {
      setLocalStorage('index', '0');
      index = 0;
   }
   return index;
}

function loadSettings() {
   let random;
   let order;
   let reverse;

   if (getLocalStorage('random') === 'true') {
      random = true;
      document.getElementById('randomizeButton').checked = true;
   } else {
      setLocalStorage('random', 'false');
      random = false;
   }

   if (checkLocalStorage('order')) {
      order = JSON.parse(getLocalStorage('order'));
   } else {
      order = setOrder();
   }

   if (getLocalStorage('reverse') === 'true') {
      reverse = true;
      document.getElementById('reverseButton').checked = true;
   } else {
      setLocalStorage('reverse', 'false');
      reverse = false;
   }
   if (reverse) {
      document.querySelector('.game-flashcards').classList.add('reversed');
   }

   return {'random': random, 'order': order, 'reverse': reverse}
}

function loadFlashcard(index) {
   flashcards.forEach(flashcard => {
      flashcard.style.transform = null;
      flashcard.classList.remove('active');
   });
   flashcards[order[index]].classList.add('active');
}

function resetFlashcards() {
   setLocalStorage('index', '0');
   currentFlashcardIndex = 0;
   loadFlashcard(0);
}

function updateRandomizeValue(value) {
   random = value;
   setLocalStorage('random', value);
   if (value) {
      order = shuffle(order);
      currentFlashcardIndex = order.indexOf(currentFlashcardIndex);
   } else {
      currentFlashcardIndex = order[currentFlashcardIndex];
      order = setOrder();
   }
}

function updateReverseValue(value) {
   reverse = value;
   setLocalStorage('reverse', value);
   if (value) {
      document.querySelector('.game-flashcards').classList.add('reversed');
   } else {
      document.querySelector('.game-flashcards').classList.remove('reversed');
   }
}

function setOrder() {
   let order = [];
   for (let i = 0; i < flashcards.length; i++) {
      order.push(i);
   }
   setLocalStorage('order', JSON.stringify(order));
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
   setLocalStorage('order', JSON.stringify(array));
   return array;
}

function setLocalStorage(key, value) {
   localStorage.setItem(`${id}${key}`, value);
}

function getLocalStorage(key) {
   item = localStorage.getItem(`${id}${key}`);
   return item;
}

function checkLocalStorage(key) {
   hasProperty = localStorage.hasOwnProperty(`${id}${key}`);
   return hasProperty;
}
