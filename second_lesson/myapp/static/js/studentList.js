function autoDismissMessages() {
    setTimeout(() => {
        const alertElements = document.querySelectorAll('.alert');
        alertElements.forEach(alert => {
            alert.remove();
        });
    }, 5000);
}

document.addEventListener('DOMContentLoaded', autoDismissMessages);
