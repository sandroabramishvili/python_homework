# დაწერეთ პროგრამა, რომელიც მომხმარებელს სთხოვს ასაკის შეყვანას.

# ასაკი უნდა გარდაქმნათ int ტიპად

# თუ მომხმარებელი შეიყვანს არარიცხვით მნიშვნელობას, გამოიტანეთ:
# "შეიყვანეთ მხოლოდ რიცხვი!"

# აღაზევეთ ერორი, იმ შემთხვევაში თუ უარყოფითი იქნება რიცხვი და დაიჭირეთ ეს ერორი

# თუ მომხმარებელი შეიყვანს რიცხვით მნიშვნელობას, ასაკი თუ იქნება 18-ზე ნაკლები,
# გამოიტანეთ რომ არის არასრულწლოვანი, ხოლო 18 ან მეტის შემთხევაში, გამოიტანეთ "სრულწლოვანი"

# გამოიყენეთ else ბლოკი

try:
    age = int(input("Enter your age: "))
    if age < 0:
        raise RuntimeError
except ValueError:
    print("Enter a number please")
except RuntimeError:
    print("Age cannot be negative")
else:
    if age < 18:
        print("You are underage")
    else:
        print("You are of legal age")



