const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});

const dashboardLink = document.getElementById('dashboard-link');

    if (dashboardLink) {
        dashboardLink.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default behavior of anchor tag

            // Redirect to /dashboard
            window.location.href = '/dashboard';
        });
    }


// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})

// Function to open the student registration page in the same tab
function openStudentRegister() {
    window.location.href = '/student-register';
}
// Add event listener to the "Register Student" button
const registerButton = document.querySelector('.btn-download');
registerButton.addEventListener('click', openStudentRegister);

// Function to handle logout action
// Function to handle logout action
function logoutUser() {
    fetch('/dashboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ logout: true })
    })
    .then(response => {
        if (response.ok) {
            // Clear any session data on the client-side
            window.location.href = '/'; // Redirect to your login page after logout
        } else {
            console.error('Logout failed:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error during logout:', error);
    });
}

// Add event listener to the logout button with class "logout"
const logoutButton = document.querySelector('.logout');
logoutButton.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default link behavior

    // Call the logoutUser function to perform logout actions
    logoutUser();
});



const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})


// Function to fetch and update table data
// function updateTableData() {
//     // Fetch data from data.json
//     fetch('data.json')
//         .then(response => response.json())
//         .then(data => {
//             // Reverse the data array to prepend new entries to the top
//             data.reverse().forEach(entry => {
//                 // Create a new table row
//                 const newRow = document.createElement('tr');
//                 // Construct HTML for the new row
//                 newRow.innerHTML = `
//                     <td>
//                         <img src="${entry.image}">
//                         <p>${entry.name}</p>
//                     </td>
//                     <td>${entry.date}</td>
//                     <td><span class="status ${entry.status.toLowerCase()}">${entry.status}</span></td>
//                     <td>
//                         <button class="live-stream-btn">Live Stream</button>
//                         <button class="upload-btn">Upload</button>
//                     </td>
//                 `;
//                 // Prepend the new row to the table body
//                 const tableBody = document.querySelector('table tbody');
//                 tableBody.insertBefore(newRow, tableBody.firstChild);
//             });
//         })
//         .catch(error => console.error('Error fetching data:', error));
// }


// document.addEventListener("DOMContentLoaded", function() {
//     // Get all the buttons with class "live-stream-btn"
//     const liveStreamButtons = document.querySelectorAll(".live-stream-btn");

//     // Attach click event listeners to each button
//     liveStreamButtons.forEach(button => {
//         button.addEventListener("click", function() {
//             // Redirect to the live stream page
//             window.location.href = "/live-stream";
//         });
//     });

//     // Get all the buttons with class "upload-btn"
//     const uploadButtons = document.querySelectorAll(".upload-btn");

//     // Attach click event listeners to each button
//     uploadButtons.forEach(button => {
//         button.addEventListener("click", function() {
//             // Redirect to the upload page
//             window.location.href = "/file-upload";
//         });
//     });
// });


  document.addEventListener('DOMContentLoaded', function () {
    const radioLabels = document.querySelectorAll('.radio-group label');

    radioLabels.forEach(label => {
        label.addEventListener('click', function () {
            const radioInput = this.querySelector('input[type="radio"]');
            if (!radioInput.checked) {
                radioInput.checked = true;
            }
        });
    });
});



// Inside your script.js file or in a <script> tag in your HTML

// Add an event listener to all class box labels
document.querySelectorAll('.class-box').forEach(function(label) {
    label.addEventListener('click', function() {
        // Find the associated radio button inside this label
        var radioBtn = this.querySelector('input[type="radio"]');
        // Check the radio button
        radioBtn.checked = true;
    });
});


let selectedSubject = null;
let selectedClass = null;

// Function to handle the click event on subject containers
function handleSubjectContainerClick(container) {
    selectedSubject = container.querySelector('h3').textContent;
    //console.log('Selected Subject:', selectedSubject);
}

// Function to handle the click event on class containers
function handleClassContainerClick(container) {
    selectedClass = container.querySelector('h3').textContent;
    //console.log('Selected Class:', selectedClass);
}

// Get all the containers under the box-info class for subjects
const subjectContainers = document.querySelectorAll('#page-1 .box-info li');

// Iterate over each subject container and add a click event listener
subjectContainers.forEach(container => {
    container.addEventListener('click', () => {
        handleSubjectContainerClick(container);
    });
});

// Get all the containers under the box-info class for classes
const classContainers = document.querySelectorAll('#page-2 .box-info li');

// Iterate over each class container and add a click event listener
classContainers.forEach(container => {
    container.addEventListener('click', () => {
        handleClassContainerClick(container);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const page1 = document.querySelector(".page-1");
    const page2 = document.querySelector(".page-2");
    const buttons = document.querySelectorAll(".page-1 .box-info .btn");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            page1.style.display = "none";
            page2.style.display = "block";
        });
    });
});


// JavaScript to handle button clicks and page navigation
function showPage(pageId) {
    window.location.href = '#' + pageId;
}

// Function to send accumulated data to the backend via a POST request
function sendCombinedDataToBackend() {
    if (selectedSubject && selectedClass) {
        const formData = {
            subject: selectedSubject,
            class: selectedClass
        };

        fetch('/dashboard', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                //console.log('Form submission successful');
                // Redirect to the student evaluation page after successful submission
                window.location.href = '/student-evaluate';
            } else {
                console.error('Form submission failed:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error during form submission:', error);
        });
    } else {
        console.error('Subject and Class must be selected');
    }
}

// Add event listener to the "Submit Selection" button
document.querySelector('.btn-submit').addEventListener('click', function() {
    //console.log('Submit button clicked!');
    // Ensure handleSubmitForm function is called when the button is clicked
    sendCombinedDataToBackend();
});



// Function to show page-2 and hide page-1
function showPage(pageId) {
    var pages = document.querySelectorAll('.page'); // Get all elements with class 'page'
    pages.forEach(function(page) {
        if (page.id === pageId) {
            page.style.display = 'block'; // Show the selected page
        } else {
            page.style.display = 'none'; // Hide other pages
        }
    });
}

// Call showPage('page-2') when page loads to initially display page-2
window.onload = function() {
    showPage('page-1');
};
