# EV Charging Stations API

Python/FastAPI backend built as an extension of my React Native EV navigation app. Finds charging stations within a vehicle's remaining range. Deployed on AWS Lambda using API Gateway (station data stored in Amazon DynamoDB).

## Features

- Retrieve charging stations by ID or as a list
- Calculate geographic distances and filter stations by remaining EV range
- Store and retrieve station data using DynamoDB and boto3
- Use sample station data for local development and testing
- Request validation with Pydantic
- Automated API testing with pytest and GitHub Actions
- Automatic deployment to AWS Lambda after tests pass on main

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

Local dev/testing uses sample station data by default. The deployed Lambda function reads from DynamoDB.

After starting the server, view the interactive API documentation at `http://127.0.0.1:8000/docs`

Run tests locally using pytest:

```bash
python -m pytest -v
```
