document.getElementById('filter-toggle').onclick = () => {
    document.querySelector('.filter-collections').classList.toggle('active');
}

document.querySelectorAll('.followButton').forEach(button => {
    button.addEventListener('click', function() {
        this.setAttribute('disabled', '');
        const collectionId = this.getAttribute('name');
        const followers = document.getElementById(`followers${collectionId}`);
        let followersNumber = parseInt(followers.innerHTML);

        if (this.innerHTML === 'Follow') {
            this.innerHTML = 'Following';
            this.classList.remove('btn-outline-dark');
            this.classList.add('btn-dark');
            followers.innerHTML = (followersNumber + 1).toString();
        } else {
            this.innerHTML = 'Follow'
            this.classList.remove('btn-dark');
            this.classList.add('btn-outline-dark');
            followers.innerHTML = (followersNumber - 1).toString();
        }

        const csrftoken = getCookie('csrftoken');

        fetch(`collection/${collectionId}`, {
            method: 'PATCH',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
            .then(response => response.json())
            .then(result => {
                this.removeAttribute('disabled');
            });
    });
});

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
