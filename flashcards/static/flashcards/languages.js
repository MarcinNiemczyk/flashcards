const selectedQuestionLanguage = document.querySelector('.selected-question');
const questionLanguagesContainer = document.querySelector('.question-container');
const questionSearchBox = document.querySelector('.question-search input');
const questionLanguages = document.querySelectorAll('.question-language');

// Question language dropdown menu
selectedQuestionLanguage.addEventListener('click', () => {
    if (answerLanguagesContainer.classList.contains('active')) {
        answerLanguagesContainer.classList.remove('active');
    }
    questionLanguagesContainer.classList.toggle('active');
    questionSearchBox.value = '';
    filterQuestionLanguage('');
    if (questionLanguagesContainer.classList.contains('active')) {
        questionSearchBox.focus();
    }
});

// Change selected question language
questionLanguages.forEach(option => {
    option.addEventListener('click', () => {
        selectedQuestionLanguage.innerHTML = option.querySelector('label').innerHTML;
        questionLanguagesContainer.classList.remove('active');
    });
});

// Question language search bar
questionSearchBox.addEventListener('keyup', function(event) {
    filterQuestionLanguage(event.target.value);
});
const filterQuestionLanguage = searchTerm => {
    searchTerm = searchTerm.toLowerCase();
    questionLanguages.forEach(option => {
        let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
        if (label.indexOf(searchTerm) > -1) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

const selectedAnswerLanguage = document.querySelector('.selected-answer');
const answerLanguagesContainer = document.querySelector('.answer-container');
const answerSearchBox = document.querySelector('.answer-search input');
const answerLanguages = document.querySelectorAll('.answer-language');

// Answer language dropdown menu
selectedAnswerLanguage.addEventListener('click', () => {
    if (questionLanguagesContainer.classList.contains('active')) {
        questionLanguagesContainer.classList.remove('active');
    }
    answerLanguagesContainer.classList.toggle('active');
    answerSearchBox.value = '';
    filterAnswerLanguage('');
    if (answerLanguagesContainer.classList.contains('active')) {
        answerSearchBox.focus();
    }
});

// Change selected answer language
answerLanguages.forEach(option => {
    option.addEventListener('click', () => {
        selectedAnswerLanguage.innerHTML = option.querySelector('label').innerHTML;
        answerLanguagesContainer.classList.remove('active');
    });
});

// Answer language search bar
answerSearchBox.addEventListener('keyup', function(event) {
    filterAnswerLanguage(event.target.value);
});
const filterAnswerLanguage = searchTerm => {
    searchTerm = searchTerm.toLowerCase();
    answerLanguages.forEach(option => {
        let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
        if (label.indexOf(searchTerm) > -1) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}
