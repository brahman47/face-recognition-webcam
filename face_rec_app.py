# Try importing models first (setuptools fixed the pkg_resources issue)
import face_recognition_models 
import face_recognition
import cv2
import numpy as np
import os

# Get the path to the known image
known_image_path = "Brahman.jpeg"
known_image_name = os.path.splitext(os.path.basename(known_image_path))[0] # Get name without extension

# Load the known image and get face encoding
try:
    known_image = face_recognition.load_image_file(known_image_path)
    # Check if any faces are found in the known image
    known_face_encodings_list = face_recognition.face_encodings(known_image)
    if not known_face_encodings_list:
        print(f"Error: No face found in the known image '{known_image_path}'. Please provide an image with a clear face.")
        exit()
    known_face_encoding = known_face_encodings_list[0]
    known_face_encodings = [known_face_encoding]
    known_face_names = [known_image_name]
except FileNotFoundError:
    print(f"Error: Known image file not found at '{known_image_path}'.")
    exit()
except Exception as e:
    print(f"Error loading known image or encoding face: {e}")
    exit()


# Initialize webcam
video_capture = cv2.VideoCapture(0) # 0 is usually the default webcam

if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting webcam feed. Press 'q' to quit.")

# Initialize variables for face detection
face_locations = []
face_encodings = []
face_names = []
frame_count = 0 # Initialize frame counter

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    if not ret:
        print("Error: Failed to grab frame from webcam.")
        break

    frame_count += 1 # Increment frame counter

    # Only process every 4th frame of video to save time
    if frame_count % 4 == 0:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # Use COLOR_BGR2RGB for OpenCV versions 3.2 and above
        if cv2.__version__.startswith('3') or cv2.__version__.startswith('4'):
             rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        else: # For older OpenCV versions
             rgb_small_frame = small_frame[:, :, ::-1] # Simple BGR to RGB conversion


        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    # Display the results (always display based on the last processed frame)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) # Red box

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1) # White text

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
print("Webcam feed stopped.")
