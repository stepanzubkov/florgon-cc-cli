"""
    Differents services for working with files.
"""
from typing import List
from io import TextIOWrapper


def concat_files(files: List[TextIOWrapper]) -> str:
    """
    Read files and concatenate them, like `cat` utility from GNU Coreutils.
    :param List[TextIOWrapper] files: list of files, opened for reading (with mode 'r')
    :return: concatenated files
    :rtype: str
    """
    return "".join(file.read() for file in files)
