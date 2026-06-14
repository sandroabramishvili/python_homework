# დაწერეთ თამაში guessing game 

# თამაშის ლოგიკა მდგომარეობს შემდეგში:
# პროგრამა შემთხვევითობის პრინციპით ირჩევს რიცხვს 1-დან 100-მდე.
# მომხმარებელს აქვს 5 სიცოცხლე.

# შემდგომ მომხმარებელს ვეკითხებით რიცხვს და თუ დაემთხვევა შემთხვევითობის პრინციპით არჩეულ რიცხვს, დავუწეროთ 
# რომ მოიგო და დამთავრდეს თამაში,თუ არ დაემთხვევა, დავუწეროთ შემთხვევითი რიცხვი მეტია ან ნაკლებია 
# მომხმარებლის მიერ შემოყვანილ რიცხვზე და სიცოცხლეც გამოაკლდეს თითოეულ ცდაზე
# სიცოცხლეების ამოწურვის შემდეგ დავუწეროთ რომ წააგო და თამაში დამთავრდეს.

from random import randint

lives_left = 5
mystery_number = randint(1,100)

while lives_left:
    try:
        guess = int(input("Guess the mystery number (1-100): "))
    except ValueError:
        print("I said guess a number!")
        continue
    if guess > 100 or guess < 1:
        print("You're out of range pal, I said 1 to 100. try again, I won't take any lives")
        continue
    elif guess == mystery_number:
        print(f"You won! the number is {guess}")
        break
    elif guess < mystery_number:
        lives_left -= 1
        print(f"Your guess is less than the mystery number, you have {lives_left} lives left. try again")
    elif guess > mystery_number:
        lives_left -= 1
        print(f"Your guess is greater than the mystery number, you have {lives_left} lives left. try again")
else:
    print("You're out of lives, you lost the guessing game :/ You'll never find out the mystery number.")

