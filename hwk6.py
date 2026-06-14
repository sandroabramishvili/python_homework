# 1. დაწერეთ პროგრამა, რომელიც მომხმარებელს შეეკითხება რიცხვს და გამოითვლის ამ რიცხვის ფაქტორიალს, შეგახსენებთ რომ ფაქტორიალი 
# არის ამ რიცხვის ნამრავლი ყველა მთელ რიცხვზე 1-მდე, ანუ 5-ის ფაქტორიალი არის 5 X 4 X 3 X 2 X 1 (დაწერეთ for ლუპის გამოყენებით)

print("I can calculate the factorial for any number.")
while True:
    try:
        number = int(input("Enter the number: "))
        if number < 0:
            raise Exception
    except ValueError:
        print("That's not a valid number. try again")
        continue
    except Exception:
        print("Factorials are defined for non-negative integers")
        continue

    factorial = 1
    for n in range(number, 1, -1):
        factorial *= n

    print(f"The factorial of {number} is {factorial}")
    break


# 2. დაწერეთ გამრავლების ტაბულა ციკლების გამოყენებით, მაგალითად ასეთი სახით:
# 1 * 1 = 1
# 1 * 2 = 2
# 1 * 3 = 3
# .........
# 9 * 7 = 63
# 9 * 8 = 72
# 9 * 9 = 81

for num1 in range(1,10):
    for num2 in range(1,10):
        print(f"{num1} * {num2} = {num1 * num2}")

# 3. ჩავთვალოთ რომ გვაქვს აპარატი, რომელშიც უნდა გადავიხადოთ რაღაც სერვისის გადასახადი, რომლის ღირებულებაც არის 50 ლარი,
# ხოლო აპარატი იღებს მხოლოდ 5, 10 და 20 ლარიან კუპიურებს და გვიბრუნებს ასევე ხურდას.

# დაწერეთ პროგრამა, რომელიც ბეჭდავს გადასახადი თანხის ოდენობას, შემდეგ მომხმარებელს სთხოვს მოათავსოს კუპიურა, თუ კუპიურა არ არის ვალიდური,
# დაბეჭდოს რომ შეიტანოს ვალიდური კუპიურა. თუ კუპიურა ვალიდურია, დაბეჭდოს რაც დარჩა გადასახდელი თანხა და კვლავ სთხოვოს მომხმარებელს კუპიურის 
# მოთავსება, მანამ სანამ, გადასახდელი თანხა არ განულდება. ბოლოს კი დაუწეროს რამდენი ეკუთვნის ხურდა. ანუ ბოლო იტერაციაზე თუ დარჩენილია 
# მაგალითად გადასახდელი თანხა 10 ლარი და მომხმარებელი შეიტანს 20 ლარიანს, დაუწეროს რომ ეკუთვნის 10 ლარი ხურდა.

service_fee = 50

while True:
    try:
        bill = int(input(f"PAY ${service_fee} (WE ACCEPT $5, $10, $20 BILLS ONLY): "))
        print("---------------------------------------------------------")
    except ValueError:
        print("THAT'S NOT MONEY!")
        print("---------------------------------------------------------")
        continue
    if bill < 0:
        print("YOU'RE SUPPOSED TO GIVE ME MONEY, NOT THE OTHER WAY AROUND.")
        print("---------------------------------------------------------")
    elif bill not in [5, 10, 20]:
        print(f"WE DON'T ACCEPT ${bill} BILLS. TRY AGAIN")
        print("---------------------------------------------------------")
    else:
        service_fee -= bill
        if service_fee > 0:
            print(f"YOU STILL HAVE TO PAY ${service_fee} MORE")
            print("---------------------------------------------------------")
        elif service_fee == 0:
            print(f"THANK YOU FOR PAYING!")
            print("---------------------------------------------------------")
            break
        elif service_fee < 0:
            change = abs(service_fee)
            print(f"THANK YOU FOR PAYING!")
            print(f"HERE'S YOUR CHANGE: ${change}")
            print("---------------------------------------------------------")
            break

