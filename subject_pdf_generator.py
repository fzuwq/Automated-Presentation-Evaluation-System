from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

def generate_pdf_report(student_data):
    # Extract student information
    name = student_data.get('Student Name', '')
    Class = student_data.get('Class', '')
    section = student_data.get('Section', '')
    roll_number = student_data.get('Roll Number', '')
    gender = student_data.get('Gender', '')
    subject = student_data.get('Subject', '')
    confidence_score = student_data.get('Confidence Score', '')
    remarks = student_data.get('Remarks', '')
    evaluation_date = student_data.get('Evaluation Date', '')
    emotion_score = student_data.get('Emotion Score', '')
    vader_sentiment_score = student_data.get('Speech Sentiment Score', '')
    speech_rate_score = student_data.get('Speech Rate Score', '')
    frequency_score = student_data.get('Vocal Frequency Score', '')
    amplitude_score = student_data.get('Vocal Amplitude Score', '')

    # Create a BytesIO object to store PDF content in memory
    pdf_buffer = BytesIO()

    # Create a new PDF document
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Set page margins and spacing
    top_margin = 50
    left_margin = 50
    line_height = 20

    # Load logo and get its dimensions
    logo = ImageReader('static/logo.jpg')
    logo_width = 80
    logo_height = 80

    # Draw the logo at the top left with spacing
    c.drawImage(logo, left_margin, letter[1] - top_margin - logo_height + 18 , width=logo_width, height=logo_height, preserveAspectRatio=True)

    # Calculate the starting x-coordinate for the heading
    heading_x = left_margin + logo_width + 35  # Add 20 units spacing between logo and heading

    # Draw the heading with underline
    c.setFont("Helvetica-Bold", 20)
    c.drawString(heading_x, letter[1] - top_margin - 20, "Automatic Presentation Evaluation")
    c.line(heading_x, letter[1] - top_margin - 25, heading_x + c.stringWidth("Automatic Presentation Evaluation", "Helvetica-Bold"), letter[1] - top_margin - 25)

    # Define content for the PDF
    content = [
        ("Student Name", name),
        ("Class", Class),
        ("Section", section),
        ("Roll Number", roll_number),
        ("Gender", gender),
        ("Subject", subject),
        ("Confidence Score", confidence_score),
        ("Remarks", remarks),
        ("Evaluation Date", evaluation_date)
    ]

    # Write content to the PDF
    current_y = letter[1] - top_margin - logo_height - 70  # Start below logo
    for parameter, value in content:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, current_y, f"{parameter}:")
        c.setFont("Helvetica", 12)
        c.drawString(left_margin + 120, current_y, str(value))
        current_y -= line_height  # Move to the next line

    # Add Individual Scores section
    c.setFont("Helvetica-Bold", 16)
    current_y -= 80 # Add space before Individual Scores
    c.drawString(left_margin, current_y, "Individual Scores")

    individual_scores = [
        ("Emotion Score", emotion_score),
        ("Speech Sentiment Score", vader_sentiment_score),
        ("Speech Rate Score", speech_rate_score),
        ("Vocal Frequency Score", frequency_score),
        ("Vocal Amplitude Score", amplitude_score)
    ]

    current_y -= line_height+10  # Move down for scores
    for parameter, value in individual_scores:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, current_y, f"{parameter}:")
        c.setFont("Helvetica", 12)
        c.drawString(left_margin + 155, current_y, str(value))
        current_y -= line_height  # Move to the next line

    # Save the PDF document content into the BytesIO buffer
    c.save()

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    # Return the PDF content as bytes
    return pdf_buffer.getvalue()

