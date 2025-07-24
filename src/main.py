from fastapi import FastAPI
import psycopg

app = FastAPI()

@app.get("/health")
def health():
	return {"status": "OK"}

@app.get("/drones")
def drones():
	return

@app.get("/nfz")
def nfz():
	return