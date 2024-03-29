## Welcome to snpierce-pangrams

This is a self-made site that takes a dictionary file, loads it, and then uses it to generate pangrams (NYT Spelling Bee parameters) and solve inputted ones. It's a Flask application that can be run by cloning this repository, downloading required packages, and hosting the url on your local computer.

Functions:
- Solve for viable words using inputted 7-letter set (option to select center letter)
- Play game iteration
    - Randomly selects 7-letter set and center letter
    - User inputs guesses (are error checked)
    - If viable guess, displays alongside all guesses

Dataset:
- Pre-processed dictionary file to identify unique 7-letter combinations where there exists a reasonable amount of English words created using only those letters
- Pangrams.txt contains list of letter sets that app.py selects from
- Pangrams.sqlite is a database that stores game data
    - The letter set
    - User guessed words
    - All possible valid words
