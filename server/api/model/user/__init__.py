from server.api.model._base import Model


class User(Model):
    name: str
    email: str
    grad_year: int
    concentration: str | None
    certificates: list[str]
