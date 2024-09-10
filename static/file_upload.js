document.addEventListener('DOMContentLoaded', function() {
  // Get the file input element
  const fileInput = document.getElementById('file');

  // Get the Cancel and Confirm buttons
  const cancelBtn = document.getElementById('cancelBtn');
  const confirmBtn = document.getElementById('confirmBtn');

  // Get the buttons group element
  const btnGroup = document.getElementById('btnGroup');

  // Get the Processing button
  const processBtn = document.getElementById('processBtn');

  // Add event listener to the file input for change event
  fileInput.addEventListener('change', function() {
    // Check if the uploaded file is a video file
    if (fileInput.files[0].type.startsWith('video/')) {
      // Show the buttons group
      btnGroup.style.display = 'block';
    } else {
      // If not a video file, alert the user and reset the file input
      alert('Please upload a valid video file.');
      fileInput.value = ''; // Reset the file input
    }
  });

  // Add event listener to the Confirm button
  confirmBtn.addEventListener('click', function() {
    // After confirming, you can show the Processing button group if needed
    // For now, I'm just showing it directly
    document.getElementById('processingBtnGroup').style.display = 'block';
  });

  // Add event listener to the Process Video button
  processBtn.addEventListener('click', function() {
    // Get the uploaded file
    const file = fileInput.files[0];

    // Create a FormData object and append the file to it
    const formData = new FormData();
    formData.append('file', file);

    // Send AJAX request to the server to save the file
    fetch('/file-upload', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      // Check if the response status is 200 (OK)
      if (response.status === 200) {
        // If response is OK, redirect to the processing page
        window.location.href = '/processing?video_path=uploaded_video.mp4';
      } else {
        // Handle other response statuses
        console.error('Error: Unexpected response status:', response.status);
      }
    })
    .catch(error => {
      // Handle errors (if any)
      console.error('Error:', error);
    });
  });
});
