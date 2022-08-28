import { getCookie } from "./utils.js";

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

        fetch(`http://127.0.0.1:8000/collection/${collectionId}`, {
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
