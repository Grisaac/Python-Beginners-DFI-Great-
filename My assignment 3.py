import random

def display_title():
    print("Virtual Football Match Result Guessing Game")
    print("Guess the outcome (W/L/D) for 10 matches:")

def play_game():
    matches = 10
    wins = 0
    losses = 0

    for match in range(1, matches + 1):
        # Generate a random result for the match (W/L/D)
        result = random.choice(["W", "L", "D"])

        # Get user's guess
        user_guess = input(f"Match {match}: Guess (W/L/D): ").upper()

        # Validate user input
        while user_guess not in ["W", "L", "D"]:
            user_guess = input("Invalid input. Guess (W/L/D): ").upper()

        # Compare user's guess with actual result
        if user_guess == result:
            print(f"Correct! The result was {result}.")
            wins += 1
        else:
            print(f"Oops! The result was {result}.")
            losses += 1

    # Print overall results
    print("\nOverall Results:")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")

    # Determine if the user won or lost overall
    if wins >= 5:
        print("Congratulations! You won the majority of the matches.")
    else:
        print("Better luck next time! You didn't win the majority of the matches.")

def main():
    display_title()
    play_game()

if __name__ == "__main__":
    main()
