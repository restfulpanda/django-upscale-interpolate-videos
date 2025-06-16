from flask import Flask, request, jsonify
import os
import subprocess
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

@app.route("/health", methods=["GET"])
def test():
    return jsonify({"status": "ok", "message": "Flask app is running"}), 200

@app.route("/upscale", methods=["POST"])
def interpolate():
    try:
        logger.info("Starting video upscale...")
        input_path = request.json.get("input_path")
        output_path = request.json.get("output_path")
        scale = request.json.get("multi", 2)

        if not input_path or not output_path:
            return jsonify({"error": "input_path and output_path are required"}), 400

        if not os.path.exists(input_path):
            return jsonify({"error": f"Input video {input_path} does not exist"}), 404

        command = [
            "python3",
            "/app/src/upscale_video.py",
            "-i",
            input_path,
            "-o",
            output_path,
            "-f",
            "/usr/bin/ffmpeg",
            "-m",
            "/app/models/",
            "-s",
            str(scale),
        ]
        
        # python3 /app/src/upscale_video.py -i /media/woman1.mp4 -o /media/woman1_x2.mp4 -f /usr/bin/ffmpeg -e "" -m /app/models/ -s 2

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.info(result)
            return jsonify({"error": result.stderr}), 500

        logger.info("Upscaling completed successfully.")
        return jsonify({"status": "success", "output": output_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
