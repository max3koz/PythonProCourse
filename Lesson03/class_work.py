class PositiveNumber:
	"""
	Дескриптор, який забезпечує, що значення є додатним числом.
	Для rating можна задати максимальне допустиме значення.
	"""
	def __init__(self, max_value: float | None = None):
		self.max_value = max_value
	
	def __set_name__(self, owner, name):
		self.private_name = "_" + name
	
	def __get__(self, obj, objtype=None):
		return getattr(obj, self.private_name)
	
	def __set__(self, obj, value):
		if not isinstance(value, (int, float)) or value <= 0:
			raise ValueError(
				f"{self.private_name[1:]} must be a positive number")
		if self.max_value is not None and value > self.max_value:
			raise ValueError(
				f"{self.private_name[1:]} must not exceed {self.max_value}")
		setattr(obj, self.private_name, value)


class Book:
	"""
	Клас, що представляє книгу з назвою, автором, кількістю сторінок і рейтингом.
	Атрибути pages і rating контролюються дескриптором PositiveNumber.
	"""
	pages = PositiveNumber()
	rating = PositiveNumber(max_value=10)
	
	def __init__(self, title: str, author: str, pages: int, rating: float):
		"""
		Ініціалізує об'єкт книги.

		Args:
		    title (str): Назва книги.
		    author (str): Автор книги.
		    pages (int): Кількість сторінок (додатне число).
		    rating (float): Рейтинг (0 < rating ≤ 10).
		"""
		self.title = title
		self.author = author
		self.pages = pages
		self.rating = rating
	
	def __str__(self) -> str:
		"""Повертає зручне текстове представлення книги."""
		return f"'{self.title}' by {self.author} — {self.pages} pages, rating: {self.rating}/10"
	
	def __eq__(self, other) -> bool:
		"""
		Порівнює книги за назвою та автором.
		Args: other (object): Інший об'єкт для порівняння.
		Returns: bool: True, якщо назва і автор збігаються.
		"""
		return isinstance(other,
		                  Book) and self.title == other.title and self.author == other.author
	
	def __len__(self) -> int:
		"""Повертає кількість сторінок."""
		return self.pages
	
	def __add__(self, other):
		"""
		Додає дві книги, створюючи серію.
		Args: other (object): Інша книга.
		Returns: BookSeries: Об'єкт серії книг.
		"""
		if not isinstance(other, Book):
			return NotImplemented
		return BookSeries([self, other])


class BookSeries:
	"""
	Клас, що представляє серію книг.
	"""
	def __init__(self, books: list[Book]):
		"""
		Ініціалізує серію книг.
		Args: books (list[Book]): Список об'єктів Book.
		"""
		self.books = books
	
	def __str__(self):
		"""Повертає строкове представлення серії."""
		titles = ", ".join(book.title for book in self.books)
		return f"Book Series: {titles}"
	
	def __len__(self):
		"""Повертає загальну кількість сторінок у серії."""
		return sum(len(book) for book in self.books)


book1 = Book("Title1", "Maksym1", 300, 9.5)
book2 = Book("Title2", "Maksym2", 250, 8.8)
book3 = Book("Title3", "Maksym3", 350, 9.5)

print(book1)
print(book2)
print(book3)

series = book1.title + book2.title
print()
print(f"{series} - total pages: {len(series)}")

