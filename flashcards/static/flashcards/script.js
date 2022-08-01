const defaultFlashcards = 2
let counter = defaultFlashcards

document.querySelector('.add-flashcard').onclick = () => {
    counter++;
    addFlashcard(counter);
}

function addFlashcard(counter) {
    const flashcard = `
        <div class="content-section" id="flashcard${counter}">
            <div class="section-header d-flex justify-content-between mb-3">
                <div class="section-number">${counter}</div>
                <div class="section-delete"><i class="fa-solid fa-trash-can"></i></div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <input type="text" class="form-control" id="task${counter}" minlength="1" maxlength="250">
                    <label class="text-muted" for="task${counter}">Task</label>
                </div>
                <div class="col-md-6">
                    <input type="text" class="form-control" id="solution${counter}" minlength="1" maxlength="250">
                    <label class="text-muted" for="solution${counter}">Solution</label>
                </div>
            </div>
        </div>
    `;
    document.querySelector('.flashcards').innerHTML += flashcard;
}