import { getCookie } from "./utils.js";

document.getElementById('toggle-flashcards').onclick = () => {
    document.querySelector('.collection-flashcards').classList.toggle('active');
}

document.getElementById('confirmDelete').onclick = function() {
    this.setAttribute('disabled', '');
    let csrftoken = getCookie('csrftoken');

    fetch(window.location.pathname, {
                method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => response.json())
        .then(result => {
            this.removeAttribute('disabled');
            if ('success' in result) {
                window.location.replace('/library');
            }
        });
}
