from typing import Any, Protocol

from ceramics import model

DataObject = dict[str, Any]


class Repository(Protocol):
    def add(self, model_instance) -> None:
        ...

    def get(self, id) -> Any:
        ...


class SQLAlchemyRepository:
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class

    def add(self, instance) -> None:
        self.session.add(instance)

    def get(self, id: int):
        return self.session.query(self.model_class).filter_by(id=id).one()

    def list(self):
        return self.session.query(self.model_class).all()


class FakeRepository:
    def __init__(self, model_class):
        self.storage = set()
        self.model_class = model_class

    def add(self, instance) -> None:
        self.storage.append(instance)

    def get(self, id: int):
        return next(instance for instance in self.storage if instance.id == id)

    def list(self):
        return self.storage
