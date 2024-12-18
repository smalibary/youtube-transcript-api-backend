from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable

app = Flask(__name__)

@app.route("/getTranscript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("videoID")
    if not video_id:
        return jsonify({"error": "Missing videoID parameter"}), 400

    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = " ".join(entry["text"] for entry in transcript)
        return jsonify({"transcript": transcript_text})
    except TranscriptsDisabled:
        app.logger.error(f"Transcripts are disabled for video ID: {video_id}")
        return jsonify({"error": "Transcripts are disabled for this video"}), 404
    except VideoUnavailable:
        app.logger.error(f"Video unavailable for video ID: {video_id}")
        return jsonify({"error": "Video unavailable"}), 404
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
