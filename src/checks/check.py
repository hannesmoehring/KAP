from abc import ABC, abstractmethod

class Check(ABC):
    @abstractmethod
    def run_check(self, df):
        pass
