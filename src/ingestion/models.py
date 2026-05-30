from pydantic import BaseModel


class VacancyRaw(BaseModel):
    id: str
    title: str
    company: str
    description_html: str
