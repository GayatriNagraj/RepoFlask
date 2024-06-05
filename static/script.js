function openUpdateModal(uniqueId, title, description, taskDone) {
    document.getElementById('update_unique_id').value = uniqueId;
    document.getElementById('update_title').value = title;
    document.getElementById('update_description').value = description;
    document.getElementById('update_task_done').checked = (taskDone === 'true');
    document.getElementById('updateModal').style.display = 'block';
}

function closeUpdateModal() {
    document.getElementById('updateModal').style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('updateModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
