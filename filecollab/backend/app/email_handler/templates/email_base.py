from abc import ABC, abstractmethod


class EmailBase(ABC):
    @staticmethod
    @abstractmethod
    def check_args(args: dict):
        pass

    @property
    @abstractmethod
    def html(self) -> str:
        pass

    @property
    @abstractmethod
    def subject(self) -> str:
        pass
