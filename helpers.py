from flask import render_template

def load_words():
    dictionary = []
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
        for word in valid_words:
            if len(word) > 4:
                dictionary.append(word)

    return dictionary

def search_apology(message, code=400):
    return render_template("search_apology.html", message=message), code

def check_distinct(search):
    abcs = []
    for letter in search:
        if letter not in abcs:
            abcs.append(letter)
        else:
            return False
    return True
