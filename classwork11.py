# შექმენით ფუნქცია generate_student, რომელსაც გადაეცემა პარამეტრად რიცხვი.
# და faker მოდულის გამოყენებით აგენერირებს სტუდენტის ინფორმაციას და აბრუნებს
# დიქტის სახით, მაგ: 
# {
#     "ID": (რა რიცხვიც გადაეცა პარამეტრად),
#     "first_name": "John",
#     "last_name": "Doe",
#     "age": 25
# }

# რათქმაუნდა სახელები და გვარები ხელით არ უნდა ჩამოწეროთ!
# ასაკი უნდა იყოს 18-დან 80-წლამდე შუალედში შემთხვევითი პრინციპით.

# შექმენით მეორე ფუნქცია generate_students, რომელსაც გადაეცემა რიცხვი  და დააბრუნებს ლისტს, 
# რომელშიც იმდენი ელემენტი იქნება, რა რიცხვიც გადაეცა ფუნქციას, ხოლო ელემენტები უნდა იყოს
# პირველი ფუნქციის ანუ generate_student-ის მიერ დაბრუნებული მნიშვნელობები.
# ყურადღება მიაქციეთ იმას, რომ ამ ლისტში არსებული დიქტის აიდები უნდა იწყებოდეს 1-დან და ავტომატურად იზრდებოდეს 1-ით!

# აუცილებლად გამოიყენეთ type hinting ფუნქციებზე!

from faker import Faker
from random import randint

fake = Faker()

def generate_student(id: int) -> dict[str,any]:

    fake_dict = {
        "ID": id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": randint(18, 80)
    }

    return fake_dict

def generate_students(number: int) -> list[dict[str, any]]:

    return [generate_student(n) for n in range(1, number + 1)]

for student in generate_students(4):
    print(student)
