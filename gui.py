import tkinter as tk
import requests

# Function to send data to Flask backend
def send_message():
    message = entry.get()
    try:
        response = requests.post("http://127.0.0.1:5000/data", json={"message": message})
        result = response.json()["response"]
        response_label.config(text=f"Response: {result}")
    except Exception as e:
        response_label.config(text=f"Error: {e}")

# Create Tkinter window
root = tk.Tk()
root.title("Flask + Tkinter GUI")
root.geometry("400x250")

# Create input field and button
tk.Label(root, text="Enter a message:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=10)

# Response label
response_label = tk.Label(root, text="Response: ", wraplength=300)
response_label.pack(pady=10)

root.mainloop()
