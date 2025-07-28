from celery import Celery
from utils.setup import initialize_celery_vars
import requests
import os

initialize_celery_vars()

celeryapp = Celery(__name__, broker=os.environ["BROKER_URL"])
@celeryapp.on_after_configure.connect
def setup_up_contab(**kwargs):
    celeryapp.add_periodic_task(10, patrol_airspace, name="Patroling the airspace")

@celeryapp.task
def patrol_airspace():
    url = os.environ["LOCAL_HOST_URL"] + "drones"
    try:
        requests.get(url)
    except Exception as err:
        print(err)
    