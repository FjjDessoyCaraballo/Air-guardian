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

### Run Development Server
```bash
poetry run uvicorn --reload --host 0.0.0.0
```

## Environment Setup

Create a `.env` file in the project root with your configuration:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/airguardian
DEBUG=True
```

## Development

### Direct Command
```bash
poetry run uvicorn src.main:app --reload
```
