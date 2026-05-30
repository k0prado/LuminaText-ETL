import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from src.database import get_database
from src.ingestion.scraper import VacancyIngestionEngine
from src.cleaning.text_cleaner import (
    clean_html,
    SalaryExtractor,
    EmailExtractor,
    WorkModelExtractor
)
from src.pre_processing.nlp_pipeline import (
    StopwordsProcessor,
    LemmatizerProcessor
)
from src.pre_processing.vectorizer import TfidfTextVectorizer
from src.analytics.text_analytics import JobTextAnalytics

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Iniciando o Pipeline ETL LuminaText com NLP integrado...")
    
    try:
        db = get_database()
        collection = db["processed_vacancies"]
    except Exception as e:
        logger.error(f"Falha ao conectar no MongoDB: {e}")
        return

    engine = VacancyIngestionEngine()
    raw_vacancies = engine.fetch_mock_vacancies()
    
    salary_extractor = SalaryExtractor()
    email_extractor = EmailExtractor()
    work_model_extractor = WorkModelExtractor()
    
    stopwords_processor = StopwordsProcessor()
    lemmatizer_processor = LemmatizerProcessor()

    processed_documents = []

    for vacancy in raw_vacancies:
        logger.info(f"Processando e aplicando NLP na vaga ID: {vacancy.id} - {vacancy.title}")
        
        clean_text = clean_html(vacancy.description_html)
        
        salary = salary_extractor.extract(clean_text)
        email = email_extractor.extract(clean_text)
        work_model = work_model_extractor.extract(clean_text)
        
        text_without_stopwords = stopwords_processor.process(clean_text)
        lemmatized_text = lemmatizer_processor.process(clean_text)
        
        document = {
            "vacancy_id": vacancy.id,
            "title": vacancy.title,
            "company": vacancy.company,
            "cleaned_description": clean_text,
            "nlp_processed": {
                "tokens_without_stopwords": text_without_stopwords,
                "lemmatized_base_text": lemmatized_text
            },
            "metadata": {
                "extracted_salary": salary,
                "extracted_email": email,
                "work_model": work_model
            }
        }
        processed_documents.append(document)

    if processed_documents:
        try:
            collection.delete_many({})
            collection.insert_many(processed_documents)
            logger.info(f"Sucesso! {len(processed_documents)} vagas salvas no MongoDB.")
        except Exception as e:
            logger.error(f"Erro ao salvar dados no MongoDB: {e}")
            return

    logger.info("Iniciando etapa de Mineração de Texto e Vetorização...")
    
    stored_vacancies = list(collection.find({}, {"nlp_processed.lemmatized_base_text": 1}))
    lemmatized_corpus = [v["nlp_processed"]["lemmatized_base_text"] for v in stored_vacancies if "nlp_processed" in v]
    
    analytics = JobTextAnalytics()
    top_keywords = analytics.get_top_keywords(lemmatized_corpus, top_n=5)
    
    logger.info(f"Top 5 Termos mais frequentes nas vagas: {top_keywords}")
    
    vectorizer = TfidfTextVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lemmatized_corpus)
    features = vectorizer.get_feature_names()
    
    logger.info(f"Matriz TF-IDF gerada com sucesso! Shape: {len(tfidf_matrix)}x{len(features)}")
    logger.info("Pipeline ETL, NLP e Analytics finalizado com sucesso!")

if __name__ == "__main__":
    run_pipeline()