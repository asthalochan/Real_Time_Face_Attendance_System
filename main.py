import os
import pickle
import face_recognition
import cv2
import cvzone
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{
    'databaseURL' : "https://faceattendance-9ef75-default-rtdb.firebaseio.com/",
    'storageBucket' : "faceattendance-9ef75.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 558)  # Set the width of the webcam capture to match the background
cap.set(4, 345)  # Set the height of the webcam capture to match the background

# Load the background image
imgBackground = cv2.imread('Resources/bg3.png')

#  mode img import
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModelist = list()
for path in modePathList:
    imgModelist.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModelist))


# load encoding file
print("loding encoded file")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("encoded file lodaed")

modeType = 0
counter = 0
id = -1
imgStudent = []
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    # Resize the webcam frame to match the dimensions of the background image
    img = cv2.resize(img, (558, 345))

    img2 = imgModelist[modeType]
    # Replace the background
    imgBackground[91:91 + img2.shape[0], 780:780 + img2.shape[1]] = img2
    imgBackground[219:564, 61:619] = img


    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            # print("matches", matches)
            # print("FaceDis", faceDis)

            matchIndex = np.argmin(faceDis)

            if matches [matchIndex]:
                # print("known Face detacted")
                # print(studentIds[matchIndex])
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 30 + x1, 172 + y1, x2 - x1, y2 - y1
                imgBackground =cvzone.cornerRect(imgBackground,bbox,rt =0 )
                id = studentIds[matchIndex]



                if counter == 0:
                    # cvzone.putTextRect(imgBackground, "loading..", (275, 600))
                    # cv2.imshow("Face Attendance System", imgBackground)
                    # cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                studentInfo = db.reference(f'Users/{id}').get()
                print(studentInfo)

                # load img data
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                # update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondElapsed)

                if secondElapsed > 30:

                    # update the data
                    ref = db.reference(f'Users/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType = 3
                    counter = 0
                    img2 = imgModelist[modeType]
                    # Replace the background
                    imgBackground[91:91 + img2.shape[0], 780:780 + img2.shape[1]] = img2

            if modeType != 3:

                if 10<counter<20:
                    modeType = 2
                    img2 = imgModelist[modeType]
                    # Replace the background
                    imgBackground[91:91 + img2.shape[0], 780:780 + img2.shape[1]] = img2
                if counter <=10:
                    cv2.putText(imgBackground,str(studentInfo['total_attendance']),(1067,373),
                                cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),2)


                    cv2.putText(imgBackground, str(id), (873, 485),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (40,40, 40), 2)

                    cv2.putText(imgBackground, str(studentInfo['branch']), (840, 558),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1)
                    cv2.putText(imgBackground, str(studentInfo['batch']), (840, 578),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (365 - w) // 2

                    cv2.putText(imgBackground, str(studentInfo['name']), (780 + offset, 440),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (225, 225, 225), 2)


                    imgBackground[137:137+170,875:875+170] = imgStudent

                counter += 1

                if counter >=20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    img2 = imgModelist[modeType]
                    # Replace the background
                    imgBackground[91:91 + img2.shape[0], 780:780 + img2.shape[1]] = img2

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance System", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
