import cv2
import pickle
import numpy as np
import os

# Initialize video capture
video = cv2.VideoCapture(0)

# Load pre-trained face detection model
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0

name = input("Enter Your Name: ")

# Create 'data' directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

while True:
    ret, frame = video.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
        
        i += 1
        
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    cv2.imshow("Frame", frame)
    
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# Load existing names or create new list
names_path = 'data/names.pkl'
if not os.path.exists(names_path):
    names = [name] * 100
else:
    with open(names_path, 'rb') as f:
        names = pickle.load(f)
    names.extend([name] * 100)

with open(names_path, 'wb') as f:
    pickle.dump(names, f)

# Load existing face data or create new list
faces_data_path = 'data/faces_data.pkl'
if not os.path.exists(faces_data_path):
    with open(faces_data_path, 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open(faces_data_path, 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open(faces_data_path, 'wb') as f:
        pickle.dump(faces, f)

print("Data saved successfully!")
