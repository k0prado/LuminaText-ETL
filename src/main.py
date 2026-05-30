import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from src.database import get_database
from src.cleaning.text_cleaner import clean_html, SalaryExtractor, EmailExtractor, WorkModelExtractor
from src.pre_processing.nlp_pipeline import StopwordsProcessor, LemmatizerProcessor
from src.pre_processing.vectorizer import TfidfTextVectorizer
from src.models.clustering import VacancyClusteringModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def process_and_train_all():
    db = get_database()
    collection = db["processed_vacancies"]
    
    stored_vacancies = list(collection.find({}))
    if not stored_vacancies:
        logger.info("Nenhuma vaga encontrada no MongoDB para rodar o treinamento.")
        return
        
    lemmatized_corpus = [v["nlp_processed"]["lemmatized_base_text"] for v in stored_vacancies if "nlp_processed" in v]
    
    vectorizer = TfidfTextVectorizer()
    # Inicializa o vocabulário com as âncoras internas
    clustering_model = VacancyClusteringModel(vectorizer)
    
    for vacancy_doc in stored_vacancies:
        lemmatized_text = vacancy_doc["nlp_processed"]["lemmatized_base_text"]
        predicted_cluster = clustering_model.predict_category(lemmatized_text)
        
        collection.update_one(
            {"_id": vacancy_doc["_id"]},
            {"$set": {"metadata.predicted_cluster": predicted_cluster}}
        )
    logger.info("Todos os modelos e categorias foram re-treinados e atualizados no MongoDB.")

if __name__ == "__main__":
    from src.ingestion.scraper import VacancyIngestionEngine
    db = get_database()
    col = db["processed_vacancies"]
    engine = VacancyIngestionEngine()
    
    # Carga inicial se estiver vazio
    if col.count_documents({}) == 0:
        raws = engine.fetch_mock_vacancies()
        salary_extractor = SalaryExtractor()
        email_extractor = EmailExtractor()
        work_model_extractor = WorkModelExtractor()
        stopwords_processor = StopwordsProcessor()
        lemmatizer_processor = LemmatizerProcessor()
        
        for vacancy in raws:
            clean_text = clean_html(vacancy.description_html)
            document = {
                "vacancy_id": vacancy.id,
                "title": vacancy.title,
                "company": vacancy.company,
                "cleaned_description": clean_text,
                "nlp_processed": {
                    "tokens_without_stopwords": stopwords_processor.process(clean_text),
                    "lemmatized_base_text": lemmatizer_processor.process(clean_text)
                },
                "metadata": {
                    "extracted_salary": salary_extractor.extract(clean_text),
                    "extracted_email": email_extractor.extract(clean_text),
                    "work_model": work_model_extractor.extract(clean_text)
                }
            }
            col.insert_one(document)
    process_and_train_all()