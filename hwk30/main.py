# Todo Dashboard

# შექმენით Front-end აპლიკაცია, რომელიც მიაკითხავს შემდეგ მისამართს
# https://jsonplaceholder.typicode.com/todos და წამოიღებს todos ჩანაწერებს.
# თითოეულ todo-ს გააჩნია userId, id, title და completed
# მთავარ გვერდზე გამოიტანეთ ყველა todo მხოლოდ title-ის ჩვენებით
# მთავარ გვერდზე გააკეთეთ პაგინაცია, ძებნა title-ის მიხედვით და
# ასევე ფილტრაცია შემდეგი ლოგიკით:
# userId-ით და completed მიხედვით
# გააკეთეთ თითოეული todo-ს დეტალური გვერდი, სადაც ყველა ველი იქნება გამოტანილი

# The front-end (index.html, detail.html, style.css, app.js, detail.js) talks
# directly to https://jsonplaceholder.typicode.com/todos from the browser, so
# no backend API is required. This script only serves the static files so the
# app can be opened over http:// instead of file://.

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)


def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"Serving Todo Dashboard at {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")


if __name__ == "__main__":
    main()
