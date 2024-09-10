document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('stream-elem');
    const startButton = document.getElementById('start-stream');
    const stopButton = document.getElementById('stop-media');
    const downloadButton = document.getElementById('download-video');
    const fileUploadButton = document.getElementById('file-upload');
    const timerElement = document.getElementById('timer');
    const statusMessage = document.getElementById('status-message'); // Element to display status message

    let mediaRecorder;
    let chunks = [];
    let startTime;
    let isRecording = false;
    let timerInterval;

    startButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    downloadButton.addEventListener('click', downloadRecording);
    fileUploadButton.addEventListener('click', redirectToUpload);

    videoElement.addEventListener('play', startTimer);
    videoElement.addEventListener('pause', stopTimer);

    function startRecording() {
        try {
            startTime = new Date();
            isRecording = true;

            // Show recording started status
            console.log('Recording Started');

            // Display recording started notification
            showNotification('Recording Started');

            // Hide download and file upload buttons
            downloadButton.style.display = 'none';
            fileUploadButton.style.display = 'none';

            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(stream => {
                    videoElement.srcObject = stream;
                    chunks = [];
                    mediaRecorder = new MediaRecorder(stream);
                    
                    mediaRecorder.ondataavailable = function(event) {
                        chunks.push(event.data);
                    };

                    mediaRecorder.start();
                })
                .catch(error => console.error('Error accessing media devices: ', error));
        } catch (err) {
            console.error('Error starting recording:', err);
        }
    }

    function stopRecording() {
        if (isRecording) {
            clearInterval(timerInterval);
            mediaRecorder.stop();
            isRecording = false;

            // Show recording stopped status
            console.log('Recording Stopped');

            // Display recording stopped notification
            showNotification('Recording Stopped');

            // Show download and file upload buttons
            downloadButton.style.display = 'block';
            fileUploadButton.style.display = 'block';
        
            videoElement.pause();
        }
    }

    function downloadRecording() {
        if (chunks.length > 0) {
            const blob = new Blob(chunks, { type: 'video/webm' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'recording.webm';
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            console.log('No recording to download.');
        }
    }

    function redirectToUpload() {
        window.location.href = '/file-upload';
    }

    function showNotification(message) {
        const notificationElement = document.createElement('div');
        notificationElement.classList.add('notification');
        notificationElement.textContent = message;
    
        // Set styles for notification
        notificationElement.style.position = 'absolute';
        notificationElement.style.bottom = '0';
        notificationElement.style.left = '50%';
        notificationElement.style.transform = 'translateX(-50%)';
        notificationElement.style.background = '#333';
        notificationElement.style.color = '#fff';
        notificationElement.style.padding = '10px';
        notificationElement.style.fontSize = '20px';
        notificationElement.style.fontWeight = 'bold';
        notificationElement.style.textAlign = 'center';
        notificationElement.style.width = '100%';
        notificationElement.style.zIndex = '9999';
    
        const container = videoElement.parentElement; // Get the container of the video element
        container.appendChild(notificationElement);
    
        setTimeout(() => {
            notificationElement.remove();
        }, 3000); // Remove notification after 3 seconds
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            const elapsedTime = Math.floor(videoElement.currentTime);
            const minutes = Math.floor(elapsedTime / 60);
            const seconds = elapsedTime % 60;
            timerElement.textContent = `${formatTime(minutes)}:${formatTime(seconds)}`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
    }

    function formatTime(time) {
        return time < 10 ? `0${time}` : time;
    }
});
