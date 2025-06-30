# <div align="center">Video Frame Interpolation & Upscale API</div>

<div align="center">

![MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![CI Status](https://github.com/restfulpanda/django-upscale-interpolate-videos/actions/workflows/ci.yml/badge.svg)
![CD Status](https://github.com/restfulpanda/django-upscale-interpolate-videos/actions/workflows/cd.yml/badge.svg)
[![Django Image](https://img.shields.io/docker/image-size/do1lbyy/django-service)](https://hub.docker.com/r/do1lbyy/django-service)
[![RIFE Image](https://img.shields.io/docker/image-size/do1lbyy/rife-service)](https://hub.docker.com/r/do1lbyy/rife-service)
[![ESRGAN Image](https://img.shields.io/docker/image-size/do1lbyy/esrgan-service)](https://hub.docker.com/r/do1lbyy/esrgan-service)

</div>

The **django-upscale-interpolate-videos** project is a web application for video resolution enhancement and frame interpolation using machine learning models. The app is built with Django and packaged using Docker for simplified deployment and scalability.

---
### 🎬 Demo

<div align="center">


#### **Original Video** (15 FPS, HD)
<video width="100%" controls><source src="assets/girl5_15FPS_HD.mp4" type="video/mp4">Your browser does not support the video tag.</video>

#### **Processed x4** (60 FPS, 4K)
<video width="100%" controls><source src="assets/girl5_60FPS_4K.mp4" type="video/mp4">Your browser does not support the video tag.</video>

</div>

📁 [Download Demo Videos](https://drive.google.com/drive/folders/1DzsBGQrUqGh9fhe23dmQJ8fj4sGKAKbL?usp=sharing)

> **Note:** The demo videos above showcase the transformation from a low-quality, low-frame-rate video to a high-quality, smooth video through our ML-powered processing pipeline.

---

### 🧠 Machine Learning Models

* 🌀 [RIFE - Real-Time Intermediate Flow Estimation](https://github.com/hzwer/Practical-RIFE)
* 📈 [Real-ESRGAN - Real Enhanced Super-Resolution Generative Adversarial Network](https://github.com/xinntao/Real-ESRGAN)

---

### 📂 Project Structure

```
├── builds/
│   ├── django/                  # Django app (backend + Celery)
│   │   ├── authentication/      # User registration and authentication
│   │   ├── logic/               # API for uploading and downloading videos
│   │   ├── tasks/               # Celery tasks and status tracking
│   │   ├── media/               # Uploaded and processed video files
│   │   ├── logs/                # Log files
│   │   ├── entrypoint.sh        # Entrypoint script
│   │   ├── dockerfile           # Dockerfile for Django
│   │   └── manage.py
│   ├── rife/                    # Flask service with interpolation model
│   │   └── dockerfile
│   ├── esrgan/                  # Flask service with upscaling model
│   │   └── dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .prod.env
└── README.md
```

---

### ⚙️ Technologies Used

| Component                    | Purpose                                  |
| ---------------------------- | ---------------------------------------- |
| **Python 3.11**              | Programming language                     |
| **Django + DRF**             | Backend API                              |
| **Celery + Redis**           | Asynchronous task queue                  |
| **PostgreSQL**               | Database for users and video data        |
| **Practical-RIFE (Flask)**   | Video frame interpolation (FPS increase) |
| **Real-ESRGAN (Flask)**      | Video upscaling (quality enhancement)    |
| **Docker**                   | Containerization of all services         |
| **GitHub Actions**           | CI/CD pipelines                          |

---

### 🧩 Implemented Django Services

#### 🔐 Authentication (`authentication` app)

* User registration and authentication
* JWT-based login

#### 🎬 Video Processing (`logic` app)

* Video upload
* Downloading processed videos

#### ⏳ Task Status Tracking (`tasks` app)

* Monitoring Celery task status via `task_id`

### 🔌 API Endpoints

| Method | URL                           | Description                        |
| ------ | ----------------------------- | ---------------------------------- |
| POST   | `/users/register/`            | Register a new user                |
| POST   | `/users/token/`               | Obtain JWT token                   |
| POST   | `/users/token/refresh/`       | Refresh JWT token                  |
| POST   | `/videos/upload/`             | Upload a video for processing      |
| GET    | `/videos/download/<video_id>` | Download processed video           |
| GET    | `/videos/status/<task_id>`    | Check video processing task status |
| GET    | `/swagger/`                   | Swagger UI for API documentation   |

### 🔐 Authentication

All secure endpoints require **JWT token** authentication.

1. Obtain token:

   ```
   POST /users/register/
   {
     "username": "user",
     "email": "user@example.com",
     "password": "your_password"
   }
   ```

2. Use it in headers:

   ```
   Authorization: Bearer <access_token>
   ```

3. Refresh token:

   ```
   POST /users/token/refresh/
   ```

### 🔁 Example API Usage (via curl)

```bash
# Upload a video
curl -X POST http://localhost:8000/videos/upload/ \
  -H "Authorization: Bearer <token>" \
  -F "original_video=@/path/to/video.mp4"

# Check processing status
curl http://localhost:8000/videos/status/<task_id> \
  -H "Authorization: Bearer <token>"

# Download final result
curl -O http://localhost:8000/videos/download/<video_id>
```

---

### 🚀 CI/CD (GitHub Actions)

#### ✅ CI: `build-and-test`

* Installs dependencies
* Runs unit tests using `pytest`
* Performs code style and static checks with `black`, `pylint`

#### 🚀 CD: `deploy`

* Builds and pushes Docker images to Yandex Container Registry
* Connects to the production server via SSH
* Pulls the latest images
* Restarts services using `docker-compose.prod.yml`
* Cleans up unused Docker images (`docker image prune -f`)

---

### 🧪 Running the Project Locally


#### 🖥️ System Requirements

**NVIDIA GPU Requirements:**
- NVIDIA GPU with CUDA support
- NVIDIA Driver version **450.80.02** or higher
- CUDA Toolkit version **11.0** or higher (compatible with CUDA 12.4)

#### 🔁 1. Clone the Repository

```bash
git clone https://github.com/restfulpanda/django-upscale-interpolate-videos.git
cd <repo-name>
```

#### 🔧 2. Set up Environment Variables

```bash
cp .env.example .env

# Configure the following variables in .env file:
# - SECRET_KEY: Django secret key (generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# - POSTGRES_DB: Database name (default: UIDataBase)
# - POSTGRES_HOST: Database host (default: postgres-db)
# - POSTGRES_USER: Database user (default: postgres)
# - POSTGRES_PASSWORD: Database password
# - POSTGRES_ROOT_PASSWORD: Database root password
# - DJANGO_ALLOWED_HOSTS: Comma-separated list of allowed hosts
# - VIDEO_STORAGE_DIR: Video storage directory (default: /media)
```

#### 🐳 3. Start the Containers

```bash
docker-compose up --build
```

---

### ❗ Common Issues

| Problem                                | Solution                                                                                        |
| -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `Video not found`                      | Check that `/media` volume is properly mounted in all containers and verify file permissions    |
| `Connection refused` to Flask services | Verify Docker network connectivity and ensure service names match `practical-rife` and `esrgan` |
| Celery tasks not processing            | Confirm Redis is running and `celery-service` container is healthy; check Celery logs           |
| 403/401 authentication errors          | Ensure valid JWT token is included in Authorization header: `Bearer <your-token>`               |
| Database connection issues             | Verify PostgreSQL container is running and environment variables are correctly set              |
| Docker build failures                  | Check available disk space and ensure all required files are present in build context           |

---

### 🧾 License

MIT License — use freely with attribution.
