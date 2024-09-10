import random

def evaluate_presentation(emotion, vader_sentiment, speech_rate, frequency, gender, amplitude):
    def combine_outputs(emotion, vader_sentiment, speech_rate, frequency, gender, amplitude):
        emotion_score_val = emotion_score(emotion)
        
        vader_sentiment_score_val = vader_sentiment_score(vader_sentiment)
        
        speech_rate_score_val = speech_rate_score(speech_rate)
        
        frequency_score_val = vocal_frequency_score(frequency, gender)
        
        amplitude_score_val = amplitude_score(amplitude)
        
        combined_score = (emotion_score(emotion) + vader_sentiment_score(vader_sentiment) + speech_rate_score(speech_rate)
                              + vocal_frequency_score(frequency, gender) + amplitude_score(amplitude)) / 5
        
        # Collect all scores in a dictionary
        scores = {
            'Emotion Score': emotion_score_val,
            'Vader Sentiment Score': vader_sentiment_score_val,
            'Speech Rate Score': speech_rate_score_val,
            'Frequency Score': frequency_score_val,
            'Amplitude Score': amplitude_score_val,
            'Combined Score': combined_score
        }
        
        return scores
    

    def assign_score(combined_score):
        # Assign a score on a 10-point scale based on the combined score
        score = int(round(combined_score * 10))
        return score

    def emotion_score(emotion):
        # Assign scores to emotions based on the specified order
        emotion_scores = {'happiness': random.uniform(0.8, 1.0), 'neutral': random.uniform(0.7, 0.9), 
                          'surprise': random.uniform(0.6, 0.7), 'fear': random.uniform(0.5, 0.6), 
                          'sadness': random.uniform(0.4, 0.5), 'anger': random.uniform(0.2, 0.4), 
                          'disgust': random.uniform(0.1, 0.3)}
        return emotion_scores.get(emotion)

    def vader_sentiment_score(vader_sentiment):
        # Assign scores to VADER sentiment
        if vader_sentiment == 'positive':
            return random.uniform(0.7, 1.0)
        elif vader_sentiment == 'negative':
            return random.uniform(0.2, 0.6)
        else:
            return random.uniform(0.6, 0.8) #For Neutral 

    def speech_rate_score(speech_rate):
        # Assign scores to speech rate categories
        speech_rate_scores = {'Very Fast': random.uniform(0.6, 0.8), 'Fast': random.uniform(0.7, 0.9), 
                              'Moderate': random.uniform(0.7, 1.0), 'Slow': random.uniform(0.4, 0.6), 
                              'Very Slow': random.uniform(0.2, 0.4)}
        return speech_rate_scores.get(speech_rate)

    def vocal_frequency_score(frequency, gender):
        # Define the standard vocal frequency ranges for male and female speakers
        male_frequency_range = [(85, 180), (165, 255)]  # (lower range, higher range)
        female_frequency_range = [(165, 255), (250, 500)]  # (lower range, higher range)

        # Determine the appropriate frequency ranges based on gender
        if gender == 'male':
            frequency_ranges = male_frequency_range
        elif gender == 'female':
            frequency_ranges = female_frequency_range
        else:
            raise ValueError("Invalid gender. Valid options are 'male' or 'female'.")

        # Check if the frequency falls within any of the standard ranges
        for freq_range in frequency_ranges:
            if frequency >= freq_range[0] and frequency <= freq_range[1]:
                # If within the range, assign a higher score
                return random.uniform(0.7, 1.0)

        # If outside all standard ranges, assign a lower score
        return random.uniform(0.6, 0.7)

    def amplitude_score(amplitude):
        # Define thresholds for amplitude ranges
        low_threshold = -0.1
        high_threshold = 0.1

        # Assign scores based on amplitude ranges
        if amplitude < low_threshold:
            return random.uniform(0.2, 0.4)
        elif low_threshold <= amplitude < high_threshold:
            return random.uniform(0.5, 0.7)
        elif amplitude > high_threshold:
            return random.uniform(0.6, 0.8)

    # Combine outputs to get individual scores and combined score
    scores = combine_outputs(emotion, vader_sentiment, speech_rate, frequency, gender, amplitude)
    
    # Assign a score based on the combined score
    score = assign_score(scores['Combined Score'])

    # Determine remarks based on confidence score
    if score >= 8:
        remarks = "Excellent Presentation Skills"
    elif score >= 7 and score < 8:
        remarks = "CONFIDENT.....WELL DONE"
    elif score == 6:
        remarks = "Good Presentation.....Keep working on it."
    elif score >= 4 and score < 6:
        remarks = "NOT UP TO THE MARK.....NEEDS IMPROVEMENT"
    else:
        remarks = "LACK OF CONFIDENCE.....NEEDS RE-EVALUATION"

    # Add confidence score and remarks to the scores dictionary
    scores.update({
        'Confidence Score': score,
        'Remarks': remarks
    })

    return scores

