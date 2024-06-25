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





// drag-and-drop.js

function allowDrop(ev) {
    ev.preventDefault();
    // console.log(ev.target.id);
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    // console.log(ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var taskElement = document.getElementById(data);
    var newStatus = ev.target.id;

    if (newStatus == 'completed_tasks') {
        newStatus = 'Completed';
    } else if (newStatus == 'overdue_tasks') {
        newStatus = 'Overdue';
    } else if (newStatus == 'in_progress_tasks') {
        newStatus = 'In_progress';
    } else {
        newStatus;
    }
    
    // Ensure we drop in the correct container
    console.log(ev.target.className);
    if (ev.target.className === 'task-column my-5 min-h-full') {
        // console.log(ev.target.className);
        ev.target.appendChild(taskElement);
        taskElement.dataset.status = newStatus;
        // console.log(taskElement.dataset.status);

        // Update status on the server
        updateTaskStatus(data, newStatus);
    }
}

function updateTaskStatus(taskId, newStatus) {
    fetch('/update-task-status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            taskId: taskId,
            newStatus: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Task status updated successfully');
        } else {
            console.error('Error updating task status:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
