import random

name = input("What is your name?")
print(f"Hello, {name}! Welcome to the Guess the Number Game.")

print("i am thiking of a number between 1 and 100.")
print("You have 10 attempts to guess the number.")
number = random.randint(1, 100)

guesses_left = 10

while guesses_left > 0:
    try:
        guess = int(input("Guess the number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    guesses_left -= 1

    if guess < number:
        print("Too low.")
        print(f"You have {guesses_left} guesses left.")
    elif guess > number:
        print("Too high.")
        print(f"You have {guesses_left} guesses left.")
    else:
        print(
            f"Congratulations, {name}! You guessed the number in {10 - guesses_left} tries!"
        )
        break

if guesses_left == 0:
    print(f"You ran out of guesses. The number was {number}.")