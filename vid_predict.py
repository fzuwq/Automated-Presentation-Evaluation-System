import cv2
import onnxruntime as ort
import numpy as np
import json

def preprocess_input(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (48, 48))  # Resize to 48x48 as expected by the model
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=-1)  # Add channel dimension at the end
    img = np.expand_dims(img, axis=0)   # Add batch dimension
    return img

def process_video(video_path):
    # Load the ONNX model
    ort_session = ort.InferenceSession('Model/fer.onnx')

    cap = cv2.VideoCapture(video_path)

    # Initialize variables to store emotion percentages
    emotion_percentages = {'neutral': 0, 'happiness': 0, 'surprise': 0, 'sadness': 0, 'anger': 0, 'disgust': 0, 'fear': 0}

    # Initialize dictionary to store emotion counts
    emotion_counts = {emotion: 0 for emotion in emotion_percentages}
    emotions_list = list(emotion_counts.keys())

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face = preprocess_input(face)
            onnx_inputs = {ort_session.get_inputs()[0].name: face}
            onnx_outputs = ort_session.run(None, onnx_inputs)
            predictions = onnx_outputs[0][0]

            for i, emotion in enumerate(emotions_list):
                emotion_percentages[emotion] = predictions[i] * 100
                if emotion_percentages[emotion] > 40:  # consider only emotions with a confidence level above 40%
                    emotion_counts[emotion] += 1

    cap.release()

    # Initialize an empty list to store emotion-percentage pairs
    emotion_data = []

    # Iterate over the emotion percentages dictionary
    for emotion, percentage in emotion_percentages.items():
        # Append the emotion and percentage as a tuple to the list
        emotion_data.append((emotion, percentage))

    # Sort the emotion data based on percentage in descending order
    emotion_data.sort(key=lambda x: x[1], reverse=True)

    # Find the dominant emotion
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)

    # Create a dictionary containing the final emotion data
    final_emotion_data = {'dominant_emotion': dominant_emotion}
    
    # Wrap the final emotion data inside a dictionary with the key 'video_result'
    result = {'video_result': final_emotion_data}
    
    # Convert the dictionary to JSON format
    json_data_recorded = json.dumps(result)
    
    print(json_data_recorded)
    
    return json_data_recorded
