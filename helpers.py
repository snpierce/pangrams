from flask import render_template, g
import random
import sqlite3

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("pangrams.sqlite", check_same_thread=False)
    return db

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

def generate_apology(message, code=400):
    cur = get_db().cursor()

    cur.execute("SELECT * FROM search")
    info = cur.fetchone()
    search = info[0]
    points = info[1]
    midletter = info[2]
    max_p = info[3]

    return render_template("play.html", letters=search, midletter=midletter, max=max_p, points=points, message=message)

def find_words(abcs, midletter):
    
    dictionary = load_words()
    search_results = []
    
    for word in dictionary:
        mark = True
        for letter in word:
            if letter not in abcs:
                mark = False
        if mark == False:
            continue
        if midletter not in word:
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

    cur_len = 4
    results_by_length = []
    temp = []

    for word in results:
        if len(word) > cur_len:
             results_by_length.append(temp)
             cur_len = len(word)
             temp = []
        else:
            temp.append(word)

    results_by_length.append(temp)

    return render_template("solve.html", perf_pangrams=perf_pangrams, pangrams=pangrams, words=results_by_length)

def remove_dup(str): 
    return "".join(set(str))

def get_letters():
    pangrams = []
    with open('pangrams.txt') as file:
        valid_words = set(file.read().split())
        for word in valid_words:
            pangrams.append(word)

    num = random.randint(0, len(pangrams))

    return pangrams[num]


def calculate_ml(search):
    lengths = []
    for letter in search:
        temp = find_words(search, letter)
        lengths.append(len(temp))

    min_count = lengths[0]
    min_index = 0
    max_count = lengths[0]
    max_index = 0

    for i in range(7):
        if lengths[i] < min_count:
            min_count = lengths[i]
            min_index = i
        elif lengths[i] > max_count:
            max_count = lengths[i]
            max_index = i

    if max_count < 50:
        return search[max_index], lengths[max_index]

    if min_count > 75:
        return search[min_index], lengths[min_index]

    return search[3], lengths[3]


    






