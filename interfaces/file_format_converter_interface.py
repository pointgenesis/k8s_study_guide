import logging

from abc import ABC, abstractmethod


class FileFormatConverter(ABC):

    @abstractmethod
    def convert(self) -> None:
        pass
