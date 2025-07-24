from fastapi import APIRouter, Request, HTTPException
from utils.nfz import authenticate

nfz_route = APIRouter()

@nfz_route.get("/nfz")
def nfz(req: Request):
	authenticated = authenticate(req.headers.get("X-Secret"))
	if not authenticated:
		raise HTTPException(401, "Unauthorized")
	# fetch from db
	return