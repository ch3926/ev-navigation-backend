# EV Charging Stations API

Python/FastAPI backend built as an extension of my React Native EV navigation app. Finds charging stations within a vehicle's remaining range. Deployed on AWS Lambda using API Gateway.

## Features

- Retrieve charging stations by ID or as a list
- Calculate geographic distances and filter stations by remaining EV range
- Request validation with Pydantic
- Automated API testing with pytest and GitHub Actions
- AWS Lambda deployment with API Gateway

## API Endpoints

| Method | Endpoint                 | Description                |
| ------ | ------------------------ | -------------------------- |
| GET    | `/health`                | Health check               |
| GET    | `/stations`              | List stations              |
| GET    | `/stations/{station_id}` | Get station by ID          |
| POST   | `/reachable-stations`    | Find stations within range |

## How to Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

Run tests locally using pytest:

```bash
python -m pytest -v
```
