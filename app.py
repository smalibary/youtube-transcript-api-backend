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
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        # Combine transcript into a single string
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return jsonify({"transcript": transcript_text})
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 404
    except VideoUnavailable:
        return jsonify({"error": "Video unavailable"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
