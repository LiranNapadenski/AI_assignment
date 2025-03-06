import tkinter as tk
from tkinter import messagebox, ttk
import cv2
from PIL import Image, ImageTk
import threading
from BackEnd import text_to_video  # Ensure the function is correctly imported from the backend module

# Function to send text for video generation
def send_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter a story.")
        return
    
    submit_button.config(state=tk.DISABLED)
    progress_label.config(text="Generating video...")
    progress_bar.start()

    # Run video generation in a separate thread
    threading.Thread(target=generate_video, args=(text,)).start()

# Function to generate the video in the background
def generate_video(text):
    try:
        video_path = text_to_video(text)  # Replace with actual function call from the backend
        # Safely call the video generated callback
        root.after(0, video_generated, video_path, None)
    except Exception as e:
        root.after(0, video_generated, None, str(e))

# Callback function when video is generated
def video_generated(video_path, error_message):
    submit_button.config(state=tk.NORMAL)
    progress_label.config(text="")
    progress_bar.stop()

    if video_path:
        show_video(video_path)
    else:
        messagebox.showerror("Error", f"Video generation failed: {error_message}")

# Function to play video in GUI
def show_video(video_path):
    global cap
    if 'cap' in globals() and cap.isOpened():
        cap.release()  # Close any existing video

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 30  # Adjust frame rate dynamically

    def update_frame():
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                video_label.config(image=img)
                video_label.image = img
                video_label.after(delay, update_frame)
            else:
                cap.release()

    update_frame()

# Create GUI window
root = tk.Tk()
root.title("Text-to-Video Generator")
root.geometry("800x600")

# Layout Configuration
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# Text Input Field
text_input = tk.Text(frame, height=7, width=70, font=("Arial", 12))
text_input.pack(pady=10, padx=10, fill=tk.X, expand=True)

# Submit Button
submit_button = tk.Button(frame, text="Generate Video", command=send_text, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
submit_button.pack(pady=5)

# Progress Bar & Label
progress_label = ttk.Label(frame, text="", font=("Arial", 10))
progress_label.pack()
progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=300)
progress_bar.pack(pady=5)

# Video Display Label
video_label = tk.Label(frame, bg="black")
video_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

root.mainloop()
