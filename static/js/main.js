// // main.js

// document.addEventListener('DOMContentLoaded', function() {
//     const filterByPriority = document.getElementById('filter_by_priority');
//     const sortByPriority = document.getElementById('sort_by_priority');
    
//     filterByPriority.addEventListener('click', function() {
//         // Implement AJAX call to filter endpoint
//         // Example using Fetch API
//         fetch('/api/tasks/?category=priority')
//             .then(response => response.json())
//             .then(data => {
//                 // Update UI with filtered data
//                 // alert(data);
//                 console.log(data);
//             })
//             .catch(error => {
//                 console.error('Error fetching data:', error);
//             });
//     });
    
//     sortByPriority.addEventListener('click', function() {
//         // Implement AJAX call to sort endpoint
//         // Example using Fetch API
//         fetch('/api/tasks/?ordering=priority')
//             .then(response => response.json())
//             .then(data => {
//                 // Update UI with sorted data
//                 console.log(data);
//                 alert(data);
//             })
//             .catch(error => {
//                 console.error('Error fetching data:', error);
//             });
//     });
// });
