from fastapi import APIRouter

health_route = APIRouter()

@health_route.get("/health")
def health():
	return {"status": "OK"}
