import json

from typing import Any, Dict, List


class BookManager:
	""""""
	
	def __init__(self, file_name: str) -> None:
		""""""
		self.file_name = file_name
	
	def load_book(self) -> List[Dict[str, Any]]:
		""""""
		try:
			with open(self.file_name, mode="r", encoding="utf-8") as file:
				return json.load(file)
		except FileNotFoundError:
			return []
	
	def show_available_books(self) -> None:
		""""""
		books = self.load_book()
		available_books = [book for book in books if
		                   book.get("availability", False)]
		print("Available books:")
		for book in available_books:
			print(f"- {book['Title']} {book['Author']} {book['year']}")
	
	def add_book(self, title: str, author: str, year: int,
	             available: bool) -> None:
		""""""
		books = self.load_book()
		
		for book in books:
			if book["Title"].strip().lower() == title.strip().lower() and \
					book["Author"].strip().lower() == author.strip().lower():
				print(f"The '{title}' book of '{author}' is exist "
				      f"in the data base.")
				return
		
		new_book = {"Title": title, "Author": author,
		            "year": year, "availability": available}
		books.append(new_book)
		
		with open(self.file_name, mode="w", encoding="utf-8") as file:
			json.dump(books, file, ensure_ascii=False, indent=4)
		print(f"Added the '{title}' book")


manager = BookManager("task_04_book_list.json")

manager.show_available_books()

manager.add_book("Книга 3", "Автор 3", 2021, True)
