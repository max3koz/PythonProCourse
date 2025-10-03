from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["libraru_db"]

authors = db["Authors"]
books = db["Books"]

authors.delete_many({})
books.delete_many({})

authors.insert_many([
	{"name": "Autor_1", "country": "Country_1"},
	{"name": "Autor_2", "country": "Country_2"},
	{"name": "Autor_3", "country": "Country_3"},
	{"name": "Autor_4", "country": "Country_"},
	{"name": "Autor_5", "country": "Country_2"}
])

books.insert_many([
	{"title": "title_1", "author": "Autor_3", "genre": "History", "year": 2011},
	{"title": "title_2", "author": "Autor_1", "genre": "Comedy", "year": 2013},
	{"title": "title_3", "author": "Autor_2", "genre": "Drama", "year": 1999}
])

print("Authors:")
for author in authors.find():
	print(author)

print("Books:")
for book in books.find():
	print(book)
