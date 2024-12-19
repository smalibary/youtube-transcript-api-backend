from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptNotFound

app = Flask(__name__)

@app.route("/get_transcript", methods=["POST"])
def get_transcript():
    try:
        # Parse the request body
        data = request.json
        video_id = data.get("video_id")
        if not video_id:
            return jsonify({"error": "Missing video_id"}), 400
        
        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item["text"] for item in transcript])
        return jsonify({"transcript": transcript_text}), 200
    except TranscriptNotFound:
        return jsonify({"error": "Transcript not found for this video."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Backend is running!", 200

if __name__ == "__main__":
    app.run(debug=True)
