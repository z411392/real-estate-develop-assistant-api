from abc import ABCMeta, abstractmethod
from uuid import uuid5, UUID, uuid1
from os import getenv


class Event(metaclass=ABCMeta):
    @abstractmethod
    def type(self) -> str:
        return NotImplemented

    @abstractmethod
    def data(self) -> dict:
        return NotImplemented

    def id(self):
        projectId = UUID(getenv("PROJECT_UUID"))
        namespace = uuid5(projectId, self.type())
        return str(uuid5(namespace, str(uuid1())))
