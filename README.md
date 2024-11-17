# RoadGuard: Real-Time Accident and Speed Detection System

This project is a real-time accident and speed detection system using computer vision and deep learning. The system detects accidents in video footage and sends an email alert with an attached image of the detected accident.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/RoadGuard.git
    cd RoadGuard
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your video file in the project directory and update the `cap = cv2.VideoCapture(r"your_video.mp4")` line in the code with your video file path.

2. Update the `sender_email`, `receiver_email`, and `password` variables with your email credentials.

3. Run the script:
    ```bash
    python main.py
    ```

## Features

- Real-time accident detection using YOLO model.
- Sends email alerts with an attached image of the detected accident.
- Configurable cooldown period to prevent multiple email alerts for the same accident.

## Configuration

- **Model**: The YOLO model is used for object detection. Update the model path if necessary.
    ```python
    model = YOLO(r"best (1).pt")
    ```

- **Classes**: The classes for detection are read from a text file.
    ```python
    df = open(r"coco1.txt", "r")
    classes = df.read().split("\n")
    ```

- **Email Configuration**: Update the email credentials and settings.
    ```python
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_email_password"
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
