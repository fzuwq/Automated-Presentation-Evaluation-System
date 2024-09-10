document.addEventListener("DOMContentLoaded", function() {
    const tableBody = document.getElementById('tableBody');
    let selectedRowData = {}; // Variable to store selected row data

    // Function to update the table with provided data
    function updateTableWithData(results) {
        tableBody.innerHTML = ''; // Clear existing table rows

        results.forEach(student => {
            const newRow = document.createElement('tr');
            const statusClass = student.eval_status ? 'completed' : 'pending';

            newRow.innerHTML = `
                <td><input type="radio" name="studentSelection" value="${student.Roll_Number}" data-id='${JSON.stringify(student)}'></td>
                <td>${student.Name}</td>
                <td>${student.Gender}</td>
                <td>${student.DOE || '-'}</td>
                <td><span class="status ${statusClass}">${student.eval_status ? 'Completed' : 'Pending'}</span></td>
                <td>${student.Class}</td>
                <td>${student.Section}</td>
                <td>${student.Roll_Number}</td>
                <td>${student.Subject}</td>
                <td>${student['Confidence Score'] || '-'}</td>
                <td>${student.Remarks || '-'}</td>
                ${student.eval_status ? `<button class="download-btn" data-id="${student.Roll_Number}">Download</button>` : ''}</td>
            `;

            tableBody.appendChild(newRow);
        });

        // Event listener for download buttons after updating the table
const downloadButtons = document.querySelectorAll('.download-btn');
downloadButtons.forEach(button => {
    button.addEventListener('click', function() {
        const rollNumber = button.getAttribute('data-id');
        if (rollNumber) {
            // Retrieve the student data associated with the selected roll number
            const selectedStudent = results.find(student => student.Roll_Number === rollNumber);
            if (selectedStudent) {
                // Trigger download of the PDF report associated with the selected student
                downloadPDFReport(selectedStudent);
            } else {
                console.error('Student data not found for download');
            }
        }
    });
});

    }

    // Function to fetch data from server using AJAX
    function fetchData() {
        fetch('/student-evaluate', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Identify AJAX request
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.results && Array.isArray(data.results) && data.results.length > 0) {
                updateTableWithData(data.results); // Update table with retrieved data
            } else {
                console.error('No results found or invalid data');
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }

    // Call fetchData function when the page loads
    fetchData();

    // Function to download the PDF report for the selected student
function downloadPDFReport(student) {
    const { Name, Class, Section, Subject } = student;
    const fileName = `${Subject}_${Name}_${Class}_${Section}_Report.pdf`;

    // Initiate download by sending request to the server
    fetch(`/download-report?studentId=${student._id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/pdf'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to download PDF');
        }
        return response.blob();
    })
    .then(blob => {
        // Create a temporary anchor element to trigger the download
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error downloading PDF:', error);
    });
}

    // Event listener using event delegation to capture changes when radio buttons are clicked
    tableBody.addEventListener('change', function(event) {
        const selectedRadioButton = event.target;

        if (selectedRadioButton && selectedRadioButton.type === 'radio' && selectedRadioButton.checked) {
            const rowDataString = selectedRadioButton.getAttribute('data-id');

            if (rowDataString) {
                selectedRowData = JSON.parse(rowDataString);
                //console.log('Selected Row Data:', selectedRowData);
            } else {
                selectedRowData = {}; // Reset selectedRowData if no valid data-id attribute found
                console.log('No row selected');
            }
        }
    });

    function handleButtonClick(action) {
        const selectedRadioButton = document.querySelector('input[name="studentSelection"]:checked');
    
        if (selectedRadioButton) {
            const rowDataString = selectedRadioButton.getAttribute('data-id');
            if (rowDataString) {
                const selectedRowData = JSON.parse(rowDataString);
                //console.log('Selected Row Data:', selectedRowData);
    
                // Determine the redirect endpoint based on the action
                let redirectEndpoint;
                if (action === 'liveStream') {
                    redirectEndpoint = '/live-stream';
                } else if (action === 'fileUpload') {
                    redirectEndpoint = '/file-upload';
                }
    
                // Send the selected row data and action to /student-evaluate endpoint
                fetch('/student-evaluate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        action: action,
                        selectedRowData: selectedRowData,
                        requestType: 'buttonClickRequest'
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    //console.log('Response from /student-evaluate:', data);
                    // Redirect to the appropriate page based on the button action
                    if (redirectEndpoint) {
                        window.location.href = redirectEndpoint;
                    } else {
                        console.error('No redirect endpoint provided');
                    }
                })
                .catch(error => {
                    console.error('Error sending data to /student-evaluate:', error);
                });
            } else {
                console.log('No row selected');
            }
        } else {
            console.log('No row selected');
        }
    }

    const dashboardLink = document.getElementById('dashboard-link');

    if (dashboardLink) {
        dashboardLink.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default behavior of anchor tag

            // Redirect to /dashboard
            window.location.href = '/dashboard';
        });
    }

    // Event listener for the Live Stream button click
    const liveStreamButton = document.querySelector('.btn-submit');
    liveStreamButton.addEventListener('click', function(event) {
        event.preventDefault();
        handleButtonClick('liveStream');
    });

    // Event listener for the Video Upload button click
    const fileUploadButton = document.querySelector('.btn-upload');
    fileUploadButton.addEventListener('click', function(event) {
        event.preventDefault();
        handleButtonClick('fileUpload');
    });

    //console.log('Radio button setup complete. Listening for changes...');

    // TOGGLE SIDEBAR
    const menuBar = document.querySelector('#content nav .bx.bx-menu');
    const sidebar = document.getElementById('sidebar');

    menuBar.addEventListener('click', function () {
        sidebar.classList.toggle('hide');
    });

    // Function to handle logout action
    function logoutUser() {
        fetch('/student-evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ logout: true })
        })
        .then(response => {
            if (response.ok) {
                // Redirect to the login page upon successful logout
                window.location.href = '/'; 
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

    // Show/hide search form on mobile
    const searchButton = document.querySelector('#content nav form .form-input button');
    const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
    const searchForm = document.querySelector('#content nav form');

    searchButton.addEventListener('click', function (e) {
        if (window.innerWidth < 576) {
            e.preventDefault();
            searchForm.classList.toggle('show');
            if (searchForm.classList.contains('show')) {
                searchButtonIcon.classList.replace('bx-search', 'bx-x');
            } else {
                searchButtonIcon.classList.replace('bx-x', 'bx-search');
            }
        }
    });

    // Hide sidebar on smaller screens by default
    if (window.innerWidth > 768) {
        sidebar.classList.add('hide');
    }

    // Reset search button icon on window resize
    window.addEventListener('resize', function () {
        if (this.innerWidth > 576) {
            searchButtonIcon.classList.replace('bx-x', 'bx-search');
            searchForm.classList.remove('show');
        }
    });

    // Dark mode switch
    const switchMode = document.getElementById('switch-mode');
    switchMode.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark');
        } else {
            document.body.classList.remove('dark');
        }
    });
});
