from flask import Flask, request, jsonify
import os
import subprocess
import logging
from pathlib import Path

app = Flask(__name__)

# Пути для volumes
VIDEO_STORAGE_DIR = Path(__file__).resolve().parent.parent.joinpath("media/")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@app.route("/upscale", methods=["POST"])
def interpolate():
    try:
        logger.info("Starting video upscale...")
        # Получение данных из запроса
        input_path = request.json.get("input_path")
        output_path = request.json.get("output_path")
        scale = request.json.get("multi", 2)  # Опциональный параметр

        if not input_path or not output_path:
            return jsonify({"error": "input_path and output_path are required"}), 400

        if not os.path.exists(input_path):
            return jsonify({"error": f"Input video {input_path} does not exist"}), 404

        # Команда для запуска inference
        command = [
            "python3",
            ".\src\upscale_video.py",
            "-i",
            input_path,
            "-o",
            output_path,
            "-f",
            "/usr/bin/ffmpeg",
            "-s",
            str(scale),
        ]

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
