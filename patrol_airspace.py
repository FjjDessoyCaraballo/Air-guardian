from celery import Celery
import requests

celeryapp = Celery(__name__, broker='amqp://localhost:5672')
@celeryapp.on_after_configure.connect
def setup_up_contab(**kwargs):
    celeryapp.add_periodic_task(10, patrol_airspace, name="Patroling the airspace")

@celeryapp.task
def patrol_airspace():
    requests.get("http://localhost:8000/drones")
