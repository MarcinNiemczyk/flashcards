
if (window.location.pathname === '/add') {
    const defaultFlashcards = 2
    let flashcardId = defaultFlashcards

    document.querySelector('.add-flashcard').onclick = () => {
        flashcardId++;
        addFlashcard(flashcardId);
    }

    updateButtons();

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
                <input type="text" class="form-control" id="task${id}" minlength="1" maxlength="250" required name="flashcard${id}">
                <label class="text-muted" for="task${id}">Task</label>
            </div>
            <div class="col-md-6">
                <input type="text" class="form-control" id="solution${id}" minlength="1" maxlength="250" required name="flashcard${id}">
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
