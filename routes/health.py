from fastapi import APIRouter
from utils.models import Health

health_route = APIRouter()

@health_route.get("/health", response_model=Health)
def health():
	return {"status": "OK"}
