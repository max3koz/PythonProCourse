from pymongo import MongoClient


# connected MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["university"]
students = db["students"]

# Add 5 students
students.insert_many([
    { "name": "Олександр Іванов", "age": 21, "phone": "+380501234567" },
    { "name": "Марія Коваль", "age": 19, "phone": "+380671112233" },
    { "name": "Ігор Сидоренко", "age": 22, "phone": "+380931234567" },
    { "name": "Наталія Шевченко", "age": 20, "phone": "+380661112233" },
    { "name": "Дмитро Бондар", "age": 23, "phone": "+380991234567" }
])

# Output all students
for student in students.find():
    print(student)
    
    
    
