from typing import Dict
from fastapi import FastAPI
import unit_commitment
import payload_classes

app = FastAPI()

result = {}

@app.get("/")
async def root():
    return "Go to /productionplan to access the API"

@app.get("/productionplan")
async def fetch_result():
    return result

@app.post("/productionplan")
async def enter_payload(payload: payload_classes.Payload):
    result["unit_commitment"] = unit_commitment.main(payload)
