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

def find_words(search, abcs):
    
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

    return search_results

# sort by word length, alphabetize, and find pangrams
def clean_list(results, letters):
    perf_pangrams = []
    pangrams = []

    for word in results:
        if sorted(letters) == sorted(word):
            perf_pangrams.append(word)
            results.remove(word)
        elif sorted(letters) == sorted(remove_dup(word)):
            pangrams.append(word)
            results.remove(word)
    
    results.sort()
    results = sorted(results, key=len)

    return render_template("solve.html", perf_pangrams=perf_pangrams, pangrams=pangrams, words=results)

def remove_dup(str): 
    return "".join(set(str))