# LuminaText-ETL & ML Production Platform

LuminaText-ETL is a production-ready, highly modular Data Engineering, Natural Language Processing (NLP), and Machine Learning pipeline built with Python 11, MongoDB, and Docker. This project was specifically engineered to apply, validate, and consolidate the core architectural concepts learned throughout the **AI and Machine Learning Postgraduate Program at PUC Minas**.

The system showcases the complete lifecycle of unstructured text data: from raw web scraping and dynamic URL ingestion to statistical feature engineering, token processing, semantic anchoring, and vector-based machine learning classification. The entire ecosystem is exposed via a high-performance REST API layer powered by FastAPI.

---

## 🛠️ System Architecture & Data Flow

The project leverages a modern **MongoDB** *Schemaless Document Store* architecture, allowing the system to ingest diverse and deeply nested web payloads without rigid database constraints. The pipeline enforces a clean separation of concerns by isolating processing states within the database:

1. **Ingestion & Data Cleansing Zone:** Captures raw content via mock engines or dynamic web scrapers, strips toxic HTML boilerplate using BeautifulSoup/Lxml, and isolates granular metadata (Salaries, Contact Emails, and Work Models) using optimized Regular Expressions (RegEx).
2. **NLP & Feature Engineering Engine:** Runs tokenization, domain-specific stopword filtering, and morphological lemmatization powered by `spaCy` (`pt_core_news_sm`). These lemmatized text structures are mathematically transformed into high-dimensional space arrays using Term Frequency-Inverse Document Frequency (**TF-IDF** Vectorization via `scikit-learn`).
3. **Semantic Classifier Layer:** Moves beyond classic numerical clustering (K-Means) into an unsupervised, anchor-driven inference model. The system calculates the **Cosine Similarity** between incoming document vectors and 25 pre-defined, semantically anchored IT career profiles to automatically classify and route jobs with absolute precision.
4. **Delivery Layer (FastAPI):** Exposes production endpoints for automated ingestion, live data retrieval, and full environment reset capabilities, completely integrated with Pydantic for bulletproof data validation.

```text
[Dynamic URL] 
      │
      ▼
(Web Scraper) ──> [HTML Ingestion] ──> (RegEx Extraction) ──> [Processed Vacancies Store]
                                                                        │
                                                                        ▼
[25 Career Labels] <── (Cosine Similarity) <── (TF-IDF Vectorizer) <── (spaCy Lemmatization)