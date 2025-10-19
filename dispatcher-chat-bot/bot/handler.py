from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict) -> bool: ...

    @abstractmethod
    def handle(self, update: dict) -> bool:
        """
        return options:
        - true - signal for dispather to continue processing
        - false - signal for dispather to STOP processing
        """
        pass
