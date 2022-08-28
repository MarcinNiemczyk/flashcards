export function getCookie(name) {
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

export function createAlert(category, message) {
    const alert = document.createElement('div');
    alert.classList.add('alert', `alert-${category}`, 'mb-5');
    alert.setAttribute('role', 'alert');
    alert.innerHTML = message;
    document.querySelector('main').prepend(alert);
}
