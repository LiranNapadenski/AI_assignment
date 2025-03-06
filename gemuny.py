import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
from transformers import pipeline
from diffusers import DiffusionPipeline
from PIL import ImageFont, ImageDraw, Image
import os
import threading
import torch

# Backend (text_to_video)
text_pipe = pipeline("text2text-generation", model="google/flan-t5-large", device=0 if torch.cuda.is_available() else "cpu") #GPU or CPU
image_pipe = DiffusionPipeline.from_pretrained("stabilityai/sd-turbo")

if torch.cuda.is_available():
    image_pipe.to("cuda") #Move the image pipeline to GPU

output_video = "output_video.mp4"
fps = 1/3
width = 480
height = 800

def text_to_video(text, callback):
    def generate_video():
        prompt = """
            Split the following text into short sentences
            such that each sentence can be understood independently:\n\n
        """ + text
        captions = text_pipe(prompt, max_length=4096)[0]["generated_text"].split(". ")
        print(captions)

        images = []
        for caption in captions:
            try:
                image = image_pipe(caption.strip(), width=width, height=height).images[0]
                images.append(image)
            except Exception as e:
                print(f"Error generating image for caption '{caption}': {e}")
                callback(None)
                return

        if not images:
            callback(None)
            return

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        for i in range(len(images)):
            try:
                draw = ImageDraw.Draw(images[i])
                font = ImageFont.truetype("arial.ttf", 24)
                length = draw.textlength(captions[i], font=font)
                l, t, r, b = draw.textbbox(((width-length)/2, height*3/4), captions[i], font=font)
                draw.rectangle((l-5, t-5, r+5, b+5), fill=(0, 0, 0, 128))
                draw.text(((width-length)/2, height*3/4), captions[i], (255, 255, 255), font=font)
                video.write(np.asarray(images[i].convert('RGB'))[:, :, ::-1])
            except Exception as e:
                print(f"Error processing image {i}: {e}")
                video.release()
                if os.path.exists(output_video):
                    os.remove(output_video)
                callback(None)
                return

        video.release()
        callback(output_video)

    threading.Thread(target=generate_video).start()

# Frontend (GUI)
def send_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter a story.")
        return
    submit_button.config(state=tk.DISABLED)
    text_to_video(text, video_generated)

def video_generated(video_path):
    submit_button.config(state=tk.NORMAL)
    if video_path:
        show_video(video_path)
    else:
        messagebox.showerror("Error", "Failed to generate video.")

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

    if cap.isOpened():
        update_frame()
    else:
        messagebox.showerror("Error", "Could not open video file.")

# Create GUI window
root = tk.Tk()
root.title("Text to Video Generator")
root.geometry("600x600")

# Text input field
text_input = tk.Text(root, height=10, width=50)
text_input.pack(pady=10)

# Submit button
submit_button = tk.Button(root, text="Generate Video", command=send_text)
submit_button.pack(pady=5)

# Video display label
video_label = tk.Label(root)
video_label.pack()

root.mainloop()