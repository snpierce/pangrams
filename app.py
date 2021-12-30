from flask import Flask, redirect, render_template, request, session, url_for, g
from flask_session import Session
from helpers import search_apology, find_words, clean_list, get_letters, calculate_ml, generate_apology, get_db

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solve", methods=["GET", "POST"])
def solve():
    
    if request.method == "POST":
        search = (request.form.get("pangram")).lower()
        midletter = (request.form.get("midletter")).lower()

        if len(search) != 7:
            return search_apology("Incorrect amount of letters.")

        if len(midletter) > 1:
            return search_apology("Enter one middle letter, or enter none to produce all possible words.")

        abcs = []
        for letter in search:
            if letter not in abcs:
                abcs.append(letter)
            else:
                return search_apology("Please enter unique letters.")
        
        if midletter not in abcs:
            return search_apology("Middle letter not found in entered letter set.")
        
        results = find_words(abcs, midletter)
        
        return clean_list(results, abcs)

    else:
        perf_pangrams = []
        pangrams = []
        words = []
        return render_template("solve.html", perf_pangrams=perf_pangrams, pangrams=pangrams, words=words)


@app.route("/generate", methods=["GET", "POST"])
def generate():

    if request.method == "POST":

        random = get_letters()

        return redirect(url_for("generate_play", search=random))
    else:
        return render_template("generate.html")

        
@app.route("/generate/<search>", methods=["GET", "POST"])
def generate_play(search):
    cur = get_db().cursor()

    if request.method == "POST":

        if not request.form.get("guess"):
            return generate_apology("Please enter guess.")
        
        guess = request.form.get("guess")

        if len(guess) < 4:
            return generate_apology("Too short.")

        
        cur.execute("SELECT * FROM search")
        info = cur.fetchone()
        search = info[0]
        points = info[1]
        midletter = info[2]
        max_p = info[3]

        if midletter not in guess:
            return generate_apology("Missing middle letter.")

        for letter in guess:
            if letter not in search:
                return generate_apology("Includes non-valid letters.")
        
        wlist = []
        guesses = []

        for row in cur.execute('SELECT word FROM list'):
            wlist.append(row[0])
 
        for row in cur.execute('SELECT word FROM guessed'):
            guesses.append(row[0])

        if guess in wlist:
            if guess not in guesses:
                cur.execute("INSERT INTO guessed (word) Values (?)", (guess,))
                cur.execute("UPDATE search SET points = ?", (points + 1,))
                get_db().commit()
            else:
                return generate_apology("Already found.")
        else:
            return generate_apology("Not in word list.")
        
        guessed = []
        for row in cur.execute('SELECT word FROM guessed'):
            guessed.append(row[0])

        cur.execute("SELECT points FROM search")
        point = cur.fetchone()[0]

        return render_template("play.html", letters=search, midletter=midletter, max=max_p, points=point, correct=guessed)

    else:
        midletter, max_p = calculate_ml(search)
        wlist = find_words(search, midletter)
        guessed = []
        
        cur.execute("DELETE FROM search")
        cur.execute("DELETE FROM guessed")
        cur.execute("DELETE FROM list")
        cur.execute("INSERT INTO search (search, points, midlet, max_p) Values (?, ?, ?, ?)", (search, 0, midletter, max_p,))

        for word in wlist:
            cur.execute("INSERT INTO list (word) Values (?)", (word,))
        get_db().commit()

        cur.execute("SELECT points FROM search")
        points = cur.fetchone()[0]

        return render_template("play.html", letters=search, midletter=midletter, max=max_p, points=points)
