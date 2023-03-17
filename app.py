import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import re

# Configure application
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
# Configure session to use filesystem (instead of signed cookies)
# Session has a default time limit of some number of minutes or hours or days after which it will expire.
app.config["SESSION_PERMANENT"] = False
#  It will store in the hard drive (these files are stored under a /flask_session folder in your config directory.)v
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///noteapp.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    id = request.form.get("note-id")

    # standard behaviour
    tags = db.execute(
        "SELECT tag, COUNT(*) AS number FROM notes GROUP BY tag")
    notes = db.execute("SELECT * FROM notes ORDER BY id DESC")

    if request.method == "POST":

        if request.form['action'] == "New note":
            return render_template("index.html", notes=notes, tags=tags)

        elif request.form['action'] == 'Edit':
            note = db.execute("SELECT id, title, tag, description FROM notes WHERE id = ?", id)

            textarea = note[0]["description"]
            title = note[0]["title"]
            tag = note[0]["tag"]
            id = note[0]["id"]

            return render_template("index.html", id=id, notes=notes, tag=tag, tags=tags, title=title, textarea=textarea)

        elif request.form['action'] == 'Delete':
            db.execute("DELETE FROM notes WHERE id = ?", id)
            return redirect("/")
        
        elif request.form['action'] == 'Delete Note':
            current_id = request.form.get("current-note-id")
            
            if current_id:
                db.execute("DELETE FROM notes WHERE id = ?", current_id)
            
            return redirect("/")

        elif request.form['action'] == 'Save Note':
            
            title = request.form.get("note-title").capitalize()
            tag = request.form.get("note-tag").lower()
            text = request.form.get("text-area")
            current_id = request.form.get("current-note-id")

            if current_id:
                current_note = db.execute("SELECT * FROM notes WHERE id = ?", current_id)[0]

                if not title:
                    title = current_note["title"]
                if not tag:
                    tag = current_note["tag"]
                if not text:
                    text = current_note["description"]
                date = current_note["date"]
                
                db.execute("UPDATE notes SET title = ?, description = ?, tag = ?, date = CURRENT_TIMESTAMP WHERE id = ?", title, text, tag, current_id)
            else:     
                db.execute("INSERT INTO notes (title, description, tag) VALUES (?, ?, ?)", title, text, tag)
            
            return redirect("/")

        elif request.form['action'] == '+':

            text =" "
            return render_template("index.html", textarea=text, notes=notes, tags=tags)

        elif request.form['tag-action']:

            tag_name = request.form.get("tag-action")
            notes = db.execute("SELECT * FROM notes ORDER BY id DESC WHERE tag = ?", tag_name)

            return render_template("index.html", notes=notes, tags=tags)

        else:
            return render_template("index.html", notes=notes, tags=tags)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", notes=notes, tags=tags)

