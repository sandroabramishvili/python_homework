# 1. დაწერეთ პროგრამა, რომელიც მომხმარებელს უსასრულოდ შეეკითხება ჯერ სახელს, შემდეგ გვარს და რაიმე ფაილში ჩაწერს 
#    სახელს და გვარს ერთ ხაზზე თავისი ნუმერაციით, ყველა ახალი სახელი და გვარი უნდა იყოს ახალ ხაზზე ჩაწერილი, მაგალითად:
   
#    Enter your first name: Otar
#    Enter your last name: Tumanishvili
#    Enter your first name: Nika
#    Enter your last name: Papaskiri
#    Enter your first name: stop

#    ფაილში უნდა ჩაიწეროს შემდეგი სახით:
#    1. Otar Tumanishvili
#    2. Nika Papaskiri

#    პროგრამა ჩერდება იმ შემთხევაში, თუ მომხმარებელმა სახელის ადგილას შეიყვანა სიტყვა stop

counter = 1

with open("names.txt", "w", encoding="utf-8") as file:
    while True:
        first_name = input("Enter your first name: ")
        
        if first_name.lower() == "stop":
            break
        
        last_name = input("Enter your last name: ")
        
        file.write(f"{counter}. {first_name} {last_name}\n")
        counter += 1

# 2. თანდართულ ფაილში "persons.txt" მოცემულია ადამიანების სია შემდეგი ფორმატით:
#    სახელი და გვარი, ასაკი, ქალაქი

#    Evelyn Cook, 75, Nixonland
#    Dr. Briana Davidson, 22, South Hunterside
#    ...
#    ...

#    თქვენი დავალებაა არსებული ფაილიდან წაიკითხოთ ინფორმაცია, შექმნათ ორი ახალი ტექსტური ფაილი (.txt გაფართოებით), ერთ ფაილში
#    ჩაწერეთ ყველა პიროვნება რომლის ასაკი ნაკლებია 50-ზე, ხოლო მეორე ფაილში ჩაწერეთ ყველა პიროვნება, რომლის ასაკი მეტია 50-ზე,
#    ფორმატი დაცული უნდა იყოს ისეთი სახით, როგორიც არის ორიგინალ "persons.txt" ფაილში ანუ თითო პიროვნება თითო ხაზზე!

with open("persons.txt", "r", encoding="utf-8") as main_file, \
     open("younger.txt", "w", encoding="utf-8") as younger_file, \
     open("older.txt", "w", encoding="utf-8") as older_file:

    for line in main_file:
        line = line.strip()
        
        line = line.split(",")
        
        name = line[0].strip()
        age = int(line[1].strip())
        city = line[2].strip()
        
        formatted_line = f"{name}, {age}, {city}\n"
        
        if age < 50:
            younger_file.write(formatted_line)
        elif age >= 50:
            older_file.write(formatted_line)

   
# 3. დაწერეთ ფუნქცია, რომელიც ატრიბუტად მიიღებს რიცხვს, რა რიცხვსაც გადავცემთ, იმდენჯერ შეეკითხება მომხმარებელს 
#    სახელს, გვარს და ასაკს. ანუ თუ გადავეცით 3, 3-ჯერ შეეკითხება მომხმარებელს აღნიშნულ ინფორმაციას, ინფუთის 
#    საფუძველზე csv ფაილში ჩაწერეთ შესაბამისი ინფორმაცია შემდეგი სახით, მაგალითად:

#    ID,first_name,last_name,age
#    1,John,Doe,25
#    2,Alice,White,30

#    და ა.შ.
   
#    გამოიყენეთ try, ecxept იმისათვის რომ მომხმარებელმა ასაკის შემოყვანის დროს აუცილებლად ინტეჯერი შემოიყვანოს!
#    ფაილში ჩასაწერად აუცილებლად გამოიყენეთ csv მოდულიდან DictWriter!

import csv

def csv_func(num):
    with open("people.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["ID", "first_name", "last_name", "age"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for id in range(1, num + 1):
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            
            while True:
                try:
                    age = int(input("Enter age: "))
                except ValueError:
                    print("You need to enter an integer")
                else:
                    break

            writer.writerow({
                "ID": id,
                "first_name": first_name,
                "last_name": last_name,
                "age": age
            })

csv_func(2)

# 4. მიმაგრებულ students.csv ფაილიდან წაიკითხეთ ინფორმაცია, გაფილტრეთ Grade-ის მიხედვით შემდეგნაირად:
#    ყველა სტუდენტი, რომელსაც 50-ზე ნაკლები ქულა აქვს შეინახეთ ახალ ფაილში(failed_students.csv)
#    ყველა სტუდენტი, რომელსაც 50-ზე მეტი ქულა აქვს შეინახეთ ახალ ფაილში(passed_students.csv)

#    ფაილებიდან ინფორმაციის წასაკითხად და ჩასაწერად აუცილებლად გამოიყენეთ DictReader და DictWriter!

import csv

with open("students.csv", "r", encoding="utf-8") as students_file, \
     open("failed_students.csv", "w", newline="", encoding="utf-8") as failed_file, \
     open("passed_students.csv", "w", newline="", encoding="utf-8") as passed_file:

    reader = csv.DictReader(students_file)
    fieldnames = reader.fieldnames

    failed_writer = csv.DictWriter(failed_file, fieldnames=fieldnames)
    passed_writer = csv.DictWriter(passed_file, fieldnames=fieldnames)

    failed_writer.writeheader()
    passed_writer.writeheader()

    for row in reader:
        grade = int(row["Grade"])
        
        if grade < 50:
            failed_writer.writerow(row)
        elif grade > 50:
            passed_writer.writerow(row)
