import pickle
import cv2
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-9ef75-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-9ef75.appspot.com"
})

# Importing student data into Firebase
ref = db.reference('Users')

# Function to import student data into Firebase
def importStudentData(student_id, name, branch, batch):
    data = {
        student_id: {
            "name": name,
            "branch": branch,
            "batch": batch,
            "total_attendance": 0,
            "last_attendance_time": "2023-09-06 00:54:34"
        }
    }
    ref.child(student_id).set(data[student_id])
    print(f"Student {name} data imported into Firebase.")

while True:
    student_id = input("Enter student ID (e.g., 22MDSA50): ")
    name = input("Enter student name: ")
    branch = input("Enter branch: ")
    batch = input("Enter batch: ")

    importStudentData(student_id, name, branch, batch)

    # Take a picture from the user
    capture = cv2.VideoCapture(0)  # Use 0 for the default camera
    ret, frame = capture.read()
    if ret:
        # Resize the captured image to 170x170
        frame = cv2.resize(frame, (170, 170))
        # Save the captured image in PNG format with the student's ID as the filename
        image_filename = f'Images/{student_id}.png'
        cv2.imwrite(image_filename, frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        capture.release()

        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(image_filename)
        blob.upload_from_filename(image_filename)
        print(f"Image for student {name} uploaded to Firebase Storage.")
    else:
        print("Error capturing image.")

    continue_input = input("Do you want to input more students? (yes/no): ")
    if continue_input.lower() != "yes":
        break

# Function to find face encodings
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

# Importing student images
folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

print("Encoding Started....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding completed")

# Save face encodings to a file
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File saved.")
