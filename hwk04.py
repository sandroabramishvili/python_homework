# 1. დაწერეთ პროგრამა რომელიც მომხმარებელს ჰკითხავს წონას(კგ) და სიმაღლეს(მ), შეყვანილი მონაცემების 
# საფუძველზე გამოითვლის BMI-ს(Body Mass Index). ფორმულა: წონა გაყოფილი სიმაღლის კვადრატზე
# თუ BMI ნაკლებია 19-ზე, გამოიტანეთ ინფო რომ ის არის underweight
# თუ BMI არის 19 და 25 შორის, გამოიტანეთ ინფო რომ ის არის normalweight
# თუ BMI მეტია 25-ზე, გამოიტანეთ ინფო რომ ის არის overweight

weight = float(input("Enter your weight: "))
height = float(input("Enter your height: "))
bmi = round(weight / (height ** 2), 2)

if bmi < 19:
    print("You are underweight")
elif 19 <= bmi < 25:
    print("You are normal weight")
else:
    print("You are overweight")

# 2. დაწერეთ კალკულატორის პროგრამა, რომელიც მომხმარებელს შეეკითხება ორ რიცხვს და არითმეტიკულ ოპერატორს,
# შესაბამისი ოპერატორის საფუძველზე გამოითვლის ამ ორი რიცხვის შედეგს.

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
operator = input("Enter your operator of choice: ")

if operator == "+":
    print(f"{num1} + {num2} = {num1 + num2}")
elif operator == "-":
    print(f"{num1} - {num2} = {num1 - num2}")
elif operator == "*":
    print(f"{num1} * {num2} = {num1 * num2}")
elif operator == "/":
    if num2 != 0:
        print(f"{num1} / {num2} = {num1 / num2}")
    else:
        print("You cannot divide by zero.")
elif operator == "%":
    print(f"{num1} % {num2} = {num1 % num2}")
elif operator == "**":
    print(f"{num1} ** {num2} = {num1 ** num2}")
else:
    print(f"Invalid option")

# 3. დაწერეთ პროგრამა, რომელიც მომხმარებელს შეეკითხება 3 რიცხვს, ჯერ შეამოწმეთ ეს რიცხვები არ უდრიდეს ერთმანეთს,
# თუ რომელიმე ორი ერთმანეთს უდრის, დაპრინტეთ რომ შეიყვანოს განსხვავებული რიცხვები. თუ რიცხვები განსხვავებულია, 
# იპოვეთ ყველაზე დიდი რიცხვი. არ გამოიყენოთ max ფუნქცია!

first = int(input("Enter first number: "))
second = int(input("Enter second number: "))
third = int(input("Enter third number: "))

if first != second and first != third and second != third:
    largest = first

    if second > largest:
        largest = second
    if third > largest:
        largest = third

    print(f"{largest} is the largest number")
else:
    print("The numbers must be different than each other, try again")
