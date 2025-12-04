from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# CSV file to store telemetry
CSV_PATH = "telemetry.csv"

# Create CSV with headers if it doesn't exist
if not os.path.exists(CSV_PATH):
    df = pd.DataFrame(columns=[
        "timestamp", 
        "temperature", 
        "vibration", 
        "pressure"
    ])
    df.to_csv(CSV_PATH, index=False)

class Telemetry(BaseModel):
    temperature: float
    vibration: float
    pressure: float

@app.post("/ingest")
def ingest_data(data: Telemetry):
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": data.temperature,
        "vibration": data.vibration,
        "pressure": data.pressure
    }

    df = pd.DataFrame([row])
    df.to_csv(CSV_PATH, mode='a', header=False, index=False)

    return {"status": "success", "message": "Telemetry stored"}