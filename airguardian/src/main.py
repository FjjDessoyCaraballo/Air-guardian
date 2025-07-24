from fastapi import FastAPI
import sqlite3

app = FastAPI()

conn = sqlite3.connect("mydb.db")

@app.get("/health")
def health():
	return {"status": "OK"}

@app.get("/drones")
def drones():
	return

@app.get("/nfz")
def nfz():
	return