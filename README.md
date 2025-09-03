# Air-guardian

![](./airguardian.gif)

## Overview

The Airguardian is an app that monitors and logs activity of drones. One can check the activity of the drones through the [radar](https://drones-api.hive.fi/demo3d) to compare with the results from our database.

This project uses three API endpoints: health, drones, and nfz. Through these endpoints we capture given data in JSON format from [here](https://drones-api.hive.fi/) and we detect all offending drones within 1000m radius of the no-fly zone.

### System Architecture design

<img width="1187" height="582" alt="Flowchart" src="https://github.com/user-attachments/assets/6ea8c40b-2cda-4ba2-b3c5-5b7fbab2f3ed" />

## Prerequisites

- Python 3.12+
- Poetry (for dependency management)
- Docker (for RabbitMQ)

## Installation

### Install Poetry

**Official installer (Recommended)**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Verify Poetry Installation
```bash
poetry --version
```

## Project Setup

### Install Dependencies
```bash
poetry install
```

### Environment Setup
Create a `.env` file with your configuration:
```env
DRONES_API_BASE_URL=https://api.example.com/
X-SECRET=your-secret-key
BROKER_URL=amqp://localhost:5672
LOCAL_HOST_URL=http://localhost:8000/
DB_NAME=nfz_list
DB_USER=user_name
DB_PASSWORD=super_secret_password
```

## Running the Application

### Start RabbitMQ (Message Broker)
```bash
docker run -d -p 5672:5672 --name rabbitmq rabbitmq:3-management
```

### Run the Celery Worker (Background Tasks)
```bash
poetry run celery -A patrol_airspace worker --beat --loglevel=info --logfile=air_guardian_celery.log
```

### Start the FastAPI Server
```bash
poetry run uvicorn main:air_guardian --reload --host 0.0.0.0 --port 8000
```

## Table Structure

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| `id` | `integer` | NOT NULL | `nextval('nfz_offender_id_seq'::regclass)` | **Primary Key** (Auto-increment) |
| `drone_uuid` | `text` | NOT NULL | - | **Unique Constraint** |
| `time` | `timestamp with time zone` | YES | - | Violation timestamp |
| `position_x` | `double precision` | YES | - | X coordinate |
| `position_y` | `double precision` | YES | - | Y coordinate |
| `position_z` | `double precision` | YES | - | Z coordinate |
| `first_name` | `text` | YES | - | Owner's first name |
| `last_name` | `text` | YES | - | Owner's last name |
| `social_security` | `text` | YES | - | Owner's social security |
| `phone_number` | `text` | YES | - | Owner's phone number |

## API Endpoints

- **Health Check**: `GET /health`
- **Drones**: `GET /drones`
- **No-Fly Zones**: `GET /nfz` (requires X-Secret header)

## FAQ

> "The `/nfz` endpoint keeps telling me I'm unauthorized!"

Direct access through the browser will probably need some modifications to your header. The best way to test this endpoint is through `curl` command in terminal:

```bash
curl -H "X-Secret:{your-super-secret}" http://localhost:8000/nfz
```
Or using [Postman](https://www.postman.com/) and adding the X-SECRET header with your secret.
