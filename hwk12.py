# 1. დაწერეთ ტრანზაქციის ფუნქცია, რომელსაც გადაეცემა ატრიბუტად ბალანსი და გადასახდელი თანხა, დაუწერეთ დეკორატორი, 
# რომელიც საკომისიოს ჩამოაჭრის 1 ლარს და თუ საკმარისი თანხა არ იქნება ანგარიშზე დაუბრუნეთ შეცდომის ტექსტი

def commission(tran):
    def wrapper_transaction(balance, to_pay):
        commission = 1
        total_to_pay = commission + to_pay

        if total_to_pay > balance:
            return "Error: Insufficient funds on the account."
        return tran(balance, total_to_pay)
    return wrapper_transaction

@commission
def transaction(balance, to_pay):
    return balance - to_pay

# 2. შექმენით დეკორატორი count_calls, რომელიც დაითვლის რამდენჯერ გამოიძახეს ფუნქცია\

def count_calls(func):
    count = 0
    def counter():
        nonlocal count
        count += 1
        return f"The function has been called {count} times"
    return counter
        
@count_calls
def func_to_call():
    pass

for _ in range(10):
    print(func_to_call())