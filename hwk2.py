# 1. დაწერეთ პროგრამა, რომელიც მომხმარებელს შეეკითხება მართკუთხა სამკუთხედის კათეტების სიგრძეს (მთელი დადებითი რიცხვი) და გამოითვლის 
# ამ სამკუთხედის ჰიპოთენუზის სიგრძეს და ფართობს.

a = abs(int(input("Please provide the length of leg (a) of a right-angled triangle: ")))
b = abs(int(input("Please provide the length of leg (b) of a right-angled triangle: ")))

# 1. ჰიპოთენუზის გამოთვლა
c = round((a ** 2 + b ** 2) ** 0.5, 2)

# 2. ფართობის გამოთვლა
area = round(0.5 * a * b, 2)

# 3. საბოლოო შედეგი
print("The length of the hypotenuse is:", c)
print("The area of the triangle is:", area)


# 2. დაწერეთ პროგრამა, რომელიც მომხმარებელს შეეკითხება წამების რაოდენობას და გამოიტანეთ საათების, წუთების და წამების
# რაოდენობა (მაგ. 20000 წამი არის  5 საათი, 33 წუთი, 20 წამი)

total_seconds = int(input("Provide the number of seconds: "))

# Using floor division to always round down, using the modulo operator to use the remaining seconds to calculate further
hours, remaining_seconds = total_seconds // 3600, total_seconds % 3600
minutes, seconds = remaining_seconds // 60, remaining_seconds % 60

print(f"{total_seconds} seconds is {hours} hours, {minutes} minutes and {seconds} seconds")

