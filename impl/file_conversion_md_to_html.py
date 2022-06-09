import os
import markdown
import shutil
import logging
from interfaces.file_format_converter_interface import FileFormatConverter
from utilities.file_utilities import FileUtils

log = logging.getLogger(f'__main__.{__name__}')


class MarkdownToHtml(FileFormatConverter):

    def __init__(self, verbose=False):
        super().__init__()
        if verbose:
            log.setLevel(logging.DEBUG)
        log.debug(f'Initializing {self.__class__.__name__}')

    def convert(self) -> None:
        """Convert all files in the markdown directory to html files"""

        # additional information about the PWD/CWD during debugging
        if log.isEnabledFor(logging.DEBUG):
            current_directory = os.getcwd()
            log.debug(f'current working directory: {current_directory}')

        # 1. get the directory where the current file exists
        file_path = os.path.dirname(os.path.realpath(__file__))
        log.info(f'current file directory: {file_path}')

        # 2. reference the html directory where generated output is stored
        html_file_path = os.path.join(file_path, '../html')

        # 3. delete the html directory and all contained files and directories
        FileUtils.delete_files_from_directory(html_file_path, True)

        # 4. get markdown data
        markdown_file_path = os.path.join(file_path, '../markdown/docs')
        log.debug(f'{os.listdir(markdown_file_path)}')
        files = [obj for obj in os.listdir(markdown_file_path) if os.path.isfile(f'{markdown_file_path}/{obj}')]

        for file in files:
            file_path = f'{markdown_file_path}/{file}'
            log.debug(f'Examining file: {file_path}')
            with open(file_path, 'r') as f:
                markdown_data = f.read()
                # 5. convert markdown to html
                html_data = markdown.markdown(markdown_data)

            file_path = f"{html_file_path}/{file.replace('.md', '.html')}"
            log.debug(f'Writing file: {file_path}')
            with open(file_path, 'w') as f:
                # 6. save html in the html directory
                f.write(html_data)

        # 7. copy the markdown/images folder to html/images
        images_file_path = os.path.join(file_path, '../markdown/images')
        TODO....

# References:
# [1] https://www.geeksforgeeks.org/python-read-file-from-sibling-directory/
# [2] https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-
# [3] https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# [4] https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-to-convert-markdown-text-to-html
# [5] https://www.geeksforgeeks.org/python-os-path-isfile-method/?ref=lbp
