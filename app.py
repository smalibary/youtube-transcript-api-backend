from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptNotFound

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Backend is running!", 200

@app.route("/test_transcript", methods=["GET"])
def test_transcript():
    try:
        # Replace with a static test video ID for browser testing
        video_id = "8TWXL710ppY"  
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item["text"] for item in transcript])
        return jsonify({"video_id": video_id, "transcript": transcript_text}), 200
    except TranscriptNotFound:
        return jsonify({"error": "Transcript not found for this video."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
