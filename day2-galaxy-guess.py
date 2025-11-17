#Day 2: Guess the number - Galaxy Edition
#a@dary33 | #PythonPower

import random

print("Welcome to the Milky Way Guessing Number")
print("I picked a secret star between 1 and 100...")
print("You have max 7 attempts. Can you guess it?\n")

secret = random.randint(1, 100)
attempts = 0
max_attempts = 7

while attempts < max_attempts:
    try:
        guess = int(input(f"Attempt {attempts + 1}/{max_attempts} → Your guess: "))
    except ValueError:
        print("Please enter a valid integer.")
        continue

    attempts += 1

    if guess == secret:
        print(f"You found the star in {attempts} ATTEMPT(S)!")
        print("The universe is yours, @a_dary33")
        break
    elif guess < secret:
        print("Too low - aim higher in the galaxy!")
    else:
        print("Too high - recalibrating...")

    if attempts == max_attempts:
        print(f"\nGame Over. The secret star was {secret}.")
        print("Try again later, future kleeon.")
