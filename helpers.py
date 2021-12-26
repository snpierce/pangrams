from flask import render_template

def load_words():
    dictionary = []
    with open('english3.txt') as word_file:
        valid_words = set(word_file.read().split())
        for word in valid_words:
            if len(word) > 3:
                dictionary.append(word)

    return dictionary

def search_apology(message, code=400):
    return render_template("search_apology.html", message=message), code

def find_words(search):
    abcs = []
    for letter in search:
        if letter not in abcs:
            abcs.append(letter)
        else:
            return search_apology("Please enter unique letters.")
    
    dictionary = load_words()
    search_results = []
    
    for word in dictionary:
        mark = True
        for letter in word:
            if letter not in abcs:
                mark = False
        if mark == False:
            continue
        search_results.append(word)

    clean_list(search_results, abcs)

def clean_list(results, letters):
    return 

