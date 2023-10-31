import pickle
import cv2
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-9ef75-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-9ef75.appspot.com"
})

# Importing student data into Firebase
ref = db.reference('Users')


# Function to import student data into Firebase
def importStudentData():
    student_id = student_id_entry.get()
    name = name_entry.get()
    branch = branch_entry.get()
    batch = batch_entry.get()

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
    messagebox.showinfo("Success", f"Student {name} data imported into Firebase.")
    clear_fields()


# Function to capture and display an image
def capture_image():
    student_id = student_id_entry.get()
    name = name_entry.get()

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

        # Display the captured image in a separate window
        display_captured_image(image_filename)

        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(image_filename)
        blob.upload_from_filename(image_filename)
        messagebox.showinfo("Success", f"Image for student {name} uploaded to Firebase Storage.")
    else:
        messagebox.showerror("Error", "Error capturing image.")


def display_captured_image(image_filename):
    # Create a new window for displaying the captured image
    image_window = tk.Toplevel(root)
    image_window.title("Captured Image")

    # Load the captured image using Pillow
    image = Image.open(image_filename)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(image_window, image=photo)
    image_label.photo = photo  # Keep a reference to the image to prevent it from being garbage collected
    image_label.pack()


# Function to clear entry fields
def clear_fields():
    student_id_entry.delete(0, 'end')
    name_entry.delete(0, 'end')
    branch_entry.delete(0, 'end')
    batch_entry.delete(0, 'end')


# Create the GUI window
root = tk.Tk()
root.title("Student Information and Image Capture")

# Labels and Entry fields for student information
student_id_label = tk.Label(root, text="Student ID:")
student_id_label.grid(row=0, column=0)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=0, column=1)

name_label = tk.Label(root, text="Name:")
name_label.grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

branch_label = tk.Label(root, text="Branch:")
branch_label.grid(row=2, column=0)
branch_entry = tk.Entry(root)
branch_entry.grid(row=2, column=1)

batch_label = tk.Label(root, text="Batch:")
batch_label.grid(row=3, column=0)
batch_entry = tk.Entry(root)
batch_entry.grid(row=3, column=1)

# Buttons for capturing image and importing data
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.grid(row=4, column=0, columnspan=2)

import_button = tk.Button(root, text="Import Data", command=importStudentData)
import_button.grid(row=5, column=0, columnspan=2)

# Button to clear entry fields
clear_button = tk.Button(root, text="Clear Fields", command=clear_fields)
clear_button.grid(row=6, column=0, columnspan=2)

root.mainloop()
