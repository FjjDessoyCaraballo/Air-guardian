from fastapi import APIRouter, Request, HTTPException
from utils.nfz import authenticate, retrieve_nfz_list
import os

nfz_route = APIRouter()

@nfz_route.get("/nfz")
def nfz(req: Request):
	"""
	The `nfz` endpoint requires the secret to be in the header. If you want to test it out, you need
	to use `curl -H "X-SECRET: {secret}" http://localhost:{port}/nfz`.
	"""
	authenticated = authenticate(req.headers.get("X-SECRET"))
	if not authenticated:
		return HTTPException(401, "Unauthorized")

	offenders = retrieve_nfz_list()
	
	if offenders is None:
		return HTTPException(204, "No content")

	return {"offenders": offenders, "count": len(offenders)}
