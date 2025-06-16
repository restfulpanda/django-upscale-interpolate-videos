from unittest.mock import patch, MagicMock

import pytest

from .server_interpolation import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_healthcheck(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_interpolate_missing_paths(client):
    response = client.post("/interpolate", json={"input_path": "in.mp4"})
    assert response.status_code == 400
    assert "error" in response.json


def test_interpolate_file_not_found(client):
    with patch("os.path.exists", return_value=False):
        response = client.post(
            "/interpolate", json={"input_path": "fake.mp4", "output_path": "out.mp4"}
        )
        assert response.status_code == 404
        assert "error" in response.json
        assert "does not exist" in response.json["error"]


def test_interpolate_success(client):
    with patch("os.path.exists", return_value=True), patch(
        "subprocess.run"
    ) as mock_run:

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        response = client.post(
            "/interpolate",
            json={"input_path": "input.mp4", "output_path": "output.mp4", "multi": 2},
        )

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["output"] == "output.mp4"


def test_interpolate_subprocess_error(client):
    with patch("os.path.exists", return_value=True), patch(
        "subprocess.run"
    ) as mock_run:

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stderr = "Interpolation error"
        mock_run.return_value = mock_proc

        response = client.post(
            "/interpolate",
            json={"input_path": "input.mp4", "output_path": "output.mp4"},
        )

        assert response.status_code == 500
        assert "error" in response.json
        assert "Interpolation error" in response.json["error"]
