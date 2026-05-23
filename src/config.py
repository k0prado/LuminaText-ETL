from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
ENV_PATH: Final[Path] = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

MONGO_INITDB_ROOT_USERNAME: Final[str] = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_INITDB_ROOT_PASSWORD: Final[str] = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "secret_password")
MONGO_URI: Final[str] = os.getenv(
    "MONGO_URI",
    f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/",
)
DATABASE_NAME: Final[str] = os.getenv("DATABASE_NAME", "lumina_text_etl")
