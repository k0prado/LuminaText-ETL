import uuid
import requests
from bs4 import BeautifulSoup
from .models import VacancyRaw

class VacancyIngestionEngine:
    def __init__(self):
        pass

    def fetch_mock_vacancies(self):
        return [
            VacancyRaw(id=uuid.uuid4().hex, title="Desenvolvedor(a) Python - Backend", company="TechCorp", description_html="<p>Procuramos dev Python backend remoto. Salário R$ 8000. Contato: vaga@techcorp.com</p>"),
            VacancyRaw(id=uuid.uuid4().hex, title="Analista de Dados (Júnior)", company="DataInc", description_html="<p>Vaga de analista de dados júnior para modelo híbrido. Salário R$ 4000.</p>"),
            VacancyRaw(id=uuid.uuid4().hex, title="Estágio em Machine Learning", company="AI Labs", description_html="<p>Venha trabalhar com machine learning e pytorch em ambiente cloud.</p>"),
            VacancyRaw(id=uuid.uuid4().hex, title="Engenheiro(a) de Dados - Sênior", company="BigData Corp", description_html="<p>Engenheiro de dados sênior com experiência em Spark e Airflow hibrido.</p>")
        ]

    def fetch_url_vacancy(self, url: str) -> VacancyRaw:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            
            title = soup.title.string if soup.title else "Vaga Remota Encontrada via API"
            body_content = str(soup.body) if soup.body else response.text
            
            return VacancyRaw(
                id=uuid.uuid4().hex,
                title=title.strip(),
                company="Web Ingested",
                description_html=body_content
            )
        except Exception as e:
            raise Exception(f"Falha ao raspar a URL: {str(e)}")