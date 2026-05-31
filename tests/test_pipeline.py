from src.pre_processing.pipeline import ProcessingPipeline
from src.ingestion.models import VacancyRaw


def test_processing_pipeline_integration():
    engine = ProcessingPipeline()

    vacancy = VacancyRaw(
        id="abc123",
        title="Desenvolvedor(a) Python - Backend",
        company="TechCorp",
        description_html="<p>Procuramos dev Python backend remoto. Salário R$ 8.000. Contato: vaga@techcorp.com</p>",
    )

    result = engine.process_vacancy(vacancy)

    assert result["vacancy_id"] == "abc123"
    assert "cleaned_description" in result
    assert "nlp_processed" in result
    assert "metadata" in result
    assert result["metadata"]["extracted_email"] == "vaga@techcorp.com"
    assert result["metadata"]["extracted_salary"] is not None
