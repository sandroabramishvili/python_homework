# 1. შექმენით მთელი რიცხვების მინიმუმ 5 ელემენტიანი სია, გამოთვალეთ ყველა რიცხვის ჯამი და საშუალო, არ გამოიყენოთ ჩაშენებული ფუნქციები!

print("Please create a list of integers consisting of a minimum of 5 elements")
int_list = [int(i) for i in input("Enter the integers separated by spaces: ").split()]
total = 0
for count, num in enumerate(int_list, start=1):
    total += num

print(f"The sum is {total}")
print(f"The average is {round(total/count, 2)}")
print("---------------------------------------------------------")

# -----------------------------------------------------------------------------------------------------------------------------

# 2. მოცემულია სია ['a', 'b', 2, 4, 2, 'c', 'j', 1, 'b', 'd', 'c', 4, 1], დაწერეთ ლოგიკა, როემლიც ამ ლისტში დატოვებს უნიკალურ
# ელემენტებს, ანუ არ განმეორდება ელემენტები. არ გამოიყენოთ set!

given_list = ['a', 'b', 2, 4, 2, 'c', 'j', 1, 'b', 'd', 'c', 4, 1]
print(f"Here's the given list: {given_list}")

# ახალი ლისტის შექმნით გამოთვლა:

unique_list = []

for character in given_list:
    if character not in unique_list:
        unique_list.append(character)

print(f"Here's the unique list: {unique_list}")

# არსებული ლისტში ცვლილებით გამოთვლა:

i = 0
while i < len(given_list):
    item = given_list[i]
    
    if given_list.index(item) < i:
        given_list.pop(i)
    else:
        i += 1

print(f"Here's the unique list: {given_list}")
print("-----------------------------------------------------------")

# -----------------------------------------------------------------------------------------------------------------------------

# 3. დააგენერირეთ 20 ელემენტიანი რიცხვების სია, რომელიც შევსებული იქნება -50 დან 50-მდე შემთხვევითი რიცხვებით და შექმენით მეორე 
# სია, რომელიც პირველი სიიდან იქნება შევსებული მხოლოდ ლუწი რიცხვებით და დაბეჭდეთ ორივე სია.

from random import randint

int_list = [randint(-50, 50) for _ in range(20)]
even_int_list = [i for i in int_list if i % 2 == 0]
print(f"Original List: {int_list}")
print(f"Even List: {even_int_list}")
print("---------------------------------------------------------")

# -----------------------------------------------------------------------------------------------------------------------------

# 4. მოცემულია სია:

# (სახელი, გვარი, ასაკი)

persons = [
    ('Kelly', 'Simpson', 26),
    ('Erika', 'Stephens', 24),
    ('Cheryl', 'Dunn', 30),
    ('Amy', 'Larsen', 49),
    ('Christine', 'Gordon', 23),
    ('Monica', 'Huff', 38),
    ('David', 'Nixon', 36),
    ('Cindy', 'Escobar', 41),
    ('Cindy', 'White', 33), 
    ('Joel', 'Hall', 43),
    ('Steven', 'Winters', 28),
    ('Alex', 'Cole', 68),
    ('Alex', 'Smith', 32),
    ('Alex', 'White', 42),
    ('Brittany', 'Thompson', 18),
    ('Ernest', 'Young', 43),
    ('Traci', 'Wells', 38),
    ('Andrew', 'Flores', 61),
    ('Christopher', 'Lewis', 29),
    ('Kevin', 'Willis', 57),
    ('Kayla', 'Lucas', 28),
    ('Michelle', 'Rush', 43),
    ('Thomas', 'Mason', 37)
]

# დაწერეთ უსასრულო ციკლი, რომელშიც მომხმარებელს ჰკითხავთ სახელს, თუ სახელი იქნება მოცემულ სიაში, შემდეგ ჰკითხეთ გვარი და გვარიც თუ იქნება,
# დაბეჭდეთ მისი ასაკი, ხოლო თუ არ იქნება სახელი დაბეჭდეთ რომ არ არის მოცემული სახელი, შესაბამისად გვარი აღარ ჰკითხოთ, ანალოგიურად
# მოიქეცით გვარის კითხვის შემთხვევაშიც. ციკლი უნდა გაჩერდეს იმ შემთხვევაში თუ მომხმარებელი შემოიყვანს სიტყვას "stop".

while True:
    name = input("Enter name: ").capitalize()

    if name == 'Stop':
        break

    available_last_names = [entry[1] for entry in persons if entry[0] == name]

    if available_last_names:
        last_name = input("Enter last name: ").capitalize()
        if last_name in available_last_names:
            for entry in persons:
                if (entry[0], entry[1]) == (name, last_name):
                    print(f"{name} {last_name} is {entry[2]} years old.")
                    print("---------------------------------------------------------")
                    break
        else:
            print(f"'{name} {last_name}' is not in our system.")
            print("---------------------------------------------------------")
    else:
        print(f"'{name}' is not in our system.")
        print("---------------------------------------------------------")