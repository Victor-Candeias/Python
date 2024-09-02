from abc import ABC, abstractmethod

class BaseInputPlugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the plugin"""
        pass

    @abstractmethod
    def process_input(self, data):
        """Process the input data"""
        pass
