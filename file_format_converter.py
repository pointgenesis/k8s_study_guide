import logging
from file_conversion_type import FileConversionType

log = logging.getLogger(f'__main__.{__name__}')


class FileFormatConverter:

    def __init__(self, conversion_type: FileConversionType) -> None:
        log.info(f'Initializing {self.__class__.__name__} as {conversion_type}')
        pass
