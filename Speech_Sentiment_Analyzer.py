from fastapi import HTTPException
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import requests
import json
import librosa
import numpy as np

def process_audio(audio_path):
    # Replace with the new Deepgram API Key
    api_key = "9c912c7d731d3e63f55517dd608a031937bb1d81"

    # Specifying the Deepgram API endpoint
    api_url = "https://api.deepgram.com/v1/listen"

    with open(audio_path, "rb") as file:
        buffer_data = file.read()
        try:
            # Specify Deepgram headers
            headers = {
                "accept": "application/json",
                "Authorization": f"Token {api_key}"
            }

            # Prepare the payload for Deepgram API
            payload = buffer_data

            # Send the POST request to Deepgram API for transcription
            response = requests.post(api_url, headers=headers, data=payload)

            # Check if the request was successful (HTTP status code 200)
            response.raise_for_status()

            # Extract the transcript
            result = response.json()
            transcript = result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")

            print("transcript:", transcript)

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Request to Deepgram API failed: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    # Load the audio file
    y, sr = librosa.load(audio_path)

    # Perform sentiment analysis using VADER
    analyzer = SentimentIntensityAnalyzer()
    vader_sentiment = analyzer.polarity_scores(transcript)

    # Perform sentiment analysis using TextBlob
    textblob_sentiment = TextBlob(transcript).sentiment

    # Calculate cumulative sentiment scores
    final_vader_sentiment = vader_sentiment['compound']
    final_textblob_sentiment = textblob_sentiment.polarity

    # Calculate the duration of the audio file
    audio_duration = librosa.get_duration(y=y, sr=sr)

    # Calculate speech rate (words per minute)
    words = transcript.split()
    word_count = len(words)
    speech_rate = word_count / (audio_duration / 60)  # Duration converted to minutes

    # Calculate pitch using the YIN algorithm
    frequency = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    # Calculate the average amplitude
    average_amplitude = np.mean(np.abs(y))

    # Determine final sentiment based on all parameters
    if final_vader_sentiment >= 0.05:
        final_sentiment = "Positive"
    elif final_vader_sentiment <= -0.05:
        final_sentiment = "Negative"
    else:
        final_sentiment = "Neutral"
        
    # Print pace of the speech
    if speech_rate > 200:
        audio_pace = "Very Fast"
    elif speech_rate > 150:
        audio_pace = "Fast"
    elif speech_rate > 100:
        audio_pace = "Moderate"
    elif speech_rate > 50:
        audio_pace = "Slow"
    else:
        audio_pace = "Very Slow"
        
    # Create a dictionary containing the values to be sent
    audio_data = {
        'final_vader_sentiment': final_sentiment,
        'speech_rate': audio_pace,
        'frequency': float(np.mean(frequency)),  # Convert to float
        'average_amplitude': float(average_amplitude)  # Convert to float
    }
 
    # Convert the dictionary to JSON format
    json_data_audio = json.dumps(audio_data)
    print(json_data_audio)

    return json_data_audio
