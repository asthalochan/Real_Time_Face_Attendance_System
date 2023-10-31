import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{
    'databaseURL' : "https://faceattendance-9ef75-default-rtdb.firebaseio.com/"
})


ref = db.reference('Users')

data = {
    "22MDSA50":
        {
            "name": "Modi",
            "branch": "DS",
            "batch": "2022-24",
            "total_attendance": 2,
            "last_attendance_time": "2023-09-06 00:54:34"
        },
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
    "22MDSA68":
        {
            "name": "DiptiRanjan",
            "branch": "DS",
            "batch": "2022-24",
            "total_attendance": 2,
            "last_attendance_time": "2023-09-06 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)
print("completed.....")


