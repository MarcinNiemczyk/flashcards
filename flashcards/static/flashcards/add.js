const defaultFlashcards = 2
let flashcardId = defaultFlashcards

// Generate starting flashcards
for (let flashcard = 1; flashcard <= defaultFlashcards; flashcard++) {
    addFlashcard(flashcard);
}

// Select language
const selected = document.querySelector('.selected');
const optionsContainer = document.querySelector('.options-container');
const searchBox = document.querySelector('.search-box input');

const optionsList = document.querySelectorAll('.option');

selected.addEventListener('click', () => {
    optionsContainer.classList.toggle('active');
    searchBox.value = '';
    filterList('');
    if (optionsContainer.classList.contains('active')) {
        searchBox.focus();
    }
});

optionsList.forEach(option => {
    option.addEventListener('click', () => {
        selected.innerHTML = option.querySelector("label").innerHTML;
        optionsContainer.classList.remove('active');
    });
});

searchBox.addEventListener('keyup', function(event) {
    filterList(event.target.value);
});

const filterList = searchTerm => {
    searchTerm = searchTerm.toLowerCase();
    optionsList.forEach(option => {
        let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
        if (label.indexOf(searchTerm) > -1) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}


// Add flashcard button
document.querySelector('.add-flashcard').onclick = () => {
    flashcardId++;
    addFlashcard(flashcardId);
}
updateButtons();

// Save collection
document.querySelector('form').onsubmit = function(event) {
    // Temporarily block save button until server responds
    document.querySelector('.btn-primary').setAttribute('disabled', '');

    // Load form data
    const title = this.title.value;
    const visibility = this.visibility.value;
    const csrftoken = this.csrfmiddlewaretoken.value

    // Make every flashcard and add to array
    const flashcards = []
    document.querySelectorAll('.content-section').forEach(content => {
        let flashcard = {
            'task': content.querySelector('.task').value,
            'solution': content.querySelector('.solution').value
        }
        flashcards.push(flashcard);
    });

    // Send add collection request
    fetch('add', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            title: title,
            visibility: visibility,
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
