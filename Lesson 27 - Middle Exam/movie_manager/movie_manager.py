import json
import os
import time
from movie_art import banner

filename = "movies.json"


class Movie:

    def __init__(self, title, director, release_year):
        self.title = title
        self.director = director
        self.release_year = release_year

    def __str__(self):
        return f"Title: {self.title}, Director: {self.director}, Release Year: {self.release_year}"

    def to_dict(self):
        return {
            "title": self.title,
            "director": self.director,
            "release_year": self.release_year,
        }

    @staticmethod
    def from_dict(data):
        return Movie(data["title"], data["director"], data["release_year"])


class MovieManager:

    def __init__(self, filename):
        self.filename = filename
        self.movies = []
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            self.movies = []
            return
        with open(self.filename, "r") as file:
            data = json.load(file)
            self.movies = [Movie.from_dict(entry) for entry in data]
       
    def save(self):
        try:
            with open(self.filename, "w") as file:
                json.dump([movie.to_dict() for movie in self.movies], file, indent=2)
        except OSError as e:
            print(f"Could not save movies to file: {e}")

    def add_movie(self, title, director, release_year):
        movie = Movie(title, director, release_year)
        self.movies.append(movie)
        self.save()
        return movie

    def view_movies(self):
        if not self.movies:
            print("No movies found.")
            return
        for movie in self.movies:
            print(movie)

    def search_by_title(self, search_title):
        search_title = search_title.strip().lower()
        found = [m for m in self.movies if m.title.lower() == search_title]
        if not found:
            print("Movie not found.")
            return []
        for movie in found:
            print(movie)
        return found


def get_valid_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_year(prompt, min_year=1888, max_year=2027):
    while True:
        stripped_year = input(prompt).strip()
        if not stripped_year.isdigit():
            print("Please enter a valid numeric year: ")
            continue
        year = int(stripped_year)
        if year < min_year or year > max_year:
            print(f"Please enter a year between {min_year} and {max_year}.")
            continue
        return year


def display_separator():
    print("*" * 100)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display():
    print(banner)
    manager = MovieManager(filename)

    while True:
        display_separator()
        print("MY MOVIE DATABASE")
        print("'" * 100)
        print("A: Add a new movie")
        print("V: View all movies")
        print("S: Search for a movie by title")
        print("Q: Quit")
        display_separator()

        choice = input("Enter your choice: ").strip()
        clear_screen()
        display_separator()

        if choice == "A":
            title = get_valid_string("Enter the name of the movie: ")
            director = get_valid_string("Enter the director of the movie: ")
            release_year = get_valid_year("Enter the year it was released: ")
            manager.add_movie(title, director, release_year)
            print(f'"{title}" was added.')
        elif choice == "V":
            manager.view_movies()
        elif choice == "S":
            search_title = get_valid_string("Enter the title of the movie to search: ")
            manager.search_by_title(search_title)
        elif choice == "Q":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    display()