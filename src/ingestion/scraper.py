from __future__ import annotations

from dataclasses import dataclass
import logging
import uuid
from typing import List

__all__ = ["JobVacancy", "VacancyIngestionEngine"]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class JobVacancy:

	id: str
	title: str
	company: str
	description_html: str


class VacancyIngestionEngine:

	def __init__(self) -> None:
		pass

	def _new_id(self) -> str:
		return uuid.uuid4().hex

	def fetch_mock_vacancies(self) -> List[JobVacancy]:

		logger.info("Starting mock vacancy ingestion")

		vacancies: List[JobVacancy] = [
			JobVacancy(
				id=self._new_id(),
				title="Desenvolvedor(a) Python - Backend",
				company="Tech & Co <span class=\"tag\">LTDA</span>",
				description_html=(
					"<div><h1>Vaga: Desenvolvedor(a) Python</h1>"
					"<p>Trabalhe com APIs, data pipelines e deploy.</p>"
					"<p>Salário: R$ 3.500,00 - R$4.200,00</p>"
					"<p>Modelo: remoto / híbrido</p>"
					"<p>Contato: recrutamento@techco.com.br</p>"
					"<script>var x = 1;</script>"
					"<!-- noisy comment -->"
					"</div>"
				),
			),
			JobVacancy(
				id=self._new_id(),
				title="Analista de Dados (Júnior)",
				company="Empresa Exemplo",
				description_html=(
					"<article><strong>Analista de Dados</strong> para time de"
					" BI.<br>Benefícios: VR, VT, plano odontológico.</br>"
					"Salário aproximado: R$5.000,00 (clt/consultoria)."
					"<div>Modelo: Híbrido. Local: São Paulo/SP</div>"
					"E-mail: rh@empresa-exemplo.com</article>"
				),
			),
			JobVacancy(
				id=self._new_id(),
				title="Estágio em Machine Learning",
				company="Pesquisa&Co",
				description_html=(
					"<div class=missing>Descrição:<ul><li>Limpeza de dados</li>"
					"<li>Treino de modelos</li></ul>"
					"Salário: R$ 1.200,00 - bolsa</p>"
					"<p>Modelo: presencial / híbrido / remoto</p>"
					"<a href=\"mailto:contato@pesquisa.co\">contato@pesquisa.co</a>"
					"<style>body{display:none}</style>"
					"</div>"
				),
			),
			JobVacancy(
				id=self._new_id(),
				title="Engenheiro(a) de Dados - Sênior",
				company="BigData <em>Corp</em>",
				description_html=(
					"<div>Vaga sênior. Requisitos: Spark, Airflow, SQL.<br>"
					"Salário: R$12.000,00 ou a combinar.</br>"
					"Contato: jobs@datacorp.com | contato@datacorp.com.br"
					"<p>Modelo: remoto</p><iframe src=\"//malicious\"></iframe>"
					"</div>"
				),
			),
		]

		logger.info("Finished mock vacancy ingestion: %d records", len(vacancies))

		return vacancies


if __name__ == "__main__":
	import logging as _logging

	_logging.basicConfig(level=_logging.INFO)
	engine = VacancyIngestionEngine()
	items = engine.fetch_mock_vacancies()
	for v in items:
		print(f"- {v.id} | {v.title} @ {v.company}")

