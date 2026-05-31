from typing import Optional

from src.cleaning.text_cleaner import clean_html
from src.cleaning.extractors import SalaryExtractor, EmailExtractor, WorkModelExtractor
from src.pre_processing.nlp_pipeline import StopwordsProcessor, LemmatizerProcessor
from src.pre_processing.vectorizer import TfidfTextVectorizer
from src.models.clustering import VacancyClusteringModel
from src.ingestion.models import VacancyRaw


class ProcessingPipeline:
    def __init__(
        self,
        salary_extractor: Optional[SalaryExtractor] = None,
        email_extractor: Optional[EmailExtractor] = None,
        work_model_extractor: Optional[WorkModelExtractor] = None,
        stopwords_processor: Optional[StopwordsProcessor] = None,
        lemmatizer_processor: Optional[LemmatizerProcessor] = None,
        vectorizer: Optional[TfidfTextVectorizer] = None,
        clustering_model: Optional[VacancyClusteringModel] = None,
    ):
        self.salary_extractor = salary_extractor or SalaryExtractor()
        self.email_extractor = email_extractor or EmailExtractor()
        self.work_model_extractor = work_model_extractor or WorkModelExtractor()
        self.stopwords_processor = stopwords_processor or StopwordsProcessor()
        self.lemmatizer_processor = lemmatizer_processor or LemmatizerProcessor()
        self.vectorizer = vectorizer or TfidfTextVectorizer()
        # Clustering model depends on vectorizer; build default if not provided
        self.clustering_model = clustering_model or VacancyClusteringModel(self.vectorizer)

    def process_vacancy(self, vacancy: VacancyRaw) -> dict:
        cleaned = clean_html(vacancy.description_html)
        tokens_no_stop = self.stopwords_processor.process(cleaned)
        lemmatized = self.lemmatizer_processor.process(cleaned)

        predicted_cluster = (
            self.clustering_model.predict_category(lemmatized)
            if lemmatized and lemmatized.strip()
            else "Pendente"
        )

        return {
            "vacancy_id": vacancy.id,
            "title": vacancy.title,
            "company": vacancy.company,
            "cleaned_description": cleaned,
            "nlp_processed": {
                "tokens_without_stopwords": tokens_no_stop,
                "lemmatized_base_text": lemmatized,
            },
            "metadata": {
                "extracted_salary": self.salary_extractor.extract(cleaned),
                "extracted_email": self.email_extractor.extract(cleaned),
                "work_model": self.work_model_extractor.extract(cleaned),
                "predicted_cluster": predicted_cluster,
            },
        }
