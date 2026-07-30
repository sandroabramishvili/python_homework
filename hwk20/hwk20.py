# 1. გვაქვს შემდეგი კლასი და ინსტანსი:

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: ({self.name}, {self.age})"

p1 = Person("Otar", 35)

# დაწერეთ სერიალაიზერ ფუნქცია, რომელიც დაგეხმარებათ არსებული კლასის ობიექტი გადააქციოთ ისეთ ობიექტად,
# რომ შემდეგ ტექსტურ ფაილში ჩაწეროთ შემდეგი სტრუქტურით:
# Name: Otar, Age: 35

# რათქმაუნდა ჩაწერეთ ფაილში.

def serializer(data: Person):
    if isinstance(data, Person):
        return f"Name: {data.name}, Age: {data.age}"
    return "Not a Person instance"

serialized_data = serializer(p1)
with open("person.txt", "w") as f:
    f.write(serialized_data)

# არსებული ფაილიდან წაიკითხეთ ინფორმაცია.

# ასევე დაწერეთ დესერიალაიზერ ფუნქცია, რომელიც ზემოაღნიშნული სტრუქტურის ფაილიდან წაკითხულ ინფორმაციას აქცევს ისევ 
# Person კლასის ობიექტად.(ჩათვალეთ რომ მხოლოდ ერთ ხაზს წერთ ფაილში და წაკითხვითაც ერთ ხაზს კითხულობთ)

with open("person.txt", "r") as f:
    line = f.readline().strip()

def deserializer(line: str) -> Person:
    name_part, age_part = line.split(", ")
    name = name_part.split(": ")[1]
    age = int(age_part.split(": ")[1])
    return Person(name, age)

deserialized_person = deserializer(line)
print(deserialized_person)

# 2. მოცემულია persons.json ფაილი შემდეგი სტრუქტურით:
# [
#     {
#         "id": 1,
#         "name": "Ana",
#         "age": 19
#     },
#     {
#         "id": 2,
#         "name": "Bob",
#         "age": 21
#     }
# ]

# თქვენი დავალებაა დაწეროთ ფუნქცია, რომელსაც პარამეტრად გადაეცემა რიცხვი და გადაცემული რიცხვის საფუძველზე 
# იმდენჯერ ჰკითხავს მომხმარებელს სახელს და ასაკს, შემდეგ კი persons.json ფაილში დაამატებს ახალ პერსონებს
# თავისივე აიდებით.მაგალითად, ორჯერ ვეკითხებით მომხმარებელს:

# enter your name: Walter
# enter your age: 45
# enter your name: Niko
# enter your age: 32

# persons.json უნდა გამოიყურებოდეს შემდეგნაირად:

# [
#     {
#         "id": 1,
#         "name": "Ana",
#         "age": 19
#     },
#     {
#         "id": 2,
#         "name": "Bob",
#         "age": 21
#     },
#     {
#         "id": 3,
#         "name": "Walter",
#         "age": 45
#     },
#     {
#         "id": 4,
#         "name": "Niko",
#         "age": 32
#     }
# ]

# გაითვალისწინეთ! არ უნდა დაირღვეს json ფაილის სტრუქტურა, ანუ პერსონები უნდა იყოს ლისტში, ლისტის გარეთ არ ჩაამატოთ!
# ასევე, აიდები უნდა გაგრძელდეს ბოლო აიდის მქონე პერსონის შემდეგ ლოგიკურად, ანუ json ფაილში თუ ბოლო პერსონის აიდი იქნება 2, 
# ახალი პერსონის დამატებისას აიდი უნდა იყოს 3, თუ ბოლო პერსონის აიდი იქნება 5, ახალი პერსონის უნდა იყოს 6 და ასე შემდეგ!

import json

def add_persons_to_json(num_persons: int):
    with open("persons.json", "r") as f:
        persons = json.load(f)

    for _ in range(num_persons):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))

        if persons:
            new_id = max(person["id"] for person in persons) + 1
        else:
            new_id = 1

        new_person = {
            "id": new_id,
            "name": name,
            "age": age
        }

        persons.append(new_person)

    with open("persons.json", "w") as f:
        json.dump(persons, f, indent=4)

num_persons = int(input("How many persons do you want to add? "))
add_persons_to_json(num_persons)
