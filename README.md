# LuminaText ETL: Intelligent Text Analytics Hub

LuminaText ETL is a production-ready, modular Data Engineering and Natural Language Processing (NLP) pipeline built with Python, MongoDB, and Docker. This project was specifically designed to apply, test, and consolidate the core concepts learned throughout the **AI and Machine Learning Postgraduate Program at PUC Minas**.

The system showcases the complete lifecycle of text data: from raw web scraping and unstructured NoSQL data ingestion to statistical vectorization, semantic embeddings, and machine learning classification. The architecture is strictly structured around the official NLP pipeline models taught in the curriculum.

---

## 🛠️ System Architecture & Data Flow

The project leverages **MongoDB** to implement a modern *Schemaless Document Store* architecture. This allows the ingestion of highly diverse web data structures without rigid schema constraints. The data is segregated into two logical collections within the `lumina_db` database:

1. **Raw Storage (`raw_content`):** Acts as a Landing Zone/Data Lake, storing un-indexed HTML, metadata, and raw text payloads directly from web crawlers.
2. **Processed Storage (`processed_content`):** Stores normalized text, granular metadata extracted via Regex, and token arrays optimized for Machine Learning models.

```text
[Web Sources] ──(Scraper)──> [raw_content (BSON)] ──(Cleaning & RegEx)──> [processed_content] ──(NLP Pipeline)──> [Tokens/Features]
