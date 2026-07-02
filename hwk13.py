# მოცემულია მისამართი https://jsonplaceholder.typicode.com/users
# requests ბიბლიოთეკის გამოყენებით მიაკითხეთ ამ მისამართს, გააკეთეთ შემდეგი დავალება:
# შექმენით ფუნქცია, რომელსაც გადაეცემა პარამეტრად user_id 

# ფუნქციამ ამ მისამართიდან უნდა მოძებნოს მომხმარებელი ID-ის მიხედვით
#     და დააბრუნოს შემდეგი ფორმატის დიქტი:

#     {
#         "name": ...,
#         "email": ...,
#         "city": ...,
#         "company": ...
#     }

#     თუ მომხმარებელი არ არსებობს,
#     დააბრუნოს None.

import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

data = response.json()

def info_dump(user_id):
    for entry in data:
        if entry["id"] == user_id:
            info = {
                "name": entry["name"],
                "email": entry["email"],
                "city": entry["address"]["city"],
                "company": entry["company"]["name"]
            }
            return info
    else:
        return None
    
print(info_dump(4))