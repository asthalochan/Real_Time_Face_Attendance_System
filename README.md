
# Real-Time Face Attendance System

The Real-Time Face Attendance System is a Python-based application that allows you to recognize and match faces from a database with the faces captured from a webcam. It records attendance with date and time and performs this action at specific intervals to create a real-time face attendance system. Firebase is used as the real-time database to store and manage attendance records.

## Features

- Face recognition and matching with database records.
- Date and time-stamped attendance records.
- Real-time attendance updates through Firebase.
- Customizable attendance interval.
- User-friendly graphical user interface (GUI).

## Requirements

Make sure you have the following requirements installed on your system:

- Python 3.x
- OpenCV (for webcam access and face recognition)
- Firebase (for real-time database)
- 

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/asthalochan/Real_Time_Face_Attendance_System.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Real_Time_Face_Attendance_System
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Update the Firebase configuration:
   - Go to the [Firebase Console](https://console.firebase.google.com/).
   - Create a new project or use an existing one.
   - Generate a Firebase Web App configuration.
   - Update the `serviceAccountKey.json` variable and credentials in  `databaseconfig.py` with your Firebase project's configuration.

## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. The GUI will appear. At active state to begin taking attendance.

3. The system will recognize faces from the webcam feed and match them with the database.

4. Attendance records will be updated in real-time on the Firebase database.

5. You can adjust the attendance interval.

## Project Structure



- `data_encode.py`: Script for encoding and adding faces to the database.
- `data_entry.py`: Manages data entry functions and interactions.
- `data_entry_gui.py`: Graphical User Interface for data entry.
- `databaseconfig.py`: Configuration file for database settings.
- `encode.py`: Script for encoding faces.
- `main.py`: The main application script.
- `requirements.txt`: List of required Python packages for this project.
- `serviceAccountKey.json`: Firebase service account key for database authentication.


## Acknowledgments

- [OpenCV](https://opencv.org/): Open Source Computer Vision Library.
- [Firebase](https://firebase.google.com/): Real-time database and authentication services.


## Contact

If you have any questions or suggestions, feel free to contact [Asthalochan Mohanta](mohantaastha@gmail.com).

Enjoy tracking attendance with the Real-Time Face Attendance System!
