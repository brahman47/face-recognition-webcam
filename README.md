# Real-Time Face Recognition App

## Description

This Python application uses a webcam to perform real-time face recognition. It detects faces in the video feed and compares them against a known face image (`Brahman.jpeg`) provided in the project directory. Recognized faces are highlighted with a bounding box and labeled with the name derived from the known image file.

## Requirements

*   Python 3.x
*   `face_recognition` library
*   `opencv-python` library (`cv2`)
*   `numpy` library
*   `face_recognition_models` (usually installed as a dependency of `face_recognition`)
*   A webcam connected to your computer.

**Note:** Installing the `face_recognition` library might require installing `dlib` first, which could have its own system dependencies (like CMake and potentially a C++ compiler). Please refer to the official installation guides for `dlib` and `face_recognition` for your specific operating system.

## Setup

1.  **Clone or download the project files.**
2.  **Install the required Python libraries:**
    ```bash
    pip install numpy opencv-python face_recognition
    ```
    *(Ensure you have the necessary prerequisites for `dlib` installed if needed.)*
3.  **Place the known face image:** Ensure the image file named `Brahman.jpeg` (containing the face you want to recognize) is present in the same directory as the `face_rec_app.py` script. The image should contain a clear, detectable face.

## Usage

1.  **Navigate to the project directory** in your terminal or command prompt.
2.  **Run the application:**
    ```bash
    python face_rec_app.py
    ```
3.  A window titled 'Video' will open, displaying the feed from your webcam.
4.  If the face from `Brahman.jpeg` is detected in the webcam feed, it will be enclosed in a red box and labeled "Brahman". Other detected faces will be labeled "Unknown".
5.  **Press the 'q' key** while the video window is active to stop the application and close the window.

## Notes

*   The application processes every 4th frame to improve performance.
*   The frame is resized to 1/4th of its original size for faster processing before face detection occurs.
*   Error messages will be printed to the console if the webcam cannot be opened, the known image is not found, or no face is detected in the known image.
