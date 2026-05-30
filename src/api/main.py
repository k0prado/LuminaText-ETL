import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, HTTPException
from src.database import get_database

app = FastAPI(title="LuminaText ETL & ML API", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "online", "project": "LuminaText-ETL"}

@app.get("/vacancies")
def get_all_vacancies():
    try:
        db = get_database()
        collection = db["processed_vacancies"]
        vacancies = list(collection.find({}, {"_id": 0}))
        return {"count": len(vacancies), "data": vacancies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vacancies/cluster/{cluster_id}")
def get_vacancies_by_cluster(cluster_id: int):
    try:
        db = get_database()
        collection = db["processed_vacancies"]
        vacancies = list(collection.find({"metadata.predicted_cluster": cluster_id}, {"_id": 0}))
        return {"cluster": cluster_id, "count": len(vacancies), "data": vacancies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))