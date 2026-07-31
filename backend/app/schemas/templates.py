from pydantic import BaseModel


class TemplateGenerateBody(BaseModel):
    template: dict | None = None
    use_ai: bool = False
    seed: int | None = None
