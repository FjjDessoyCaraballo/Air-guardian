# Airguardian

## Prerequisites

- Python 3.12+
- Poetry (for dependency management)

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

Start the message broker rabbitmq in a container
```bash
docker run -d -p 5672:5672 rabbitmq
```
Run the Celery worker server
```bash
celery -A patrol_airspace worker --beat --loglevel=info  
```

Get this bad boy online and serving files!

```bash
uvicorn main:air_guardian
```
