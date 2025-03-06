import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
from transformers import pipeline
from diffusers import DiffusionPipeline
from PIL import ImageFont, ImageDraw, Image
import os
import torch

text_pipe = pipeline("text2text-generation", model="google/flan-t5-large")
image_pipe = DiffusionPipeline.from_pretrained("stabilityai/sd-turbo")

if torch.cuda.is_available():
    image_pipe.to("cuda") #Move the image pipeline to GPU

output_video = "output_video.mp4"
fps = 1/3
width = 480
height = 800

def text_to_video(text):
    prompt = """
        Split the following text into short sentences
        such that each sentence can be understood independently:\n\n
    """ + text
    captions = text_pipe(prompt, max_length=4096)[0]["generated_text"].split(". ")
    print(captions)

    images = list(map(lambda x: image_pipe(x.strip(), width=width, height=height).images[0], captions))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for i in range(len(images)):
        draw = ImageDraw.Draw(images[i])
        font = ImageFont.truetype("arial.ttf", 20)
        length = draw.textlength(captions[i], font=font)
        l, t, r, b = draw.textbbox(((width-length)/2, height*3/4), captions[i], font=font)
        draw.rectangle((l-5, t-5, r+5, b+5), fill=(0, 0, 0))
        draw.text(((width-length)/2, height*3/4), captions[i], (255, 255, 255), font=font)
        video.write(np.asarray(images[i].convert('RGB'))[:, :, ::-1])
    video.release()

    return output_video
