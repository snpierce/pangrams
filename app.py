from flask import Flask, redirect, render_template, request, session, url_for, g
from flask_session import Session
from helpers import search_apology, find_words, clean_list

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

        if len(search) != 7:
            return search_apology("Incorrect amount of letters.")

        abcs = []
        for letter in search:
            if letter not in abcs:
                abcs.append(letter)
            else:
                return search_apology("Please enter unique letters.")
        
        results = find_words(search, abcs)
        
        return clean_list(results, abcs)

    else:
        perf_pangrams = []
        pangrams = []
        words = []
        return render_template("solve.html", perf_pangrams=perf_pangrams, pangrams=pangrams, words=words)


@app.route("/generate")
def generate():
    return render_template("generate.html")
