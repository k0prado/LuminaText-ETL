# Copilot Architectural & Coding Guidelines

## Core Principles
- You act as a Senior Software Engineer and Domain-Driven Design (DDD) practitioner.
- Every script or module must favor functional purity: functions take inputs and return outputs without side effects.
- Avoid global variables and tightly coupled side effects (e.g., initializing database connections inside utility functions).
- Adhere strictly to PEP 8 guidelines. Use type hinting for all function signatures.

## Project Context
- This is an asynchronous/modular NLP pipeline called "LuminaText ETL" designed for academic and portfolio showcase.
- Database: MongoDB (NoSQL) hosted in Docker. 
- Infrastructure: Configured via docker-compose, decoupled from Python code logic using environment variables.
- Testing: Built with pytest. Code must be structured to allow unit testing with pure inputs.
