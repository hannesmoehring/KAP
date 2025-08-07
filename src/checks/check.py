from abc import ABC, abstractmethod

from src.types import GenericResponse


class Check(ABC):
    @abstractmethod
    def run_check(self, df) -> GenericResponse:
        pass
