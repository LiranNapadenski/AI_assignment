import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from BackEnd import text_to_video


def send_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter a story.")
        return
    
    video_path = text_to_video(text)
    show_video(video_path)

def show_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            video_label.config(image=img)
            video_label.image = img
            video_label.after(30, update_frame)
        else:
            cap.release()
    
    update_frame()

# Create GUI window
root = tk.Tk()
root.title("Text to Video Generator")
root.geometry("600x400")

# Text input field
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=10)

# Submit button
submit_button = tk.Button(root, text="Generate Video", command=send_text)
submit_button.pack(pady=5)

# Video display label
video_label = tk.Label(root)
video_label.pack()

root.mainloop()
