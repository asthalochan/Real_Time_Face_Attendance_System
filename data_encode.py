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
data = {
    "22MDSA50": {
        "name": "Modi",
        "branch": "DS",
        "batch": "2022-24",
        "total_attendance": 2,
        "last_attendance_time": "2023-09-06 00:54:34"
    },
    # Add more student data here...
    "22MDSA51":
        {
            "name": "Virat",
            "branch": "vls",
            "batch": "2022-24",
            "total_attendance": 1,
            "last_attendance_time": "2023-09-06 00:54:34"
        },
    "22MDSA52":
        {
            "name": "Dropodi",
            "branch": "Cli",
            "batch": "2022-24",
            "total_attendance": 2,
            "last_attendance_time": "2023-09-06 00:54:34"
        },
    "22MDSA53":
        {
            "name": "Astha",
            "branch": "DS",
            "batch": "2022-24",
            "total_attendance": 3,
            "last_attendance_time": "2023-09-06 00:54:34"
        },
    "22MDSA69":
        {
            "name": "DiptiRanjan",
            "branch": "DS",
            "batch": "2022-24",
            "total_attendance": 2,
            "last_attendance_time": "2023-09-06 00:54:34"
        },

}

for key, value in data.items():
    ref.child(key).set(value)
print("Student data imported into Firebase.")

# Importing student images
folderPath = 'Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentIds = []

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

# Function to find face encodings
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding completed")

# Save face encodings to a file
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File saved.")
