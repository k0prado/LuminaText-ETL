import spacy
from typing import Any


class SpacyModelLoader:
    _model: Any | None = None

    @classmethod
    def get_model(cls, model_name: str = "pt_core_news_sm") -> Any:
        """Load and cache a spaCy model to avoid repeated loads.

        Returns a spaCy Language object.
        """
        if cls._model is None:
            cls._model = spacy.load(model_name)
        return cls._model
