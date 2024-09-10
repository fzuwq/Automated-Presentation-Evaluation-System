import datetime
import json
import re
import logging
import os
from flask import Flask, jsonify, make_response, redirect, request, render_template, send_file, session, url_for, flash
from decision import evaluate_presentation
from vid_predict import process_video
from Audio_Extractor import extract_audio_from_video
from Speech_Sentiment_Analyzer import process_audio
from subject_pdf_generator import generate_pdf_report
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from gridfs import GridFS
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

# Secret key for session management
app.secret_key = os.getenv('SECRET_KEY')

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

# Dictionary to keep track of processed videos
processed_videos = {}

# Lock to prevent multiple processing of the same video
processing_lock = threading.Lock()

# Set to store video paths being processed
processing_videos = set()

# Variable to store the video file name
video_file_name = ""

# MongoDB connection initialization
uri = os.getenv('MONGODB_URI')
client = MongoClient(uri)

#User Database(Admin)
db = client['user_database']
users_collection = db['users']
    
#Student Database
db1 = client['student_database']
students_collection = db1['students']

#Student Result Database
db2 = client['result_database']
Biology = db2['Biology']
Chemistry = db2['Chemistry']
Commerce = db2['Commerce']
Computer = db2['Computer']
Language = db2['Language']
Literature = db2['Literature']
Geography = db2['Geography']
History = db2['History']
Mathematics = db2['Mathematics']
Physics = db2['Physics']

data = []

@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        
        # Check if the form is for registration or login
        action = request.form.get('action')
        if action == 'register':
            # Registration logic
            name = request.form['Name']
            username = request.form['Username']
            email = request.form['Email']
            mobile_number = request.form['Mobile Number']
            password = request.form['Password']

            # Check if the email already exists in the database
            existing_user = users_collection.find_one({'Email': email})

            if existing_user:
                return "Email already exists", 400
            
            else:
                # Hash the password before storing it in the database
                hashed_password = generate_password_hash(password)

                user_data = {
                    'Name': name,
                    'Username': username,
                    'Email': email,
                    'Mobile Number': mobile_number,
                    'Password': hashed_password
                }
            

            users_collection.insert_one(user_data)
            
            return "Registration Successful", 200  # Return success message with HTTP status code 200

        elif action == 'login':
            # Login logic
            email = request.form['Email']
            password = request.form['Password']
            

            user = users_collection.find_one({'Email': email})
            
            # Print session data for debugging
            #logging.debug('Session data after login: %s', session)

            if user and check_password_hash(user['Password'], password):
                # Convert the ObjectId to string before storing in session
                user['_id'] = str(user['_id'])
                session['user'] = user  # Store user data in session
                return redirect('/dashboard')
            else:
                return jsonify({'Success': False}), 401

    return render_template('homepage.html')

@app.route('/student-register', methods=['GET', 'POST'])
def student_register():
    
    if request.method == 'POST':
        
        # Extract form data from request
        name = request.form.get('Name')
        class_value = request.form.get('Class')
        section = request.form.get('Section')
        roll_number = request.form.get('Roll_Number')
        gender = request.form.get('Gender')
        
        # Check if the roll number already exists in the database
        existing_student = students_collection.find_one({'Roll_Number': roll_number})
        
        if existing_student:
                return "Student with the given Roll Number already exists.", 400
            
        else:
            # Prepare student data to insert into the database
            student_data = {
                'Name': name,
                'Class': class_value,
                'Section': section,
                'Roll_Number': roll_number,
                'Gender': gender
            }
            

        students_collection.insert_one(student_data)
            
        return "Registration Successful", 200  # Return success message with HTTP status code 200
        
        
    return render_template('stud_register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Check if the logout form is submitted
        if 'logout' in request.form:
            session.pop('user', None)  # Remove the user data from the session
            session.clear()  # Clear all session data
    
            # Expire the session cookie by setting its expiration time to the past
            response = redirect(url_for('home'))
            response.set_cookie('session', '', expires=0)  # Set cookie expiration to the past
            
            return response
        
        if request.is_json:
            data = request.get_json()
            if 'subject' in data and 'class' in data:
                selected_subject = data['subject']
                selected_class_temp = data['class']
                selected_class = re.sub(r'\D', '', selected_class_temp)
        
                # Process selected subject and class
                #print(f"Selected Subject: {selected_subject}, Class: {selected_class}")
        
                students = students_collection.find({'Class': selected_class})
                
                
                results = []
                
                for student in students:
                    print(student)
                    student_roll = student['Roll_Number']
                    
                    if student_roll:
                        subject_collection = db2[selected_subject]
                        if not subject_collection.find_one({'Roll_Number': student_roll}):
                            student_details = {
                                'Name': student['Name'],
                                'Class': student['Class'],
                                'Section': student['Section'],
                                'Roll_Number': student['Roll_Number'],
                                'Gender': student['Gender'],
                                'Subject': selected_subject,
                                'DOE': None,
                                'eval_status': False,
                                'Confidence Score': None,
                                'Remarks': None,
                                'Report': None
                            }
                            #print(student_details)
                            subject_collection.insert_one(student_details)
                    
                    
                temp = ({
                    'selected_subject': selected_subject,
                    'selected_class': selected_class
                })
                #print(temp)
                    
                # Store 'temp' in session for access after redirection
                session['temp'] = temp
            
                return redirect(url_for('student_evaluate'))
        


    
    # Check if the user is logged in (by checking the 'user' key in session)
    if 'user' in session:
        # User is logged in, render the dashboard template
        user = session['user']
        
        return render_template('dashboard_main.html', user=user)
    
    else:
        # User is not logged in, redirect to the homepage
        return redirect(url_for('home'))


@app.route('/student-evaluate', methods=['GET', 'POST'])
def student_evaluate():
    if request.method == 'POST':
        data = request.get_json()
        
        if 'logout' in data and data['logout'] == True:
            # Perform logout actions
            session.pop('user', None)  # Remove the user data from the session
            session.clear()  # Clear all session data
            response = redirect(url_for('home'))  # Redirect to the home page
            response.set_cookie('session', '', expires=0)  # Expire the session cookie
            return response
        
        if 'action' in data:
            action = data['action']
            
            if action == 'liveStream' or action == 'fileUpload':
                selected_row_data = data.get('selectedRowData')
                
                if selected_row_data:
                    # Store selected_row_data in session based on the action
                    session['selected_row_data'] = selected_row_data

                    # Determine the redirect endpoint based on the action
                    if action == 'liveStream':
                        redirect_endpoint = '/live-stream'
                    elif action == 'fileUpload':
                        redirect_endpoint = '/file-upload'

                    return jsonify({'message': f'Data received for {action}', 'redirectEndpoint': redirect_endpoint}), 200
                else:
                    return jsonify({'error': 'Selected row data not provided'}), 400
            else:
                return jsonify({'error': 'Invalid action'}), 400
        else:
            return jsonify({'error': 'Invalid request'}), 400
    
    elif request.method == 'GET':
        if 'user' in session:
            # User is logged in, render the dashboard template
            user = session['user']
            try:
                # Retrieve 'temp' data from session
                temp = session.get('temp')
                if temp:
                    selected_subject = temp.get('selected_subject')
                    selected_class = temp.get('selected_class')
                    # Retrieve the results collection after processing    
                    subject_collection = db2[selected_subject]        
                    results = list(subject_collection.find({'Class': selected_class}))
                    #print(results)
                
                    #Convert ObjectId to string for each document
                    for result in results:
                        result['_id'] = str(result['_id'])
                        #print(result)

                    # Check if it's an AJAX request
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        # If it's an AJAX request, return JSON data
                        response_data = {
                            'selected_subject': selected_subject,
                            'selected_class': selected_class,
                            'results': results
                        }
                        return jsonify(response_data), 200
                    
                    

                    # If it's a regular GET request, render the dashboard_result.html template
                    return render_template('dashboard_result.html',
                                           selected_subject=selected_subject,
                                           selected_class=selected_class,
                                           results=results, user=user)
                else:
                    return jsonify({'error': 'Data not found in session'}), 404  # Session data not found
            except KeyError:
                return jsonify({'error': 'Data retrieval error'}), 500  # Error retrieving session data
        else:
            # User is not logged in, redirect to the home page or login page
            return redirect(url_for('home'))  # Redirect to the home page

  
@app.route('/download-report', methods=['GET'])
def download_report():
    student_id = request.args.get('studentId')
    #print(student_id)
    
    if student_id:
        # Retrieve the PDF report file from the database based on the student ID
        fs = GridFS(db2)
        report_file = fs.find_one({'student_id': ObjectId(student_id)})
        
        if report_file:
           # Serve the PDF report file for download
            pdf_data = fs.get(report_file._id).read()  # Read the PDF file content
            response = make_response(pdf_data)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename=report.pdf'
            return response
        else:
            return jsonify({'error': 'PDF report not found'}), 404
    else:
        return jsonify({'error': 'Invalid request'}), 400 


@app.route('/live-stream', methods=['GET', 'POST'])
def live_stream():
    if 'user' in session:
        user = session['user']    
        # Retrieve selected_row_data from session using the correct key
        selected_row_data = session.get('selected_row_data', {})
        #print('Session for live-stream:', selected_row_data)
        
        return render_template("live_stream.html", user=user, selected_row_data=selected_row_data)
    
    else:
        # User is not logged in, redirect to the homepage
        return redirect(url_for('home'))

@app.route('/file-upload', methods=['GET', 'POST'])
def file_upload():
    if 'user' in session:
        user = session['user']
        
        # Retrieve selected_row_data from session
        selected_row_data = session.get('selected_row_data', {})
        #print('session for file-upload: ',selected_row_data)
        
        if request.method == 'POST' and 'file' in request.files:
            video_file = request.files['file']
            video_path = 'uploaded_video.mp4'
            video_file.save(video_path)

            # Log the execution
            logging.debug('File saved at path: %s', video_path)

            # Redirect to /processing if video not processed yet
            if video_path not in processed_videos:
                 return redirect('/processing?video_path=' + video_path)

        return render_template('file_upload.html', user=user)
    
    else:
        # User is not logged in, redirect to the homepage
        return redirect(url_for('home'))
    

@app.route('/processing')
def processing():
    video_path = request.args.get('video_path')
    selected_row_data = session.get('selected_row_data', {})  # Initialize selected_row_data
    #print("session data for processing:", selected_row_data)
    if video_path not in processing_videos:

        # Start processing only if the video is not being processed
        process_thread = threading.Thread(target=process_uploaded_video, args=(video_path, selected_row_data,))
        process_thread.start()
        processing_videos.add(video_path)
    
    return render_template('processing.html', video_path=video_path, selected_row_data=selected_row_data)

def process_uploaded_video(video_path, selected_row_data):
    output_audio = 'Audio.wav'

    try:
        # Acquire the lock to prevent multiple threads from processing the same video
        with processing_lock:
            # Process video and audio
            selected_row_data = selected_row_data
            
            video_result = process_video(video_path)
            extract_audio_from_video(video_path=video_path, output_audio_path=output_audio)
            audio_result = process_audio('Audio.wav')

            video_result = json.loads(video_result)
            audio_result = json.loads(audio_result)

            # Now you can access keys of the dictionary
            emotion = video_result['video_result']['dominant_emotion']
            vader_sentiment = audio_result['final_vader_sentiment']
            speech_rate = audio_result['speech_rate']
            frequency = audio_result['frequency']
            amplitude = audio_result['average_amplitude']
            gender = selected_row_data['Gender'].lower()
            #print(gender)

            # Evaluate presentation
            presentation_result = evaluate_presentation(emotion, vader_sentiment, speech_rate, frequency, gender, amplitude)
            
            #print(presentation_result)

            # Store the presentation result
            processed_videos[video_path] = presentation_result
            
    except Exception as e:
        logging.error(f"Error processing video {video_path}: {e}")

    finally:
        # Remove the video from the processing set even if an exception occurs
        processing_videos.discard(video_path)

    return

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Retrieve selected_row_data from session
        selected_row_data = session.get('selected_row_data', {})
        #print("Session data for result:", selected_row_data)
        
        # Extract required information from selected_row_data
        try:
            selected_class = selected_row_data['Class']
            roll_number = selected_row_data['Roll_Number']
            subject = selected_row_data['Subject']
        except KeyError as e:
            return f"KeyError: Missing key in selected_row_data: {e}", 400
        
        # Access the appropriate collection in the database
        subject_collection = db2[subject]
        
        # Retrieve the student document based on class and roll number
        student = subject_collection.find_one({'Class': selected_class, 'Roll_Number': roll_number})
        #print(student)
        
        if student:
                
            # Retrieve data from the POST request
            data = request.get_json()
            confidence_score = data.get('confidenceScore')
            #print(confidence_score)
            remarks = data.get('remarks')
            #print(remarks)
            emotionScore = data.get('emotionScore')
            #print(emotionScore)
            sentimentScore = data.get('sentimentScore')
            #print(sentimentScore)
            speechRateScore = data.get('speechRateScore')
            #print(speechRateScore)
            frequencyScore = data.get('frequencyScore')
            #print(frequencyScore)
            amplitudeScore = data.get('amplitudeScore')
            #print(amplitudeScore)

            # Update student document with evaluation results
            student['DOE'] = datetime.date.today().isoformat()
            student['eval_status'] = True  # Assuming evaluation is complete
            student['Confidence Score'] = confidence_score
            student['Remarks'] = remarks
            
            
            # Generate PDF report for the student
            pdf_data = {
                'Student Name': student['Name'],
                'Class': student['Class'],
                'Section': student['Section'],
                'Roll Number': student['Roll_Number'],
                'Gender': student['Gender'],
                'Subject': subject,
                'Confidence Score': confidence_score,
                'Remarks': remarks,
                'Evaluation Date': datetime.date.today().isoformat(),
                'Emotion Score': emotionScore,
                'Speech Sentiment Score': sentimentScore,
                'Speech Rate Score': speechRateScore,
                'Vocal Frequency Score': frequencyScore,
                'Vocal Amplitude Score': amplitudeScore
            }
            
            # Call the function to generate the PDF report
            pdf_bytes = generate_pdf_report(pdf_data)

            if pdf_bytes:
                # Save the generated PDF report to MongoDB GridFS
                fs = GridFS(db2)
                report_id = fs.put(pdf_bytes, filename=f"{subject}_{student['Name']}_{student['Class']}_{student['Section']}_Report.pdf", student_id=student['_id'])

                # Update student document with the report ID
                student['Report'] = str(report_id)
                subject_collection.update_one({'_id': student['_id']}, {'$set': student})
                

                # Clear selected_row_data from session after processing
                session.pop('selected_row_data', None)
            
                # Remove the temp data from the session
                #session.pop('temp', None) 
            
                # Remove the current video entry from processed_videos
                video_path = request.args.get('video_path')
                if video_path in processed_videos:
                    del processed_videos[video_path] 
            

            # Return a response (optional)
            return jsonify({'message': 'Result updated successfully', 'report_id': str(report_id)}), 200
        
        else:
            return "Student not found in the database", 404
    
    # Handle GET request (rendering the result.html template)
    video_path = request.args.get('video_path')
    if video_path in processed_videos:
        presentation_result = processed_videos[video_path]
        return render_template('result.html', presentation_result=presentation_result)
    
    else:
        return redirect('/file-upload')

    
@app.route('/check-result')
def check_result():
    video_path = request.args.get('video_path')
    if video_path in processed_videos:
        # Check if processing for this video is complete
        if video_path not in processing_videos:
            return jsonify({'result_available': True})
        else:
            return jsonify({'result_available': False, 'message': 'Video processing in progress'})
    else:
        return jsonify({'result_available': False, 'message': 'Video not processed'})
    
@app.route('/clear-videos', methods=['POST'])
def clear_videos():
    global processed_videos
    global processing_videos

    # Clear processed videos dictionary
    processed_videos = {}

    # Clear processing videos set
    processing_videos.clear()

    return jsonify({'message': 'Videos data cleared successfully'}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
