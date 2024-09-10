document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');

    registrationForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Get form values
        const name = document.getElementById('name').value;
        const classValue = document.getElementById('class').value;
        const section = document.getElementById('section').value;
        const rollNumber = document.getElementById('rollNumber').value;
        const gender = document.querySelector('input[name="gender"]:checked').value;

        // Create a URL-encoded form data string
        const formData = new URLSearchParams();
        formData.append('Name', name);
        formData.append('Class', classValue);
        formData.append('Section', section);
        formData.append('Roll_Number', rollNumber);
        formData.append('Gender', gender);

        // Function to submit form data via fetch and handle responses
        async function submitForm(url, formData) {
            const response = await fetch(url, {
                method: 'POST',
                body: formData, // Send form data as URL-encoded
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            return response;
        }

        // Endpoint for registration (same as current route)
        const registerUrl = '/student-register'; // Update with your registration endpoint

        // Submit form data via fetch and handle responses
        const response = await submitForm(registerUrl, formData);

        if (!response) {
            alert('An error occurred while processing your request.');
            return;
        }

        const responseData = await response.text();

        console.log('Response Status:', response.status);
        console.log('Response Data:', responseData);

        if (response.status === 200) {
            alert('Student Registered Successfully.');
            // Optionally redirect to another page after successful registration
            // window.location.href = '/dashboard'; // Redirect to dashboard after registration
        } else if (response.status === 400 && responseData.includes('Student with the given Roll Number already exists.')) {
            alert('Student with the given Roll Number already exists.');
        } else {
            console.error('Unexpected response status:', response.status);
            alert('An error occurred while processing your request.');
        }

        // Reset the form after submission
        registrationForm.reset();
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');

    // Add event listeners for button clicks
    document.getElementById('maleButton').addEventListener('click', function() {
        document.getElementById('gender').value = 'male';
    });

    document.getElementById('femaleButton').addEventListener('click', function() {
        document.getElementById('gender').value = 'female';
    });

    registrationForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Rest of the form submission code...
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');

    // Add event listeners for radio button clicks
    const maleRadio = document.getElementById('maleRadio');
    const femaleRadio = document.getElementById('femaleRadio');

    maleRadio.addEventListener('change', function() {
        if (maleRadio.checked) {
            document.getElementById('gender').value = 'male';
        }
    });

    femaleRadio.addEventListener('change', function() {
        if (femaleRadio.checked) {
            document.getElementById('gender').value = 'female';
        }
    });

    registrationForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Rest of the form submission code...
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');

    // Add event listener for "Back to Dashboard" button click
    document.getElementById('backToDashboardButton').addEventListener('click', function() {
        // Redirect to index.html one folder back
        window.location.href = '/dashboard';
    });

    // Rest of your JavaScript code for form submission, etc.
    registrationForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        // Rest of the form submission code...
    });
});
