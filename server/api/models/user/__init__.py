from server.api.models._base import Model


class User(Model):
    id: str | None
    name: str
    email: str
    grad_year: int
    concentration: str | None
    certificates: list[str]
