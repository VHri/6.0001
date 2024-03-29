# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

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
    flag = False
    for i in secret_word:
        if i not in letters_guessed:
            flag = True
    if flag:
        return False
    else:
        return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess_word = []
    for i in secret_word:
        if i in letters_guessed:
            guess_word.append(i + ' ')
        else:
            guess_word.append('_ ')
    return ''.join(guess_word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    import string
    unused_letters = []
    for i in string.ascii_lowercase:
        if i not in letters_guessed:
            unused_letters.append(i)
    return ''.join(unused_letters)
    
    

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

    print('Welcome to the game : Hangman')
    print('I am thinking of a word that is', len(secret_word), 'letters long.\n')
    guesses = 6
    warnings = 3
    letters_guessed = []

    if not is_word_guessed(secret_word, letters_guessed):

        while guesses > 0 and not is_word_guessed(secret_word, letters_guessed):

            print('You have', guesses, 'guesses and', warnings, 'warnings left.')
            print('Available letters:', get_available_letters(letters_guessed))

            temp = str(input('Guess a letter: '))
            while not temp.isalpha():
                print('You input was not a letter, you lose a warning.')
                warnings -= 1
                if warnings == 0:
                    print('You have no warnings left, you lose a guess and gain 3 warnings.')
                    guesses -= 1
                    warnings = 3
                print('You have', guesses, 'guesses and', warnings, 'warnings left.')
                if guesses == 0:
                    break;
                temp = str(input('Try again: '))

            raw_input = temp.lower()
            while raw_input[0] in letters_guessed:
                print('You have previously guessed this letter')
                raw_input = str(input('try another letter: '))

            letters_guessed.append(raw_input[0])
            if raw_input[0] not in secret_word:
                if raw_input[0] in ['a', 'e', 'i', 'o', 'u']:
                    guesses -= 2
                else:
                    guesses -= 1
                print('The guessed letter wasn\'t in the word')
            else:
                print('Good guess!')
            print(get_guessed_word(secret_word, letters_guessed))

    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!')
        print('Your score is', guesses * len(secret_word))
    elif guesses <=0:
        print('You have no guesses left, you lost, the word was', secret_word)



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
    temp = []
    for i in my_word:
        if i != ' ':
            temp.append(i)
    flag = True
    if len(temp) == len(other_word):
        for i in range(len(temp)):
            if temp[i] != '_':
                if temp[i] != other_word[i]:
                    flag = False
    else:
        flag = False
    return flag


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    match_list = []
    for i in wordlist:
        if match_with_gaps(my_word, i):
            match_list.append(i)
    print (" ".join(match_list))



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
    print('Welcome to the game : Hangman')
    print('I am thinking of a word that is', len(secret_word), 'letters long.\n')
    guesses = 6
    warnings = 3
    letters_guessed = []

    if not is_word_guessed(secret_word, letters_guessed):

        while guesses > 0 and not is_word_guessed(secret_word, letters_guessed):

            print('You have', guesses, 'guesses and', warnings, 'warnings left.')
            print('Available letters:', get_available_letters(letters_guessed))

            temp = str(input('Guess a letter: '))
            while not temp.isalpha():
                if temp[0] == '*':
                    show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                    temp = str(input('Guess a letter: '))
                else:
                    print('You input was not a letter, you lose a warning.')
                    warnings -= 1
                    if warnings == 0:
                        print('You have no warnings left, you lose a guess and gain 3 warnings.')
                        guesses -= 1
                        warnings = 3
                    print('You have', guesses, 'guesses and', warnings, 'warnings left.')
                    if guesses == 0:
                        break;
                    temp = str(input('Try again: '))

            raw_input = temp.lower()
            while raw_input[0] in letters_guessed:
                print('You have previously guessed this letter')
                raw_input = str(input('try another letter: '))

            letters_guessed.append(raw_input[0])
            if raw_input[0] not in secret_word:
                if raw_input[0] in ['a', 'e', 'i', 'o', 'u']:
                    guesses -= 2
                else:
                    guesses -= 1
                print('The guessed letter wasn\'t in the word')
            else:
                print('Good guess!')
            print(get_guessed_word(secret_word, letters_guessed))

    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!')
        print('Your score is', guesses * len(secret_word))
    elif guesses <= 0:
        print('You have no guesses left, you lost, the word was', secret_word)



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
