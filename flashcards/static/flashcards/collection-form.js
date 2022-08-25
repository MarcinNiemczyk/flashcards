let flashcardCounter = 0;

if (window.location.pathname === '/add') {
    // Generate starting flashcards
    const defaultFlashcards = 2;
    flashcardCounter = defaultFlashcards;

    for (let flashcard = 1; flashcard <= defaultFlashcards; flashcard++) {
    addFlashcard(flashcard);
    }
} else {
    // Count existing flashcards in edit mode
    document.querySelectorAll('.content-section').forEach(flashcard => {
        flashcardCounter++;
    })
}

// Add flashcard button
document.querySelector('.add-flashcard').onclick = () => {
    flashcardCounter++;
    addFlashcard(flashcardCounter);
}
updateButtons();

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

// Save collection
document.querySelector('form').onsubmit = function(event) {
    document.querySelector('.btn-primary').setAttribute('disabled', '');

    const title = this.title.value;
    const visibility = this.visibility.value;
    const language1 = selectedQuestionLanguage.innerHTML
    const language2 = selectedAnswerLanguage.innerHTML
    const csrftoken = this.csrfmiddlewaretoken.value

    const flashcards = []
    document.querySelectorAll('.content-section').forEach(content => {
        let flashcard = {
            'task': content.querySelector('.task').value,
            'solution': content.querySelector('.solution').value
        }
        flashcards.push(flashcard);
    });

    fetch((window.location.pathname === '/add' ? 'add' : window.location.pathname), {
        method: (window.location.pathname === '/add' ? 'POST' : 'PUT'),
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            title: title,
            visibility: visibility,
            language1: language1,
            language2: language2,
            flashcards: flashcards
        })
    })
        .then(response => response.json())
        .then(result => {
            document.querySelector('.btn-primary').removeAttribute('disabled');
            if ('error' in result) {
                createAlert('danger', result['error']);
            } else {
                window.location.replace('/library');
            }
        });
    event.preventDefault()
}

function addFlashcard(id) {
    const flashcardContainer = document.createElement('div');
    flashcardContainer.classList.add('content-section');
    flashcardContainer.setAttribute('id', `flashcard${id}`);
    const flashcard = `
        <div class="section-header d-flex justify-content-between mb-3">
            <div class="section-number">${id}</div>
            <div class="section-delete" name="${id}" id="delete${id}"><i class="fa-solid fa-trash-can"></i></div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <input type="text" class="form-control task" id="task${id}" minlength="1" maxlength="250" required>
                <label class="text-muted" for="task${id}">Task</label>
            </div>
            <div class="col-md-6">
                <input type="text" class="form-control solution" id="solution${id}" minlength="1" maxlength="250" required>
                <label class="text-muted" for="solution${id}">Solution</label>
            </div>
        </div>
    `;
    flashcardContainer.innerHTML += flashcard;
    document.querySelector('.flashcards').append(flashcardContainer);
    updateOrder();
    updateButtons();
    window.scrollTo(0, document.body.scrollHeight);
}

function deleteFlashcard(id) {
    document.getElementById(`flashcard${id}`).remove()
    updateOrder();
}

function updateOrder() {
    let counter = 1;
    document.querySelectorAll('.section-number').forEach(number => {
        number.innerHTML = counter;
        counter++;
    });
}

function updateButtons() {
    document.querySelectorAll('.section-delete').forEach(button => {
        button.onclick = () => {
            deleteFlashcard(button.getAttribute('name'));
        }
    });
}

function createAlert(category, message) {
    const alert = document.createElement('div');
    alert.classList.add('alert', `alert-${category}`, 'mb-5');
    alert.setAttribute('role', 'alert');
    alert.innerHTML = message;
    document.querySelector('main').prepend(alert);
}
