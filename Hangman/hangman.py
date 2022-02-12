# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    word_guessed = True
    for letter in secret_word:
        if letter not in letters_guessed:
            word_guessed = False
            break
    return  word_guessed



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    final_word=""
    for word in secret_word:
        if word in letters_guessed:
            final_word = final_word + word + " "
        else:
            final_word = final_word + "_ "

    return final_word





def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    alphabet=string.ascii_lowercase
    available_letters=alphabet
    for letter in letters_guessed:
        available_letters=available_letters.replace(letter,"")

    return available_letters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guessed_letter=[]
    play_on = True
    warning=3
    guess=6
    blank=""

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} long.")
    for _ in range(len(secret_word)):
        blank=blank + "_ "
    print(blank)

    while play_on == True:

        print(f"You have {guess} guesses left.")
        print(f"You have {warning} warnings left.")
        print(f"Available letters: {get_available_letters(guessed_letter)} ")

        while True:
            current_guess= input("Please guess a letter.")
            current_guess=current_guess.lower()
            if current_guess in guessed_letter:
               warning-=1
               print(f"Oops! You've already guessed that letter. You now have {warning} warnings:")
               if warning==0:
                   break

            elif current_guess not in string.ascii_lowercase:
               warning-=1
               print(f"Oops! Please enter an alphabet. You now have {warning} warnings:")
               if warning==0:
                   break

            else:
                break

        if warning==0:
            print(f"Oops! Your warnings are finished. Be careful next time. Your word is {secret_word}")
            break

        guessed_letter.append(current_guess)




        if current_guess not in secret_word and current_guess not in ['a','e','i','o','u'] :
            guess-=1
            print("Wrong guess")
        elif current_guess not in secret_word:
            guess-=2
            print("Wrong guess")
        else:
            print("Good guess")

        if guess <= 0 :
            print(f"You lost. The correct word was {secret_word}. Better luck next time.")
            play_on = False

        print(get_guessed_word(secret_word, guessed_letter))

        if is_word_guessed(secret_word,guessed_letter) == True :
            print(f"You won!. \nThe word is {secret_word}")
            print(f"You score is {guess*len(secret_word)}")
            play_on = False

        print("-----------------------------------")



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    counter=0
    match = True
    if 2 * len(other_word) == len(my_word):
        for word in other_word:
            if (my_word[counter] != word) and (my_word[counter] != "_")  :
                match = False
                break
            counter += 2
    else:
        match = False

    if match == True:
        counter=0
        for word in other_word:
            if my_word[counter] == "_":
                if word in my_word:
                    match = False
                    break
            counter += 2

    return match


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    possible_words=""
    for words in wordlist:
        if match_with_gaps(my_word,words) == True:
            possible_words = possible_words + " " + words

    print(possible_words)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guessed_letter = []
    play_on = True
    warning = 3
    guess = 6
    blank = ""

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} long.")
    for _ in range(len(secret_word)):
        blank = blank + "_ "
    print(blank)

    while play_on == True:

        print(f"You have {guess} guesses left.")
        print(f"You have {warning} warnings left.")
        print(f"Available letters: {get_available_letters(guessed_letter)} ")

        while True:
            current_guess = input("Guess your letter")
            current_guess = current_guess.lower()
            if current_guess in guessed_letter:
                warning -= 1
                print(f"Oops! You've already guessed that letter. You now have {warning} warnings:")
                if warning == 0:
                    break

            elif current_guess not in string.ascii_lowercase and current_guess != "*":
                warning -= 1
                print(f"Oops! Please enter an alphabet. You now have {warning} warnings:")
                if warning == 0:
                    break

            elif current_guess ==  "*":
                show_possible_matches(get_guessed_word(secret_word, guessed_letter))
                break

            else:
                break

        if warning == 0:
            print(f"Oops! Your warnings are finished. Be careful next time. Your word is {secret_word}")
            break

        if current_guess != "*":

            guessed_letter.append(current_guess)

            if current_guess not in secret_word and current_guess not in ['a', 'e', 'i', 'o', 'u']:
                guess -= 1
                print("Wrong guess")
            elif current_guess not in secret_word:
                guess -= 2
                print("Wrong guess")
            else:
                print("Good guess")

            if guess <= 0:
                print(f"You lost. The correct word was {secret_word}. Better luck next time.")
                play_on = False

            print(get_guessed_word(secret_word, guessed_letter))

            if is_word_guessed(secret_word, guessed_letter) == True:
                print(f"You won!. \nThe word is {secret_word}")
                print(f"You score is {guess * len(secret_word)}")
                play_on = False

            print("-----------------------------------")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
