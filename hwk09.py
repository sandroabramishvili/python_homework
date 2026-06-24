# 1. დაწერეთ ფუნქცია, რომელიც პარამეტრად მიიღებს მომხმარებლის მიერ შეყვანილ ტექსტს და ამ ტექსტში დათვლის რამდენი სიმბოლო იყო მაღალ 
# რეგისტრში შეყვანილი და ასევე ამ ტექსტს გადააქცევს uppercase-ად ანუ მაღალ რეგისტრში დააბრუნებს, მაგალითად, მომხმარებელმა თუ შეიყვანა ტექსტი 
# Hello woRld, ფუნქციამ უნდა დააბრუნოს რომ 2 დიდი ასოა ამ ტექსტში და ეს ტექსტი აქციოს HELLO WORLD-ად.

def make_it_upper(text):
    
    num_of_upper = len([letter for letter in text if letter.isupper()])
    print(f"There are {num_of_upper} uppercase letters in this text.")
    return text.upper()

print(f"Turned into uppercase: {make_it_upper(input("Enter text: "))}")

# 2. დაწერეთ ფუნქცია, რომელიც პარამეტრად მიიღებს ე.წ. camel case ცვლადებს და დააბრუნებს snake case სახით, ანუ თუ გადავცემთ ცვლადს
#    firstName დააბრუნებს first_name, name დააბრუნებს ისევ name, preferredFirstName დააბრუნებს preferred_first_name, lastName დააბრუნებს
#    last_name და ასე შემდეგ.

def make_it_snake_case(text):
    result = ""

    for position, letter in enumerate(text):
        if letter.isupper() and position != 0:
            result += "_" + letter.lower()
        else:
            result += letter.lower()

    return result

print(f"Turned into snake_case: {make_it_snake_case(input("Enter text: "))}")

