import logging
import os
import shutil
import logging

log = logging.getLogger(f'__main__.{__name__}')


class FileUtils:

    def __init__(self) -> None:
        log.warning(f'Initializing a static class -> {self.__class__.__name__}')

    @staticmethod
    def delete_files_from_directory(directory_name: str, verbose=False):
        log.setLevel('DEBUG') if verbose else log.setLevel('INFO')

        log.debug(f'About to delete all files and directories under {directory_name}')
        for file in os.listdir(directory_name):
            path = os.path.join(directory_name, file)
            log.debug(f'Attempting to remove directory tree: {path}')
            try:
                shutil.rmtree(path)
                log.info(f'Removed directory tree: {path}')
            except OSError:
                try:
                    os.remove(path)
                    log.info(f'Removed file: {path}')
                except OSError as e:
                    log.warning("Unable to remove object at {}", path, e)
