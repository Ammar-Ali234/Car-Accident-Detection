# RoadGuard: Real-Time Accident and Speed Detection System

This project is a computer vision-based solution that uses YOLO for detecting accidents in real-time video streams. It highlights detected accidents on the video frames and notifies users via email with an attached image of the detected event.

---

## Features

- **Accident Detection:** Identifies accidents in real-time using YOLOv8.
- **Visual Feedback:** Highlights detected objects and accidents with bounding boxes in the video feed.
- **Email Notifications:** Sends an alert email with an attached image of the accident scene when an accident is detected.
- **Cool-down Mechanism:** Prevents duplicate emails by implementing a cooldown frame-based mechanism.

---

## Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- OpenCV
- cvzone
- numpy
- ultralytics (for YOLO)
- smtplib (standard library)
- ssl (standard library)

Install the required Python libraries with:
```bash
pip install opencv-python cvzone numpy ultralytics
