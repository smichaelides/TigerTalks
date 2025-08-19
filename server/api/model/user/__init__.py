from server.api.model._base import Model


class User(Model):
    name: str
    grad_year: int
