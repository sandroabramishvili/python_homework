# დაწერეთ ფუნქცია, რომელსაც პარამეტრად გადაეცემა რიცხვი და შეამოწმებს ეს რიცხვი არის თუ არა მარტივი
# შემდეგ ნაკადების გამოყენებით გაუშვით ეს ფუნქცია პარალელურად რომ შეამოწმოს შემდეგ ლისტში
# num_list = [17, 25, 74, 199, 101, 41, 39, 50, 20, 19, 51] ყველა რიცხვი და დააბრუნოს პასუხი

import multiprocessing

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main():
    num_list = [17, 25, 74, 199, 101, 41, 39, 50, 20, 19, 51]

    with multiprocessing.Pool() as pool:
        results = pool.map(is_prime, num_list)

    for num, result in zip(num_list, results):
        print(f"{num} is {'prime' if result else 'not prime'}.")

if __name__ == "__main__":
    main()