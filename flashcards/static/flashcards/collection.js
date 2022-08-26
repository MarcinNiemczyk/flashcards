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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
