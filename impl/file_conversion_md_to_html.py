import os
import shutil
import logging
from interfaces.file_format_converter_interface import FileFormatConverter

log = logging.getLogger(f'__main__.{__name__}')


class MarkdownToHtml(FileFormatConverter):

    def __init__(self, verbose=False):
        super().__init__()
        if verbose:
            log.setLevel(logging.DEBUG)
        log.debug(f'Initializing {self.__class__.__name__}')

    def convert(self) -> None:
        """Convert all files in the markdown directory to html files"""

        # log.debug(f"Invoking {self.__class__.__name__}.{self.convert.__name__}")

        current_directory = os.getcwd()
        log.info(f'current working directory: {current_directory}')

        file_path = os.path.dirname(os.path.realpath(__file__))
        log.info(f'current file directory: {file_path}')

        # https://www.geeksforgeeks.org/python-read-file-from-sibling-directory/ <<<<<<<<<<<<<<<<<<<<<<<<<<<< Read 

        # shutil.rmtree()
        # 1. delete the html directory and all contained files and directories
        # 2. iterate through the files in the markdown directory
        # 3. convert to text
        # 4. convert to markdown
        # 5. save as html file in the html directory
        # 6. copy the markdown/images folder to html/images


        # with open(source_path, 'r') as f:
        #     text = f.read()

        #     html = markdown.markdown(text)
        #
        # with open()
        pass

