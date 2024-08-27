function searchTeacherName() {
    var input = document.getElementById('name').value;
    if (input.length > 0) {
        fetch(`/search_teacher_name?query=${input}`)
            .then(response => response.json())
            .then(data => {
                var suggestions = document.getElementById('suggestions');
                suggestions.innerHTML = '';
                data.forEach(name => {
                    var suggestionItem = document.createElement('a');
                    suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                    suggestionItem.innerText = name;
                    suggestionItem.onclick = () => {
                        document.getElementById('name').value = name;
                        suggestions.innerHTML = '';
                    };
                    suggestions.appendChild(suggestionItem);
                });
            });
    } else {
        document.getElementById('suggestions').innerHTML = '';
    }
}
