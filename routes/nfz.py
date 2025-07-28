from fastapi import APIRouter, Request, HTTPException
from utils.nfz import authenticate, retrieve_nfz_list
import os


nfz_route = APIRouter()

@nfz_route.get("/nfz")
def nfz(req: Request):
	authenticated = authenticate(req.headers.get("X-Secret"))
	if not authenticated:
		return HTTPException(401, "Unauthorized")

	offenders = retrieve_nfz_list()
	
	if offenders is None:
		return HTTPException(204, "No content")

	return {"offenders": offenders, "count": len(offenders)}
