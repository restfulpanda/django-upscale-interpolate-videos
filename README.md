# 🧠 Video Frame Interpolation & Upscale API

The **django-upscale-interpolate-videos** project is a web application for video resolution enhancement and frame interpolation using machine learning models. The app is built with Django and packaged using Docker for simplified deployment and scalability.

---

## 📂 Project Structure

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
│   ├── upscale/                 # Flask service with upscaling model
│   │   └── dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .prod.env
└── README.md
```

---

## ⚙️ Technologies Used

| Component           | Purpose                                  |
| ------------------- | ---------------------------------------- |
| **Python 3.11**     | Programming language                     |
| **Django + DRF**    | Backend API                              |
| **Celery + Redis**  | Asynchronous task queue                  |
| **PostgreSQL**      | Database for users and video data        |
| **RIFE (Flask)**    | Video frame interpolation (FPS increase) |
| **Upscale (Flask)** | Video upscaling (quality enhancement)    |
| **Docker**          | Containerization of all services         |
| **GitHub Actions**  | CI/CD pipelines                          |

---

## 🧩 Implemented Django Services

### 🔐 Authentication (`authentication` app)

* User registration and authentication
* JWT-based login

### 🎬 Video Processing (`logic` app)

* Video upload
* Downloading processed videos

### ⏳ Task Status Tracking (`tasks` app)

* Monitoring Celery task status via `task_id`

---

## 🔌 API Endpoints

| Method | URL                           | Description                        |
| ------ | ----------------------------- | ---------------------------------- |
| POST   | `/users/register/`            | Register a new user                |
| POST   | `/users/token/`               | Obtain JWT token                   |
| POST   | `/users/token/refresh/`       | Refresh JWT token                  |
| POST   | `/videos/upload/`             | Upload a video for processing      |
| GET    | `/videos/download/<video_id>` | Download processed video           |
| GET    | `/videos/status/<task_id>`    | Check video processing task status |
| GET    | `/swagger/`                   | Swagger UI for API documentation   |

---

## 🔐 Authentication

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

---

## 🔁 Example API Usage (via curl)

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

## 📚 Swagger API Documentation

Explore and test the API in browser:

🔗 [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

Powered by `drf-yasg`.

---

## 🧠 Machine Learning Models

* 🌀 [RIFE - Real-Time Intermediate Flow Estimation](https://github.com/hzwer/Practical-RIFE)
* 📈 [Upscales Video 2x or 4x using AI](https://github.com/davlee1972/upscale_video)

---

## 🐳 Docker Containers

| Container         | Purpose                                    |
| ----------------- | ------------------------------------------ |
| `django-service`  | Main Django backend                        |
| `celery-service`  | Celery worker for video processing tasks   |
| `rife-service`    | Flask service for RIFE interpolation model |
| `upscale-service` | Flask service for video upscaling          |
| `redis`           | Message broker for Celery                  |
| `postgres`        | PostgreSQL database                        |

---

## 🚀 CI/CD (GitHub Actions)

### ✅ CI: `build-and-test`

* Installs dependencies
* Runs unit tests using `pytest`
* Performs code style and static checks with `black`, `pylint`

### 🚀 CD: `deploy`

* Builds and pushes Docker images to Yandex Container Registry
* Connects to the production server via SSH
* Pulls the latest images
* Restarts services using `docker-compose.prod.yml`
* Cleans up unused Docker images (`docker image prune -f`)

---

## 🧪 Running the Project Locally

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/msrbl/django-upscale-interpolate-videos.git
cd <repo-name>
```

### 🔧 2. Set up Environment Variables

```bash
cp .env.example .env
```

### 🐳 3. Start the Containers

```bash
docker-compose up --build
```

---

## 🧬 Useful Commands

```bash
# Apply migrations
docker-compose exec django python manage.py migrate

# Open Django shell
docker-compose exec django python manage.py shell

# Run tests
docker-compose exec django pytest
```

---

## ❗ Common Issues

| Problem                                | Solution                                                  |
| -------------------------------------- | --------------------------------------------------------- |
| `Video not found`                      | Make sure `/media` is correctly mounted in all containers |
| `Connection refused` to Flask services | Check Docker network / container names                    |
| Celery not working                     | Ensure Redis and `celery-service` are running             |
| 403/401 errors                         | Use a valid JWT token in headers                          |

---

## 🧾 License

MIT License — use freely with attribution.