from hangman_art import stages
from hangman_art import logo
from hangman_words import word_list
import random

chosen_word = random.choice(word_list)
word_length = len(chosen_word)
end_of_game = False
lives = 6

print(logo)

print(f'Pssst, the solution is {chosen_word}.')

#Create blanks
display = []
for _ in range(word_length):
    display += "_"

while not end_of_game:
    guess = input("Guess a letter: ").lower()

    # If the user has entered a letter they've already guessed
    
    if "_" not in display:
        end_of_game = True
        print("You win.")
    elif guess in display:
        print(f'you allready guessed "{guess}" once, please try other characters !!')
    elif guess not in chosen_word:
        print(f'"{guess}" is not in the word!!')
        lives -= 1
        if lives == 0:
            end_of_game = True
            print("You lose.")
    else:
      for position in range(word_length):
          letter = chosen_word[position]
          if letter == guess:
              display[position] = letter

    #Join all the elements in the list and turn it into a String.
    print(f"{' '.join(display)}")

    print(stages[lives])
