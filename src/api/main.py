import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database import get_database
from src.ingestion.scraper import VacancyIngestionEngine
from src.cleaning.text_cleaner import clean_html, SalaryExtractor, EmailExtractor, WorkModelExtractor
from src.pre_processing.nlp_pipeline import StopwordsProcessor, LemmatizerProcessor
from src.main import process_and_train_all

app = FastAPI(title="LuminaText Production AI Platform", version="2.0.0")

class UrlPayload(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "online", "engine": "Similaridade por Âncoras Semânticas"}

@app.get("/vacancies")
def get_all_vacancies():
    db = get_database()
    collection = db["processed_vacancies"]
    vacancies = list(collection.find({}, {"_id": 0}))
    return {"count": len(vacancies), "data": vacancies}

@app.post("/vacancies/ingest-url")
def ingest_by_url(payload: UrlPayload):
    try:
        db = get_database()
        collection = db["processed_vacancies"]
        
        # 1. Busca o HTML bruto da URL informada
        engine = VacancyIngestionEngine()
        raw_vacancy = engine.fetch_url_vacancy(payload.url)
        
        # 2. Executa toda a esteira de NLP e limpeza construída
        clean_text = clean_html(raw_vacancy.description_html)
        
        salary_extractor = SalaryExtractor()
        email_extractor = EmailExtractor()
        work_model_extractor = WorkModelExtractor()
        stopwords_processor = StopwordsProcessor()
        lemmatizer_processor = LemmatizerProcessor()
        
        document = {
            "vacancy_id": raw_vacancy.id,
            "title": raw_vacancy.title,
            "company": raw_vacancy.company,
            "cleaned_description": clean_text,
            "nlp_processed": {
                "tokens_without_stopwords": stopwords_processor.process(clean_text),
                "lemmatized_base_text": lemmatizer_processor.process(clean_text)
            },
            "metadata": {
                "extracted_salary": salary_extractor.extract(clean_text),
                "extracted_email": email_extractor.extract(clean_text),
                "work_model": work_model_extractor.extract(clean_text),
                "predicted_cluster": "Pendente"
            }
        }
        
        # 3. Salva a nova vaga no MongoDB
        collection.insert_one(document)
        
        # 4. Aciona automaticamente o re-treinamento da IA com o novo dado incluso!
        process_and_train_all()
        
        return {"status": "sucesso", "message": f"URL processada e IA re-treinada para a vaga: {raw_vacancy.title}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/vacancies/reset")
def reset_database_and_training():
    try:
        db = get_database()
        collection = db["processed_vacancies"]
        
        # Deleta absolutamente todos os registros
        result = collection.delete_many({})
        
        return {
            "status": "sucesso", 
            "message": "Banco de dados limpo e histórico de treinamento resetado com sucesso!",
            "documents_deleted": result.deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))