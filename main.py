import logging
from file_format_converter_factory import FileFormatConverterFactory
from file_conversion_type import FileConversionType

log = logging.getLogger('__name__')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class Main:
    """
    References:
    [1] Logging, https://realpython.com/python-logging/
    [2] ArgumentParser, https://docs.python.org/3/library/argparse.html
    [3] Virtual Environment, https://realpython.com/python-virtual-environments-a-primer/
    [4] Markdown to HTML, https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-to-convert-markdown-text-to-html
    [5] Factory Pattern, https://realpython.com/factory-method-python/
    [6] Python Interface, https://realpython.com/python-interface/
    """

    def __init__(self) -> None:
        pass


def main() -> None:
    log.setLevel(logging.DEBUG)
    log.debug('test')
    file_format_converter_factory = FileFormatConverterFactory(True)
    file_format_converter = file_format_converter_factory.get_file_format_converter(FileConversionType.MD_TO_HTML)
    file_format_converter.convert()


if __name__ == "__main__":
    main()
