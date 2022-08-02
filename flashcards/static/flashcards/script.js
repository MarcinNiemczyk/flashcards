
if (window.location.pathname === '/add') {
    const defaultFlashcards = 2
    let flashcardId = defaultFlashcards

    // Generate starting flashcards
    for (let flashcard = 1; flashcard <= defaultFlashcards; flashcard++) {
        addFlashcard(flashcard);
    }

    document.querySelector('.add-flashcard').onclick = () => {
        flashcardId++;
        addFlashcard(flashcardId);
    }
    updateButtons();

    document.querySelector('form').onsubmit = function(event) {
        const title = this.title.value;
        const visibility = this.visibility.value;

        const flashcards = []
        document.querySelectorAll('.content-section').forEach(content => {
            let flashcard = {
                'task': content.querySelector('.task').value,
                'solution': content.querySelector('.solution').value
            }
            flashcards.push(flashcard);
        });
        console.log(title);
        console.log(visibility);
        console.log(flashcards);
        event.preventDefault()
    }

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
