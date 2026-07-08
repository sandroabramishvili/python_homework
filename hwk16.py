# 1.
# შექმენით ბანკის სისტემა, რომელიც შეიცავს მომხმარებლებს და მათ ანგარიშებს. სისტემაში უნდა გამოიყენოთ:
#    კლასის ატრიბუტები:
#    	bank_name - ბანკის დასახელება
#    	total_accounts(private) - ანგარიშების რაოდენობა(ყოველი ანგარიშის გახსნის შემდეგ ავტომატურად უნდა გაიზარდოს)
   	
#    ინსტანსის ატრიბუტები:
# 	owner (protected) — ანგარიშის მფლობელის სახელი
# 	balance (private) — ანგარიშზე არსებული თანხა
# 	account_number (private) — უნიკალური ანგარიში(ეს არ უნდა გადაეცეს ობიექტის შექმნის დროს, უნდა დაგენერირდეს
# 	ავტომატურად შემდეგი პრინციპით: პირველი ექაუნთის ნომერი იქნება AN0001, მეორესი AN0002 და ა.შ.
	
#    მეთოდები:
#    	__init__(self, owner, balance) — მნიშვნელობების მინიჭება

# 	deposit(self, amount) - ბალანსზე თანხის დამატება

# 	withdraw(self, amount) - ბალანსიდან თანხის გამოტანა

# 	check_balance(self) — აბრუნებს ბალანსს

# 	get_account_number(self) — აბრუნებს ანგარიშის ნომერს

# 	change_owner(self, new_owner) — ცვლის owner მნიშვნელობას
	
#    კლასის მეთოდი:
#    	get_total_accounts(): — აბრუნებს ანგარიშების რაოდენობას

#    სტატიკური მეთოდი:
#    	validate_amount(amount): — აბრუნებს True, თუ თანხა დადებითია
#    	ეს მეთოდი უნდა გამოიყენოთ __init__-ში ბალანსის შემოწმებისას და ისე გაუკეთოთ ბალანსს ინიციალიზაცია. ასევე,
#    	deposit და withdraw დროსაც ეს გამოიყენეთ რომ ვალიდაცია გაუკეთოთ amount-ს და ისე დაუმატოთ ან გამოიტანოთ თანხა
   	
# ობიექტი დაბეჭდვისას გამოჩნდეს შემდეგი სახით, მაგალითად: "Account: AN0002 | Owner: Nino Beridze"

class BankSystem:
    bank_name = "Sandro's Bank"
    __total_accounts = 0

    def __init__(self, owner, balance):
        self._owner = owner
        self.__balance = balance if self.validate_amount(balance) else 0
        BankSystem.__total_accounts += 1
        self.__account_number = f"AN{BankSystem.__total_accounts:04d}"

    def deposit(self, amount):
        if self.validate_amount(amount):
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if self.validate_amount(amount) and amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance: {self.__balance}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def change_owner(self, new_owner):
        self._owner = new_owner
        print(f"Owner changed to {new_owner}")

    def __str__(self):
        return f"Account: {self.__account_number} | Owner: {self._owner}"

    @classmethod
    def get_total_accounts(cls):
        return cls.__total_accounts

    @staticmethod
    def validate_amount(amount):
        return amount > 0


account1 = BankSystem("Sandro Abramishvili", 1000)
account2 = BankSystem("Nino Beridze", 1000)
print(account1)  # Account: AN0001 | Owner: Sandro Abramishvili
print(account2)  # Account: AN0002 | Owner: Nino Beridze