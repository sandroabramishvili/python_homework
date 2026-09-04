# შექმენით FastAPI აპლიკაცია, სერვერის გასაშვებად გამოიყენეთ uvicorn სერვერი

from fastapi import FastAPI

app = FastAPI()

# შექმენით ენდპოინტები GET, POST, PUT, PATCH და DELETE მოთხოვნების დასამუშავებლად
# თითოეულ ენდპოინტზე დააბრუნეთ შესაბამისი პასუხი, მაგ: პროდუქტი შეიქმნა წარმატებით და ა.შ.
# არ არის საჭირო request body, მხოლოდ პასუხები დააბრუნეთ საჩვენებლად.
# პროექტი ატვირთეთ გითჰაბის რეპოზიტორიაში, პროექტს გაატანეთ ასევე requirements ფაილი.

@app.get("/get-endpoint")
def get_endpoint():
    return {"message": "Product retrieved successfully!"}

@app.post("/post-endpoint")
def post_endpoint():
    return {"message": "Product created successfully!"}

@app.put("/put-endpoint")
def put_endpoint():
    return {"message": "Product updated successfully!"}

@app.patch("/patch-endpoint")
def patch_endpoint():
    return {"message": "Product patched successfully!"}

@app.delete("/delete-endpoint")
def delete_endpoint():
    return {"message": "Product deleted successfully!"}
