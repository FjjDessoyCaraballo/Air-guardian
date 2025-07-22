from fastapi import APIRouter

nfz_route = APIRouter()

@nfz_route.get("/nfz")
def nfz():
	return