import tkinter as tk
import requests
import tempfile
import os
from tkinter import scrolledtext
import cv2
from PIL import Image, ImageTk

# Function to send story to Flask and receive video
def send_story():
    story = text_box.get("1.0", tk.END).strip()
    if not story:
        status_label.config(text="Please enter a story")
        return

    status_label.config(text="Processing...")
    try:
        response = requests.post("http://127.0.0.1:5000/process_story", json={"story": story}, stream=True)

        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            with open(temp_file.name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            status_label.config(text="Video received! Playing...")
            play_video(temp_file.name)
        else:
            status_label.config(text="Error: " + response.json().get("error", "Unknown error"))

    except Exception as e:
        status_label.config(text=f"Error: {e}")

# Function to play video in OpenCV window
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Generated Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Tkinter GUI setup
root = tk.Tk()
root.title("Story to Video")
root.geometry("500x400")

tk.Label(root, text="Enter your story:").pack(pady=5)
text_box = scrolledtext.ScrolledText(root, width=50, height=10)
text_box.pack(pady=5)

send_button = tk.Button(root, text="Generate Video", command=send_story)
send_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
