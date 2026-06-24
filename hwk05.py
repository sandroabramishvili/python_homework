# დაწერეთ პროგრამა, რომელიც:

# მომხმარებელს შეაყვანინებს ორ რიცხვს.
# ორივე მნიშვნელობას გადააქცევს float ტიპად.
# გამოთვლის პირველის მეორეზე გაყოფას.

# გამოიყენეთ try/except/else/finally.

# დაიჭირეთ:
# ValueError
# ZeroDivisionError
# ამოუცნობი ერორი
# თუ ყველაფერი წარმატებით შესრულდა, გამოტანეთ შედეგი
# ყოველთვის დაიბეჭდოს: "პროგრამა დასრულდა"

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = num1 / num2
except ValueError:
    print("Please enter a valid number")
except ZeroDivisionError:
    print("You can't divide by zero")
except Exception as e:
    print(f"An unknown error ocurred: {e}")
else:
    print(f"{num1} / {num2} = {result}")
finally:
    print("End of program")
