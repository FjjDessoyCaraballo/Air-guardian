# Airguardian

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
```

## Running the Application

### Start RabbitMQ (Message Broker)
```bash
docker run -d -p 5672:5672 --name rabbitmq rabbitmq:3-management
```

### Run the Celery Worker (Background Tasks)
```bash
poetry run celery -A patrol_airspace worker --beat --loglevel=info
```

### Start the FastAPI Server
```bash
poetry run uvicorn main:air_guardian --reload --host 0.0.0.0 --port 8000
```

### Run Tests
```bash
poetry run test
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

