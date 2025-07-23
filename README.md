# Airguardian

## Setup

Create a virtual environment:

```bash
python3 -m venv {you_virtual_environment_name}
```

Activate the virtual environment:

```bash
source {you_virtual_environment_name}/bin/activate
```

Run the `requirements.txt`:

```bash
pip install -r requirements.txt
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