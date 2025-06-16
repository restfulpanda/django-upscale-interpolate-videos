import os
import subprocess
import logging

from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """
    Return a JSON response indicating the health status of the server.

    Returns:
        tuple: A tuple containing a JSON response with a 'status' key set to 'healthy'
               and an HTTP status code 200.
    """
    return jsonify({"status": "healthy"}), 200


@app.route("/interpolate", methods=["POST"])
def interpolate():
    """
    Handles video interpolation by spawning a subprocess to run a video inference script.
    The function retrieves JSON data from the HTTP request containing the following keys:
        - "input_path": Path to the input video file.
        - "output_path": Path where the interpolated output video should be saved.
        - "multi": Optional scaling factor for interpolation (defaults to 2 if not provided).

    Returns:
        Flask response: A JSON response indicating the resultof the interpolation process,
        including HTTP status codes.
    """
    try:
        logger.info("Starting video interpolation...")

        input_path = request.json.get("input_path")
        output_path = request.json.get("output_path")
        scale = request.json.get("multi", 2)

        logger.info("Путь до файла: ", input_path)

        if not input_path or not output_path:
            return jsonify({"error": "input_path and output_path are required"}), 400

        if not os.path.exists(input_path):
            return jsonify({"error": f"Input video {input_path} does not exist"}), 404

        command = [
            "python3",
            "./inference_video.py",
            "--video",
            input_path,
            "--output",
            output_path,
            "--multi",
            str(scale),
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        logger.info("Interpolation completed successfully.")
        return jsonify({"status": "success", "output": output_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
