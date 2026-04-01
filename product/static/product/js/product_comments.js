// for set/remove disabled attr on Comment/edit Button
function disableBtnWhenTextEmpty(inputTextElement, btnElement, e) {
  if (e.target.value.trim().length > 0) {
    btnElement.removeAttribute('disabled');
  } else {
    btnElement.setAttribute('disabled', '');
  }
}






function showEditForm(commentId) {
  const editForm = document.getElementById(`edit-form-${commentId}`)
  const commentTextElement = document.getElementById(`comment-text-${commentId}`);
  const editTextareaElement = document.getElementById(`edit-comment-text-${commentId}`);
  const dropDownChoicesBtn = document.getElementById(`dropdown-choices-${commentId}`);
  let editBtn = document.getElementById(`edit-btn-${commentId}`);

  

  commentTextElement.classList.add('d-none');
  editForm.classList.remove('d-none');
  dropDownChoicesBtn.classList.add('d-none');
  editTextareaElement.focus();
}




// when user press 'Enter' send the comment 
// and handle the (shift + Enter)
function updateComment(element, e) {
    if (!e.shiftKey && e.key === "Enter") {
        e.preventDefault(); 
        
        // Get the ID from the textarea ID
        // If the ID is: edit-comment-text-5, it will take the number 5.
        const commentId = element.id.split('-').pop(); 
        const newText = element.value.trim();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (newText.length === 0) return;

        // Delete the word "new" and send the text directly.
        const bodyData = `text=${encodeURIComponent(newText)}`;

        fetch(`/comments/edit/${commentId}/`, { 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: bodyData
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                const textDisplay = document.getElementById(`comment-text-${commentId}`);
                textDisplay.innerText = data.text; // Update the old text with the new one

                // Hide the form and restore the original appearance
                document.getElementById(`edit-form-${commentId}`).classList.add('d-none');
                textDisplay.classList.remove('d-none');
                
                const dropDownBtn = document.getElementById(`dropdown-choices-${commentId}`);
                if(dropDownBtn) dropDownBtn.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred during editing, please try again.");
        });
    }
}



function preventEnter(element, e) {
  if (e.key === "Enter" && !e.shiftKey) {
    
    e.preventDefault();

    if (element.value.trim().length > 0) {
      element.closest('form').submit();

    } else {

      return;
    }
  }
}