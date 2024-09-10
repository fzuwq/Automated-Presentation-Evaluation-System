# Automated Presentation Evaluation System

## Overview

**The Automated Presentation Evaluation System is a web application designed to evaluate student presentations based on video and audio inputs. It provides features for user registration, login, student management, and detailed analysis of presentation videos. The system uses various deep learning models and APIs to process video and audio data, providing feedback on different aspects of the presentation such as emotions, speech rate, and sentiment.**


## Features

* **User Registration and Login:** Secure user registration and login functionality using hashed passwords.
* **Student Management:** Register and manage student details.
* **Video Processing:** Upload and process presentation videos to analyze emotions using a custom CNN model.
* **Audio Processing:** Extract and analyze audio from videos to evaluate speech sentiment, rate, and other parameters using Deepgram API and various Python libraries.
* **PDF Report Generation:** Generate detailed PDF reports for each student presentation evaluation.
* **Dashboard:** User dashboard to view and manage evaluations.
* **Session Management:** Secure session management for logged-in users.

## Technologies Used

* **Frontend:** HTML, CSS, JavaScript for the user interface.
* **Backend:** Flask Framework for server-side logic and API integration.(using Python)
* **Database:** MongoDB for storing user data, evaluations, and student details.
* **Video Processing:** OpenCV, FFmpeg
* **Audio Processing & Sentiment Analysis:** VaderSentiment, TextBlob, Librosa
* **PDF Generator:** ReportLab
* **Deep Learning:** TensorFlow + Keras for model training and inference
* **Deployment (Optional):** Docker, AWS or Render


## Installation

1. **Clone the repository:**

```
git clone https://github.com/your-username/Automated-Presentation-Evaluation-System.git
cd Automated-Presentation-Evaluation-System
```

2. **Install required dependencies:**

```
pip install -r requirements.txt
```

  **3. Set up MongoDB:**

* Create a MongoDB Atlas cluster or use a local MongoDB instance.
* Update the MongoDB connection URI in `app.py`

```
uri = "your-mongodb-connection-uri"
```

  **4. Set up Deepgram API:**

* Sign up for a Deepgram account and get your API key.
* Update the API key in `Speech_Sentiment_Analyzer.py`:

```
api_key = "your-deepgram-api-key"
```


5. **Run the application:**

```
python application.py
```

6. **Access the application:**

Open your web browser and navigate to `http://0.0.0.0:8000`.


## Usage

1. **User Registration and Login:**
   * Register as a new user or login with existing credentials.
2. **Student Management:**
   * Register new students with details like name, class, section, roll number, and gender.
3. **Video Upload and Processing:**
   * Upload presentation videos through the dashboard.
   * The system will process the video to analyze emotions and extract audio for further analysis.
4. **View Results and Download Reports:**
   * View the evaluation results on the dashboard.
   * Download detailed PDF reports for each presentation.



## License

This project is licensed under the Non-Commercial Use License. See the `LICENSE` file for details.


## Acknowledgements

* [Deepgram API](https://www.deepgram.com/)
* [VaderSentiment](https://github.com/cjhutto/vaderSentiment)
* [TextBlob](https://textblob.readthedocs.io/en/dev/)
* [Librosa](https://librosa.org/)
* [OpenCV](https://opencv.org/)
* [ONNX](https://onnx.ai/)


**Feel free to contact me if you have any questions or need further assistance. Happy coding!**
