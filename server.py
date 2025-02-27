from flask import Flask, request, Response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

def Main(story):
    """Processes the story and generates a video file."""
    video_path = "output.mp4"  # Replace with your actual video generation logic
    time.sleep(2)  # Simulating video processing time
    return video_path

@app.route('/process_story', methods=['POST'])
def process_story():
    data = request.json
    story = data.get("story", "")

    if not story:
        return {"error": "No story provided"}, 400

    video_path = Main(story)
    return Response(open(video_path, "rb"), mimetype="video/mp4")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
