# 🏠 House Management API

House Management API is a FastAPI-based service for managing houses, flats, inhabitants, and utility payments. It provides endpoints for handling buildings, water meters, electricity counters, and more.

## 🚀 Features
- Manage **Buildings**, **Flats**, and **Inhabitants**
- Track **Utility Counters** (Water, Electricity, Gas, Heat)
- **Automated Payments** Calculation
- **FastAPI & Django** Backend
- **Celery** Task Queue for Async Processing
- **PostgreSQL & Redis** for Database & Caching
- **Logstash** for Centralized Logging

## 📦 Installation

### Prerequisites
- Python **3.11**
- PostgreSQL **15+**
- Redis **7+**
- Poetry **1.8+**

### Setup

#### Local Setup
```bash
# Clone the repository
git clone https://github.com/deadlovelll/hkc.git
cd hkc
```

```bash
# Create and get into venv
python3 -m venv venv
source venv/bin/activate
```

```bash
# Install requirements
pip install -r requirements.txt
```

or

```bash
# Install requirements
pip install poetry
poetry install
poetry shell
```

```bash
# Run the services
cd house_zhkh_ms
python3 main.main.py

cd house_zhkh_core
python3 manage.py runserver
```

#### Docker Setup

```
docker compose up --buiild
```

or

```
docker-compose up --buiild
```

if you're encorouting problems try this:

```
DOCKER_BUILDKIT=0 docker compose up --build --force-recreate
```

## 🏗 Project Structure
```
.
├── base/
│   ├── models/          # Django models (Flats, Payments, Counters, etc.)
│   ├── controllers/     # Business logic
│   ├── views/           # API views
│   └── tasks.py         # Celery tasks
├── config/              # Configuration files
├── routes/              # FastAPI route handlers
├── modules/
│   ├── database/        # Database connections
│   ├── logger/          # Logstash logging setup
├── main.py              # FastAPI application entry point
├── worker.py            # Celery worker entry point
├── Dockerfile           # Docker build file
└── README.md            # Project documentation
```

## 🔥 Usage

### 1️⃣ Get House Info
```bash
curl -X GET "http://localhost:8000/houses/info?house_street=Main%20Street" -H "accept: application/json"
```

### 2️⃣ Create New House
```bash
curl -X POST "http://localhost:8000/houses/new" -H "Content-Type: application/json" -d '{"street": "Main Street", "number": "42"}'
```

### 3️⃣ Start Payment Calculation
```bash
curl -X POST "http://localhost:8000/payments/calculate" -H "accept: application/json"
```

## 🛠 Technologies
- **FastAPI** 🚀
- **Django** 🕸️
- **Celery + Redis** ⏳
- **PostgreSQL** 🗄️
- **Logstash** 📜

## 📜 License
MIT License © 2025 Timofei Ivankov

![Built with FastAPI](https://via.placeholder.com/800x200.png?text=Built+with+FastAPI)