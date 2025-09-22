class FileProcessor:
    """A class for writing and reading text files."""

    @staticmethod
    def write_to_file(file_path: str, data: str) -> None:
        """
        Writes a string to a file.
        Args:
            file_path (str): path to the file
            data (str): text to write
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """
        Reads the contents of a file as a string.
        Args: file_path (str): path to the file
        Returns: str: contents of the file
        Raises: FileNotFoundError: if the file does not exist
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
