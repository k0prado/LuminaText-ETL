import pytest
from src.pre_processing.vectorizer import TfidfTextVectorizer
from src.models.clustering import VacancyClusteringModel

def test_model_initialization_and_categories():
    """Garante que o modelo inicializa com o vetorizador e possui as 25 categorias."""
    vectorizer = TfidfTextVectorizer()
    model = VacancyClusteringModel(vectorizer)
    
    assert len(model.categories) == 25
    assert "Engenheiro de Dados" in model.categories
    assert "Especialista em IA Generativa" in model.categories

def test_model_predicts_correct_category_by_similarity():
    """Valida se o modelo classifica corretamente com base nas palavras-chave (âncoras)."""
    vectorizer = TfidfTextVectorizer()
    model = VacancyClusteringModel(vectorizer)
    
    # Testando uma vaga com forte viés de IA Generativa
    text_ai_gen = "vaga para especialista focado em llm gpt prompt engineering e langchain"
    predicted_ai = model.predict_category(text_ai_gen)
    assert predicted_ai == "Especialista em IA Generativa"
    
    # Testando uma vaga com forte viés de Engenharia de Dados
    text_data = "procuramos profissional para criar pipeline etl usando spark airflow e sql"
    predicted_data = model.predict_category(text_data)
    assert predicted_data == "Engenheiro de Dados"

def test_model_handles_empty_text_gracefully():
    """Garante que o modelo não quebra e retorna uma categoria padrão para textos vazios."""
    vectorizer = TfidfTextVectorizer()
    model = VacancyClusteringModel(vectorizer)
    
    predicted = model.predict_category("")
    assert predicted in model.categories