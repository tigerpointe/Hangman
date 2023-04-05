#!/usr/bin/env python3
"""A module for starting a classic game of Hangman in Python.

TO start the module from the REPL, import using:
    >>> from hangman import start_hangman
    >>> help(start_hangman)
    >>> start_hangman()

.SYNOPSIS
Starts a classic game of Hangman in Python.

.DESCRIPTION
Players discover puzzle words or phrases by suggesting letters.
Each incorrect guess adds an element to the hangman diagram.
The game ends when a solution is guessed, or a diagram is completed.

Various word and phrase dictionaries can be found online.

A dictionary can be a simple list of words or phrases, one per line.
For example:  hangman
              tic-tac-toe
              powershell programming

An optional category can be specified by adding a comma separator.
For example:  classic games, hangman
              classic games, tic-tac-toe
              computers, powershell programming

Please consider giving to cancer research.

.PARAMETER path
Specifies the path to a dictionary file of puzzle words and phrases.

.INPUTS
None.

.OUTPUTS
A whole lot of fun.

.EXAMPLE
start_hangman()
Starts the program with the default options.

.EXAMPLE
start_hangman(path="./dictionary.txt")
Starts the program with a custom dictionary of puzzle words and phrases.

.NOTES
MIT License

Copyright (c) 2023 TigerPointe Software, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

If you enjoy this software, please do something kind for free.

History:
01.00 2023-Apr-01 Scott S. Initial release.
01.01 2023-Apr-04 Scott S. Fix whitespace.

.LINK
https://en.wikipedia.org/wiki/Hangman_(game)

.LINK
https://en.wikipedia.org/wiki/ASCII_art

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/
"""

from os import system, name # operating system specific

import random # random numbers
import time   # time functions

# Define the list of special non-alphabetic characters
# (escapes backslashes and double-quotes)
special = " !\"#$%&'()*+,-./0123456789:;<=>?@[\\]^_`{|}~"

# Define the ASCII art (originally created by Scott S.)
# (escapes backslashes and double-quotes)
ascii = """
  [ ]============[]
  | |/     |
  | |      |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|_ _|}
  | |   O| o |O
  | |    ( - )
  | |     ===
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( O )
  | |   _ === _
  | |  [  \./  ]
  | |    | . |
  | |    |=O=|
  | |    '   '
  | |
  | |
  | |
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. _|}
  | |   O| o |O
  | |    ( - )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . |
  | |  |_|=O=|
  | |  (_'   '
  | |
  | |
  | |
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|_ .|}
  | |   O| o |O
  | |    ( - )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_'   '_)
  | |
  | |
  | |
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( - )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | |
  | |   .|_|
  | |  (___'
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( O )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | | |
  | |   .|_|_|.
  | |  (___'___)
  | |  .=======.
 /   \\ |       |
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/     |
  | |      |
  | |      |
  | |    /////
  | |   {|x x|}
  | |   O| o |O
  | |    (---)
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | | |
  | |   .|_|_|.
  | |  (___'___)
 /   \\
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
  [ ]============[]
  | |/
  | |
  | |   Yippee!
  | |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( ~ )
  | |   _.| |._
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | | |
  | |   .|_|_|.
 /   \\ (___'___)
'\"'\"'\"'\"'\"'\"'\"'\"'\"'
"""


def clear():
    """ Clears the screen, works across all platforms.
    """
    if (name == 'nt'):
        _ = system('cls')   # Microsoft Windows
    else:
        _ = system('clear') # All others


def get_new_mask(word, mask, guess):
    """ Gets a new mask value that includes the current guess.
    Parameters
    word  : the original puzzle word value
    mask  : the mask with placeholders
    guess : the letter guess
    """
    # Replace matching characters in the mask with the guess value
    # (starts with the puzzle word and copies back the mask characters)
    chars = list(word)
    for i in range(len(chars)):
        if chars[i] != guess:
            chars[i] = mask[i]
    return "".join(chars)


def start_hangman(path="./hangman.txt"):
    """ Starts a classic game of Hangman in Python.
    Parameters
    path : Defines the default path to a dictionary file of puzzle words and
           phrases (the default data file must be placed in the same folder as
           this script)
    """
    # Use a try-catch for exceptions because the host is cleared on each guess
    # (otherwise, the exception messages get cleared with the console)
    try:

        # Read the entire dictionary file
        # (be sure to ignore encoding errors for third-party data files)
        print("Loading ...")
        time.sleep(0.5)
        datafile = open(path, "r", errors="ignore")
        words = datafile.readlines()
        datafile.close()

        # Define the ASCII art panel variables
        height = 18                 # number of text lines per panel
        width  = 22                 # includes the horizontal padding
        lines  = ascii.splitlines() # splits on the line feeds
        del lines[0]                # delete the initial blank line

        # Loop while more games are selected
        more = "Y"
        while (more == "Y"):

            # Initialize the loop control variables
            solved  = False # not solved
            count   = 0 # no guesses
            maximum = 8 # wrong guesses, number of ASCII art panels minus one

            # Initialize the puzzle variables (includes an optional category)
            remain   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; # holds remaining letters
            category = "";
            word     = random.choice(words).strip().upper()
            idx      = word.rfind(",") # finds optional category separator
            if (idx >= 0):
                category = "The category is " + word[0:idx].strip()
                idx += 1
                word = word[idx:len(word)].strip()

            # Create a mask and replace the special characters
            mask = ("." * len(word)) # repeats a placeholder for each character
            for chr in special:
                mask = get_new_mask(word, mask, chr)

            # Loop while not solved and remaining guesses are available
            while (not solved) and (count < maximum):

                # Check for a solved puzzle and skip to the winning count value
                if (mask == word):
                    solved = True
                    count  = maximum

                # Display the ASCII art panel for the current count value
                clear()
                print()
                for i in range(height):
                    line = lines[(count * height) + i]
                    line = line.ljust(width, " ")
                    if (i == 3):
                        line = line + " Welcome to HANGMAN"
                    elif (i == 4):
                        line = line + " " + category
                    elif (i == 7):
                        line = line + " " + mask
                    elif (i == 11):
                        line = line + " Remaining Letters:"
                    elif (i == 12):
                        line = line + " " + remain
                    print(line)

                # If solved, exit the loop (winning screen has been drawn)
                if (solved):
                    continue

                # Otherwise, check for remaining guesses
                if (count < (maximum - 1)):

                    # Read the next guess (limit to the remaining letters only)
                    guess = ""
                    while (len(guess) != 1) or (guess not in remain):
                        guess = input( \
                            "Please choose one of the remaining letters: ")
                        guess = guess.upper()
                    remain = remain.replace(guess, " ")

                    # Check for a correct guess and update the mask
                    if (guess != " ") and (guess in word):
                        mask = get_new_mask(word, mask, guess)
                        continue

                # Increment the counter for an incorrect guess
                count += 1

            # Display the solution message
            message = "GACK!"
            if (solved):
                message = "Congratulations!"
            print(message + "  The solution was " + word)

            # Prompt for another game
            more = ""
            while (len(more) != 1) or (more not in "YN"):
                more = input("Do you want to play another game? (Y/N): ")
                more = more.upper()

    except Exception as e:
        print(str(e))


# Start the module interactively
if __name__ == "__main__":
    start_hangman()
