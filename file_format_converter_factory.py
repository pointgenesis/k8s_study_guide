import os
import logging

from file_conversion_type import FileConversionType
from interfaces.file_format_converter_interface import FileFormatConverter
from impl.file_conversion_md_to_html import MarkdownToHtml

log = logging.getLogger(f'__main__.{__name__}')


class FileFormatConverterFactory:

    def __init__(self, verbose=False) -> None:
        self.verbose = verbose
        if self.verbose:
            log.setLevel(logging.DEBUG)
        log.info(f'Initializing {self.__class__.__name__}')

    def get_instance(self, conversion_type: FileConversionType) -> FileFormatConverter:
        if conversion_type == FileConversionType.MD_TO_HTML:
            log.info(f'{conversion_type} is a supported conversion type.')
            # current_directory = os.path.abspath(__file__)
            # log.debug(f'{current_directory}')
            return MarkdownToHtml(self.verbose)
        else:
            raise IOError(f'{conversion_type} is not a supported conversion type.')



