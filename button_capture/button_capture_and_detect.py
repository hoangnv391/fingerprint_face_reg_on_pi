import RPi.GPIO as GPIO
import time

import face_recognition
import cv2
import numpy as np
import pickle

import fingerprint_handler


# Load pre-trained face encodings
print("[INFO] loading encodings...")
with open("../encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]
print("[INFO] load encodings complete")

# Initialize our variables
cv_scaler = 1 # this has to be a whole number

face_locations = []
face_encodings = []
face_names = []
frame_count = 0
start_time = time.time()
fps = 0

# Camera setup
print("Camera opening...")
# cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print("Camera ready")

detected = False

# Init states for GPIO pins
GPIO.setmode(GPIO.BCM)

button1_GPIO_pin = 26    # position follow on Raspberry Pi Pinout Mapping
GPIO.setup(button1_GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button2_GPIO_pin = 5    # position follow on Raspberry Pi Pinout Mapping
GPIO.setup(button2_GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def process_frame(frame):
    global face_locations, face_encodings, face_names

    # Resize the frame using cv_scaler to increase performance (less pixels processed, less time spent)
    resized_frame = cv2.resize(frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))

    # Convert the image from BGR to RGB colour space, the facial recognition library uses RGB, OpenCV uses BGR
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')

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
            
        # print(face_distances)
        # print(matches)
        # print(best_match_index)
        # print(known_face_names)
    
    return frame

def draw_results(frame):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)

    return frame

# Function to process button 1 - Capture image and detect
def button_1_processing():
    
    btn1_proc_str_time = time.time()
    while time.time() - btn1_proc_str_time < 9:
        print("Button 1 processing...")
        
        # Capture frame from Camera
        ret, frame = cap.read()
        
        # Display the frame
        cv2.imshow('Video capture', frame)
        
        global detected
        
        if not detected:        
            time.sleep(3)
        
            capture_frame = frame
            
            # Clean up
            cv2.destroyAllWindows()
            
            # Process the frame with the function
            processed_frame = process_frame(capture_frame)
            
            # Get the text and boxes to be drawn based on the processed frame
            display_frame = draw_results(processed_frame)
            
            # Calculate and update FPS
            current_fps = 0

            # Attach FPS counter to the text and boxes
            cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)    
            
            cv2.imshow('Detect result', display_frame)
            
            detected = True
        
        time.sleep(0.1)
    
    print("Stop button 1 processing")
    return

# Function to process button 2 - Read fingerprint sensor data and detect
def button_2_processing():
    fingerprint_info = {'id': 0, 'confidence': 0}
    btn2_proc_str_time = time.time()
    
    # while time.time() - btn2_proc_str_time < 5:
    fingerprint_handler.find_fingerprint(fingerprint_info)
    print(fingerprint_info)
        
        # time.sleep(0.1)
    
    print("Stop button 2 processing")
    return



# Main process

# Monitoring button state and process
try:
    while True:
        btn1_sts = GPIO.input(button1_GPIO_pin)
        btn2_sts = GPIO.input(button2_GPIO_pin)
        
        if not (btn1_sts == GPIO.HIGH):
            print("Button 1 captured - processing...")
            cv2.destroyAllWindows()
            button_1_processing()
            
        if not (btn2_sts == GPIO.HIGH):
            print("Button 2 captured - processing...")
            cv2.destroyAllWindows()
            button_2_processing()

except KeyboardInterrupt:
    print("Progam stopped!!!")
    
finally:
    GPIO.cleanup()
