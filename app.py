from flask import Flask, request, jsonify
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable

app = Flask(__name__)

# Route to fetch video details and transcript
@app.route("/getVideoDetails", methods=["GET"])
def get_video_details():
    video_id = request.args.get("videoID")
    api_key = request.args.get("apiKey")

    if not video_id or not api_key:
        return jsonify({"error": "Missing videoID or apiKey parameter"}), 400

    try:
        # Step 1: Fetch Video Details from YouTube Data API
        details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        if not details_data["items"]:
            return jsonify({"error": "Video not found"}), 404

        video_data = details_data["items"][0]
        title = video_data["snippet"]["title"]
        publish_date = video_data["snippet"]["publishedAt"]
        views = video_data["statistics"].get("viewCount", "N/A")
        likes = video_data["statistics"].get("likeCount", "N/A")
        comments = video_data["statistics"].get("commentCount", "N/A")

        # Step 2: Fetch Transcript
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript_text = " ".join([entry["text"] for entry in transcript_data])
        except (TranscriptsDisabled, VideoUnavailable):
            transcript_text = "Transcripts are disabled for this video."

        # Combine Results
        result = {
            "videoID": video_id,
            "title": title,
            "publishDate": publish_date,
            "views": views,
            "likes": likes,
            "comments": comments,
            "transcript": transcript_text,
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
