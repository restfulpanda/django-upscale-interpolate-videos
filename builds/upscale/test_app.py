import os
import pytest
from unittest.mock import patch, MagicMock
from .server_upscale import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json == {"message": "pong"}

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "message": "Flask app is running"}

def test_upscale_missing_input_path(client):
    response = client.post("/upscale", json={"output_path": "out.mp4"})
    assert response.status_code == 400
    assert "error" in response.json

def test_upscale_file_not_exists(client):
    with patch("os.path.exists", return_value=False):
        response = client.post("/upscale", json={
            "input_path": "fake.mp4",
            "output_path": "out.mp4"
        })
        assert response.status_code == 404
        assert "error" in response.json

def test_upscale_success(client):
    with patch("os.path.exists", return_value=True), \
         patch("subprocess.run") as mock_run:
        
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        response = client.post("/upscale", json={
            "input_path": "input.mp4",
            "output_path": "output.mp4",
            "multi": 2
        })

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["output"] == "output.mp4"

def test_upscale_subprocess_failure(client):
    with patch("os.path.exists", return_value=True), \
         patch("subprocess.run") as mock_run:

        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "Some error occurred"
        mock_run.return_value = mock_process

        response = client.post("/upscale", json={
            "input_path": "input.mp4",
            "output_path": "output.mp4"
        })

        assert response.status_code == 500
        assert "error" in response.json
        assert "Some error occurred" in response.json["error"]
