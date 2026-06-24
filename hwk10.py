# 1. დაწერეთ ფუნქცია, რომელიც პარამეტრად მიიღებს რიცხვს, თუ რამდენჯერ უნდა ჰკითხოს მომხმარებელს რიცხვი და საბოლოოდ დააჯამებს
#    ყველა შეყვანილ რიცხვს, თუ არგუმენტად არ გადაეცა არანაირი რიცხვი, მაშინ ფუნქციამ 5-ჯერ ჰკითხოს მომხმარებელს რიცხვის 
#    შეყვანა და დააჯამოს ეს 5 რიცხვი. დააბრუნეთ საბოლოო ჯამი

def input_sum(num_of_inputs = 5):
    return sum(int(input("Enter number: ")) for _ in range(num_of_inputs))

print(f"The sum is: {input_sum(int(input('Enter how many times you want to be prompted to enter a number: ')))}")

# 2. დაწერეთ ფუნქცია რომელიც მიიღებს არგუმენტების განუსაზღვრელ რაოდენობას მთელი რიცხვების სახით და დააბრუნებს
#    ორ ლისტს, ერთ ლისტში იქნება გადაცმული არგუმენტებიდან კენტი რიცხვები ხოლო მეორე ლისტში ლუწი რიცხვები

def input_even_odd(*nums):
    return list(filter(lambda x: x % 2 == 0, nums)), list(filter(lambda x: x % 2 != 0, nums))

both = input_even_odd(*(int(n) for n in input("Enter numbers separated by spaces: ").split()))
print(f"Even list: {both[0]}")
print(f"Odd list: {both[1]}")

# 3. დაწერეთ ფუნქცია, რომელსაც პარამეტრად გადაეცემა მომხმარებლის მიერ შეყვანილი წინადადება და ამ წინადადებაში დაითვლის სიტყვებს
#    და დიქტის სახით დააბრუნებს თუ რომელი სიტყვა რამდენჯერ არის, მაგ: "This is a test. This test is fun." --> დააბრუნებს დიქტის
#    შემდეგი სახით: {'this': 2, 'is': 2, 'a': 1, 'test': 2, 'fun': 1} უნდა იყოს case insensitive (ანუ დიდ და პატარა ასოებს არ უნდა
#    ჰქონდეს მნიშვნელობა!)

import string
def word_counter(sentence):
    # პუნკტუაციის მოშორება
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    words = sentence.lower().split()
    return {word:words.count(word) for word in words}

print(word_counter(input("Enter sentence: ")))

# 4. მოცემულია პროდუქტების ლისტი:

products = [
    {"name": "Laptop", "price": 1200},
    {"name": "Mouse", "price": 15},
    {"name": "Keyboard", "price": 25},
    {"name": "Monitor", "price": 150},
    {"name": "Power", "price": 100},
    {"name": "Pad", "price": 10},
]

# filter() ფუნქციის გამოყენებით გაფილტრეთ და გამოიტანეთ პროდუქტები, რომლის ფასი ნაკლებია 100-ზე;

filtered_list = list(filter(lambda product : product["price"] < 100, products))
print(f"Filtered list: {filtered_list}")
print("-----------------------------------------------------------------------")

# map() ფუნქციის გამოყენებით გამოიტანეთ ყველა პროდუქტის სახელი და ფასი

map_list = list(map(lambda product : (product["name"], product["price"]), products))
print(f"Mapped list: {map_list}")
print("-----------------------------------------------------------------------")

# sorted() ფუნქციის გამოყენებით დაასორტირეთ პროდუქტების სია ფასის მიხედვით

sorted_list = list(sorted(products, key = lambda product: product["price"]))
print(f"Sorted list: {sorted_list}")
print("-----------------------------------------------------------------------")

# reduce() ფუნქციის გამოყენებით გამოიტანეთ ყველა პროდუქტის ფასების ჯამი

from functools import reduce

total_value = reduce(lambda total, product : total + product["price"], products, 0)
print(f"Total value: {total_value}")
print("-----------------------------------------------------------------------")


# 5. დაწერეთ რეკურსიული ფუნქცია, რომელსაც პარამეტრად გადაეცემა რიცხვი და დააბრუნებს 1-დან ამ რიცხვის ჩათვლით ყველა რიცხვის ჯამს

def recursive_function(num):
    if num <= 1:
        return num
    return num + recursive_function(num - 1)

print(f"The sum is: {recursive_function(int(input('Enter number: ')))}")