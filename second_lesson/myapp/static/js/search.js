function searchStudentName() {
    var input = document.getElementById('student_name').value;
    if (input.length > 0) {
        fetch(`/search_student_name?query=${input}`)
            .then(response => response.json())
            .then(data => {
                var suggestions = document.getElementById('student_suggestions');
                suggestions.innerHTML = '';
                data.forEach(name => {
                    var suggestionItem = document.createElement('a');
                    suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                    suggestionItem.innerText = name;
                    suggestionItem.onclick = () => {
                        document.getElementById('student_name').value = name;
                        suggestions.innerHTML = '';
                    };
                    suggestions.appendChild(suggestionItem);
                });
            });
    } else {
        document.getElementById('student_suggestions').innerHTML = '';
    }
}
