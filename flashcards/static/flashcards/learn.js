import { getCookie } from "./utils.js";

const csrftoken = getCookie('csrftoken');
const flashcards = document.querySelectorAll('.game-flashcard');
const settings = JSON.parse(document.getElementById('settings').textContent);

let index = settings['index'];
let random = settings['random'];
let reversed = settings['reversed'];
let order = settings['order'];
loadSettings();

if (order.trim().length === 0) {
   order = setOrder();
} else {
   order = JSON.parse(order);
}

if (reversed) {
   order = shuffle(order);
}
loadFlashcard(index);


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
   if (index > 0) {
      index--;
      loadFlashcard(index);
      updateSettings();
   }
}

document.getElementById('nextButton').onclick = () => {
   if (index < flashcards.length - 1) {
      index++;
      loadFlashcard(index);
      updateSettings();
   }
}

document.getElementById('resetProgress').onclick = () => {
   resetFlashcards();
}

document.getElementById('closeSettingsButton').onclick = () => {
   loadSettings();
}

document.getElementById('saveSettings').onclick = () => {
   updateRandomizeValue(document.getElementById('randomizeButton').checked);
   updateReverseValue(document.getElementById('reverseButton').checked);
   updateSettings();
}

function loadFlashcard(index) {
   flashcards.forEach(flashcard => {
      flashcard.style.transform = null;
      flashcard.classList.remove('active');
   });
   flashcards[order[index]].classList.add('active');
}

function loadSettings() {
   document.getElementById('randomizeButton').checked = random;
   document.getElementById('reverseButton').checked = reversed;
}

function resetFlashcards() {
   index = 0;
   loadFlashcard(0);
   updateSettings();
}

function updateRandomizeValue(status) {
   random = status;
   if (status) {
      order = shuffle(order);
      index = order.indexOf(index);
   } else {
      index = order[index];
      order = setOrder();
   }
}

function updateReverseValue(status) {
   reversed = status;
   if (status) {
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
   return array;
}

function updateSettings() {
   fetch('', {
      method: 'PUT',
      body: JSON.stringify({
         'index': index,
         'random': random,
         'reversed': reversed,
         'order': order
      }),
      headers: {
         'X-CSRFToken': csrftoken
      }
   });
}
