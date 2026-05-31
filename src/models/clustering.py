import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VacancyClusteringModel:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer
        self.categories = [
            "Engenheiro de Inteligência Artificial", "Especialista em IA Generativa",
            "Engenheiro de Dados", "Engenheiro de Machine Learning",
            "Analista de Cibersegurança", "Auditor de Segurança da Informação",
            "Analista de Conformidade de TI", "Engenheiro Cloud",
            "Engenheiro DevOps", "Engenheiro de SRE",
            "Desenvolvedor Fullstack", "Desenvolvedor Backend",
            "Desenvolvedor Frontend", "Arquiteto de Software",
            "Auditor de Controle Externo em TI", "Perito Criminal Computacional",
            "Cientista de Dados", "Engenheiro de Hardware Embarcado",
            "Engenheiro de IoT", "Gerente de Projetos de TI",
            "Scrum Master", "Product Owner",
            "Analista de Suporte Técnico", "Administrador de Redes",
            "Analista de Sistemas"
        ]
        self._build_anchors()

    def _build_anchors(self):
        anchors = {
            "Engenheiro de Inteligência Artificial": "inteligência artificial redes neurais deep learning pytorch tensorflow nlp cv",
            "Especialista em IA Generativa": "ia generativa llm gpt bert prompt engineering langchain openai rga",
            "Engenheiro de Dados": "engenheiro dados pipeline etl spark airflow databricks sql warehouse cloud hdf",
            "Engenheiro de Machine Learning": "machine learning mlops scikit-learn deploy mlflow modelo pipeline preditivo",
            "Analista de Cibersegurança": "cibersegurança segurança ddos firewall pentest vulnerabilidade siem soc incidentes",
            "Auditor de Segurança da Informação": "auditoria segurança informação iso 27001 conformidade controle risco vulnerabilidade",
            "Analista de Conformidade de TI": "conformidade ti compliance sox lgpd governança cobit itil auditoria",
            "Engenheiro Cloud": "cloud nuvem aws azure gcp arquitetura migração terraform serverless",
            "Engenheiro DevOps": "devops ci cd jenkins github actions docker kubernetes terraform infraestrutura",
            "Engenheiro de SRE": "sre confiabilidade observabilidade prometheus grafana monitoramento SLA SLO uptime",
            "Desenvolvedor Fullstack": "fullstack javascript typescript react node angular vue backend frontend web",
            "Desenvolvedor Backend": "backend python node java c# go api rest microserviços sql banco dados",
            "Desenvolvedor Frontend": "frontend react angular vue javascript typescript css tailwind html ui ux web",
            "Arquiteto de Software": "arquiteto software padroes arquitetura microserviços clean code design patterns cloud togaf",
            "Auditor de Controle Externo em TI": "auditor controle externo tcu tce auditoria ti governança licitação publica fiscalização",
            "Perito Criminal Computacional": "perito criminal computacional forense digital extração evidencias analise discos vestigios cibercrime",
            "Cientista de Dados": "cientista dados estatistica python pandas analise exploratoria insights r",
            "Engenheiro de Hardware Embarcado": "hardware embarcado firmware microcontrolador c c++ asic fpga placas circuito pcb",
            "Engenheiro de IoT": "iot internet das coisas sensores protocolos mqtt amqp raspberry esp32 firmware",
            "Gerente de Projetos de TI": "gerente projetos ti pmp pmbok escopo cronograma orçamento stakeholders entregas",
            "Scrum Master": "scrum master agil daily sprint planning retrospectiva facilitação impedimentos kanban",
            "Product Owner": "product owner backlog historias usuario roadmap produto negocio stakeholders prioritização",
            "Analista de Suporte Técnico": "suporte tecnico chamado helpdesk desktop atendimento hardware windows linux infraestrutura",
            "Administrador de Redes": "administrador redes cisco switch router vlan tcp ip roteamento firewall infraestrutura",
            "Analista de Sistemas": "analista sistemas requisitos modelagem diagramas uml analise negocio fluxograma documentos"
        }
        
        anchor_texts = [anchors[cat] for cat in self.categories]
        anchor_matrix_list = self.vectorizer.fit_transform(anchor_texts)
        # ensure we have a numpy array for similarity calculations
        self.anchor_matrices = np.array(anchor_matrix_list)

    def predict_category(self, lemmatized_text: str) -> str:
        if not lemmatized_text.strip():
            return "Desenvolvedor Backend"
        vacancy_matrix_list = self.vectorizer.transform([lemmatized_text])
        vacancy_matrix = np.array(vacancy_matrix_list)
        similarities = cosine_similarity(vacancy_matrix, self.anchor_matrices)
        best_match_idx = np.argmax(similarities)
        
        return self.categories[best_match_idx]