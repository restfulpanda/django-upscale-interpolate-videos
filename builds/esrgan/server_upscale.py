import os
import subprocess
import logging

from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """
    Handles the ping route.

    Returns:
        A tuple containing a JSON object with a "pong" message and an HTTP status code 200.
    """
    return jsonify({"message": "pong"}), 200


@app.route("/health", methods=["GET"])
def test():
    """
    Return a JSON response indicating that the Flask app is running.

    Returns:
        tuple: A tuple containing a JSON response with status and message, and the HTTP 200 status code.
    """
    return jsonify({"status": "ok", "message": "Flask app is running"}), 200


@app.route("/upscale", methods=["POST"])
def interpolate():
    """
    Performs video upscaling by invoking an external process.
    Extracts input and output paths, along with the scaling factor, from the request JSON.
    Validates input paths and uses a subprocess call to execute the upscale command.
    Returns a JSON response indicating success or detailing any encountered errors.
    """
    try:
        logger.info("Starting video upscale...")
        input_path = request.json.get("input_path")
        output_path = request.json.get("output_path")
        scale = request.json.get("scale", 2)

        sep = "/" if "/" in output_path else "\\"
        path_parts = output_path.split(sep)
        folder_path = sep.join(path_parts[:-1]) + sep
        file_name = path_parts[-1]
        new_file_name = file_name[:-4] + "_out" + file_name[-4:]

        file_path = folder_path + new_file_name

        if not input_path or not output_path:
            return jsonify({"error": "input_path and output_path are required"}), 400

        if not os.path.exists(input_path):
            return jsonify({"error": f"Input video {input_path} does not exist"}), 404

        command = [
            "python3",
            "/app/src/inference_realesrgan_video.py",
            "-i",
            input_path,
            "-o",
            folder_path,
            # "--ffmpeg_bin",
            # "/usr/bin/ffmpeg",
            "-n",
            "realesr-general-x4v3",
            # "--face_enhance",
            "-s",
            str(scale),
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.info(result)
            return jsonify({"error": result.stderr}), 500

        logger.info("Upscaling completed successfully.")
        return jsonify({"status": "success", "output": file_path})
    except Exception as e:
        logger.error(f"Captured error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
