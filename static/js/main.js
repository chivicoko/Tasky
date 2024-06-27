// main.js

document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.getElementById('filter-btn');
    const sortButton = document.getElementById('sort-btn');
    
    filterButton.addEventListener('click', function() {
        // Implement AJAX call to filter endpoint
        // Example using Fetch API
        fetch('/api/tasks/?category=work')
            .then(response => response.json())
            .then(data => {
                // Update UI with filtered data
                console.log(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
    
    sortButton.addEventListener('click', function() {
        // Implement AJAX call to sort endpoint
        // Example using Fetch API
        fetch('/api/tasks/?ordering=-due_date')
            .then(response => response.json())
            .then(data => {
                // Update UI with sorted data
                console.log(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});
