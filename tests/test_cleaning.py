import pytest
from src.cleaning.text_cleaner import (
    clean_html,
    SalaryExtractor,
    EmailExtractor,
    WorkModelExtractor
)

def test_clean_html_removes_tags():
    raw_html = "<p>Olá, <strong>Mundo</strong>!</p>"
    assert clean_html(raw_html) == "Olá, Mundo!"

def test_clean_html_handles_empty_and_none():
    assert clean_html("") == ""
    assert clean_html(None) == ""


def test_salary_extractor_matches_brl_formats():
    extractor = SalaryExtractor()
    
    assert extractor.extract("Salário de R$ 5.000") == "R$ 5.000"
    assert extractor.extract("Oferecemos R$8.500,00 + benefícios") == "R$8.500,00"
    assert extractor.extract("Valor: R$ 10.000,00 por mês") == "R$ 10.000,00"
    assert extractor.extract("Não menciona valores") is None


def test_email_extractor_finds_contact():
    extractor = EmailExtractor()
    
    assert extractor.extract("Contato em rh@empresa.com") == "rh@empresa.com"
    assert extractor.extract("Envie para VAGAS@TESTE.COM.BR") == "vagas@teste.com.br"  
    assert extractor.extract("Texto sem e-mail válido @empresa") is None


def test_work_model_extractor_identifies_keywords():
    extractor = WorkModelExtractor()
    
    assert extractor.extract("Vaga 100% Remoto") == "remoto"
    assert extractor.extract("Modelo híbrido de trabalho") == "híbrido"
    assert extractor.extract("Trabalho presencial em São Paulo") == "presencial"
    assert extractor.extract("Horário flexível comercial") is None