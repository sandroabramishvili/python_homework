# 1. დაწერეთ პროგრამა, რომელიც შექმნის დიქტს, რომელშიც key-ები იქნება 1-დან 10-ის ჩათვლით რიცხვები, ხოლო value-ები key-ს შესაბამისი
#    კვადრატები, ანუ {1: 1, 2: 4, 3: 9...}, არ დაწეროთ ხელით, გამოიყენეთ ციკლი(ბონუსი: გამოიყენეთ dictionary comprehension )

squared_dict = {n:n**2 for n in range(1,11)}
print(squared_dict)

# ---------------------------------------------------------------------------------------------------------------------------

# 2. მოცემულია პროდუქტების ლისტი:
products = [
    {"cola": {
        "price": 1.5,
        "quantity": 10
    }},
    {"fanta": {
        "price": 2.5,
        "quantity": 5
    }},
    {"snickers": {
        "price": 3.5,
        "quantity": 12
    }},
    {"water": {
        "price": 4.5,
        "quantity": 8
    }},
    {"beer": {
        "price": 6.5,
        "quantity": 5
    }}
]

# ა. დაბეჭდეთ ყველა პროდუქტის დასახელება

print("Here is the list of the products:")

for entry in products:
    for product in entry:
        print(product)

# ბ. გამოითვალეთ ყველა პროდუქტის ღირებულების ჯამი(ანუ პროდუქტის ფასი უნდა გაამრავლოთ რაოდენობაზე და დააჯამოთ)

total = 0

for entry in products:
    for product, details in entry.items():
        total += details["price"] * details["quantity"]

print(f"The total value of the products is ${total:.2f}")

# ---------------------------------------------------------------------------------------------------------------------------

# 3. დაწერეთ პროგრამა, რომელიც მომხმარებელს შეეკითხება ხილის სახელს, მანამ სანამ, მომხმარებელი არ შეიყვანს სიტყვას stop,
#    ამის შემდეგ გამოიტანეთ დიქტის სახით ხილის დასახელება და ველიუ იქნება რამდენჯერაც შეიყვანა ეს ხილი, მაგალითად:

#    Enter your favorite fruit: banana
#    Enter your favorite fruit: apple
#    Enter your favorite fruit: banana
#    Enter your favorite fruit: stop

# შედეგი:

# {'banana': 2, 'apple': 1}

fruits = []

while True:
    fruit = input("Enter your favorite fruit: ").lower()
    if fruit == "stop":
        fruits_dict = {f:fruits.count(f) for f in fruits}
        print(fruits_dict)
        break
    fruits.append(fruit)

# ---------------------------------------------------------------------------------------------------------------------------

