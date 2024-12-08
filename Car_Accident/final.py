import cv2
import cvzone
from ultralytics import YOLO
import os
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
from tracker import Tracker  # Your tracker module

path = r"Path of the directory where all the files are present"
os.chdir(path)


# Model
model = YOLO(r"best (1).pt")

# Data
df = open(r"coco1.txt", "r")
classes = df.read().split("\n")

cap = cv2.VideoCapture(r"cr.mp4")

# Store previous centers, timestamps, and speeds
prev_centers = {}
prev_times = {}

fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second of the video

# SMTP configuration for sending emails
sender_email = "sender gmail"
receiver_email = "receiver gmail"
password = ""  # For app password if 2-factor authentication is enabled

# Flag to track if an accident email has been sent
accident_email_sent = False
accident_detected_frames = 0
cooldown_limit = 30  # Number of frames to wait before resetting email flag

# Define a function to send email
def send_email_with_image(image_path):
    subject = "Accident Detected! ⚠️"
    body = "An accident has been detected. See the attached image for details."
    
    # Create email message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the image
    with open(image_path, "rb") as attachment:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename="accident_detected.jpg"')
        msg.attach(mime_base)

    # Connect to Gmail server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not load frame")
        break

    frame = cv2.resize(frame, (1020, 700))

    # Get the timestamp for the current frame (in seconds)
    results = model.predict(frame)

    accident_detected = False

    for result in results:
        for re in result.boxes:
            x1, y1, x2, y2 = map(int, re.xyxy[0])
            if int(re.cls[0]) < len(classes):
                name = classes[int(re.cls[0])]
                ww = x2 - x1
                hh = y2 - y1

                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cvzone.putTextRect(frame, name, (x1 + 10, y1 - 10), scale=1, thickness=1,
                                   colorR=(0, 255, 0), colorT=(0, 0, 0))

                # Check if an accident is detected
                if "Accident Detection !" in name:
                    accident_detected = True
                    # Highlight accident detection
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cvzone.putTextRect(frame, f"Accident Detected!", (x1 + 10, y1 - 10), scale=1,
                                       thickness=1, colorR=(0, 0, 255), colorT=(0, 0, 0))
                    
                    # Save the frame where accident is detected and send email if not already sent
                    if not accident_email_sent:
                        accident_image_path = "accident_detected.jpg"
                        cv2.imwrite(accident_image_path, frame)
                        send_email_with_image(accident_image_path)
                        accident_email_sent = True

    # If no accident is detected in the current frame, start cooldown for resetting email flag
    if not accident_detected:
        accident_detected_frames += 1
        if accident_detected_frames > cooldown_limit:
            accident_email_sent = False
            accident_detected_frames = 0
    else:
        accident_detected_frames = 0  # Reset frame counter if accident is detected

    cv2.imshow("RoadGuard Real-Time Accident and Speed Detection System", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
