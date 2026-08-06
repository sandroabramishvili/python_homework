import os
import random
import string
import sys
import time

from hangman_art import hangman_title, already_guessed_art, wrong_guess_art, correct_guess_art, game_over_art, you_win_art, \
    state6, state5, state4, state3, state2, state1, state0

WORDS_FILE = "words.txt"
MAX_ATTEMPTS = 6
STATES_BY_ATTEMPTS = {6: state6, 5: state5, 4: state4, 3: state3, 2: state2, 1: state1, 0: state0}


def choose_word():
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as file:
            words = [line.strip().lower() for line in file]
    except FileNotFoundError:
        sys.exit(f"Error: could not find '{WORDS_FILE}'. Make sure it's in the same folder as this script.")

    words = [word for word in words if word.isalpha()]

    if not words:
        sys.exit(f"Error: '{WORDS_FILE}' doesn't contain any usable words.")

    return random.choice(words)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_hangman_state(attempts):
    state = STATES_BY_ATTEMPTS.get(attempts)
    if state is not None:
        print(state)

def print_memes(condition):
    clear_screen()
    if condition == "already_guessed":
        print(already_guessed_art)
    elif condition == "wrong_guess":
        print(wrong_guess_art)
    elif condition == "correct_guess":
        print(correct_guess_art)
    elif condition == "game_over":
        print(game_over_art)
    elif condition == "you_win":
        print(you_win_art)
    time.sleep(2)


def get_guess(guessed_letters):
    try:
        guess = input("\nPlease, guess a letter: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)

    if len(guess) != 1 or guess not in string.ascii_lowercase:
        return None, "Please, enter a single letter from a to z."

    if guess in guessed_letters:
        print_memes("already_guessed")
        return None, "You have already guessed this letter."

    return guess, None


def hangman():
    chosen_word = choose_word()
    shown_word = ["_"] * len(chosen_word)
    attempts = MAX_ATTEMPTS
    guessed_letters = []
    message = ""

    while attempts > 0 and "_" in shown_word:
        clear_screen()
        print("\n" + "-" * 60)
        print(hangman_title)
        print_hangman_state(attempts)
        print(" ".join(shown_word))
        if message:
            print(message)

        guess, message = get_guess(guessed_letters)
        if guess is None:
            continue

        guessed_letters.append(guess)

        if guess in chosen_word:
            for index, letter in enumerate(chosen_word):
                if letter == guess:
                    shown_word[index] = guess
            print_memes("correct_guess")
            message = f"Correct! The letter '{guess}' is in the word."
        else:
            print_memes("wrong_guess")
            attempts -= 1
            message = f"Incorrect! The letter '{guess}' is not in the word. Remaining attempts: {attempts}"

    clear_screen()
    if "_" not in shown_word:
        print_memes("you_win")
        clear_screen()
        print("\nCongratulations! You've guessed the word:", chosen_word)
    else:
        print_memes("game_over")
        clear_screen()
        print_hangman_state(attempts)
        print("\nGame over! The word was:", chosen_word)


if __name__ == "__main__":
    hangman()
