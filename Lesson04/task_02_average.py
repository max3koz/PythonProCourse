from typing import List

class FileProcessingError(Exception):
    """
    Base exception class for errors encountered during file processing.

    This class can be extended to represent specific issues such as:
    - File not found
    - Non-numeric data
    - Empty file
    """
    def __init__(self, message: str = "An error occurred while processing the file.") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

class NonNumericDataError(FileProcessingError):
    """
    Raised when non-numeric data is found in the file.
    """
    def __init__(self, line_number: int, content: str) -> None:
        message = f"Non-numeric data on line {line_number}: '{content}'"
        super().__init__(message)

class EmptyFileError(FileProcessingError):
    """
    Raised when the file is empty or contains no valid numbers.
    """
    def __init__(self) -> None:
        super().__init__("The file is empty or contains no valid numbers.")

class NumberFileProcessor:
    """
    Reads numeric data from a file and computes the arithmetic mean.
    """
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.numbers: List[float] = []

    def read_numbers(self) -> None:
        """
        Reads and parses numeric values from the file.
        Raises appropriate exceptions for errors.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    stripped = line.strip()
                    if not stripped:
                        continue  # skip empty lines
                    try:
                        number = float(stripped.replace(",", "."))
                        self.numbers.append(number)
                    except ValueError:
                        raise NonNumericDataError(line_number, stripped)
        except FileNotFoundError:
            raise FileProcessingError(f"File '{self.filename}' not found.")

    def calculate_average(self) -> float:
        """
        Calculates the arithmetic mean of the parsed numbers.
        """
        if not self.numbers:
            raise EmptyFileError()
        return sum(self.numbers) / len(self.numbers)

def average_calculator() -> None:
    """
    Entry point for the program.
    """
    print("File Average calculator!!!")
    print("Type 'quit' to exit at any time.\n")
    
    while True:
        filename = input("Enter the filename: ")
        if filename.lower() == "quit":
            print("See you later!!!")
            break
	    
        processor = NumberFileProcessor(filename)
	
        try:
            processor.read_numbers()
            average = processor.calculate_average()
            print(f"Average for '{filename}': {average:.2f}\n")
        except FileProcessingError as e:
            print(f"Error: {e}")
            print("You can try again or type 'quit' to exit.\n")
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("You can try again or type 'quit' to exit.\n")


average_calculator()