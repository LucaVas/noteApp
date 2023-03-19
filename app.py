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

    # list of possible notes statuses
    status = {"active_status": "active", "deleted_status": "deleted", "archived_status": "archived"}

    # group tags to display in navbar
    tags = db.execute(
        "SELECT tag, COUNT(*) AS number FROM notes WHERE status = ? GROUP BY tag", status["active_status"])
    
    # possible views of notes
    all_notes = db.execute("SELECT * FROM notes ORDER BY id DESC")
    active_notes = db.execute("SELECT * FROM notes WHERE status = ? ORDER BY id DESC ", status["active_status"])
    deleted_notes = db.execute("SELECT * FROM notes WHERE status = ? ORDER BY id DESC ", status["deleted_status"])
    archived_notes = db.execute("SELECT * FROM notes WHERE status = ? ORDER BY id DESC ", status["archived_status"])


    # User reached route via POST
    if request.method == "POST":

        if request.form["action"] == "All notes":
            return render_template("index.html", notes=all_notes, tags=tags)
        
        elif request.form["action"] == "Active":
            return render_template("index.html", notes=active_notes, tags=tags)

        elif request.form["action"] == "Archive":
            return render_template("index.html", notes=archived_notes, tags=tags)

        elif request.form["action"] == "Trash bin":
            return render_template("index.html", notes=deleted_notes, tags=tags)

        elif request.form['action'] == "New note":
            return render_template("index.html", notes=active_notes, tags=tags)

        elif request.form['action'] == 'Edit':
            note = db.execute("SELECT id, title, tag, description FROM notes WHERE id = ?", id)

            textarea = note[0]["description"]
            title = note[0]["title"]
            tag = note[0]["tag"]
            id = note[0]["id"]

            return render_template("index.html", id=id, notes=active_notes, tag=tag, tags=tags, title=title, textarea=textarea)

        elif request.form['action'] == 'Delete':
            db.execute("UPDATE notes SET status = ? WHERE id = ?", status["deleted_status"], id)
            return redirect("/")
        
        elif request.form['action'] == 'Delete Note':
            current_id = request.form.get("current-note-id")
            
            if current_id:
                db.execute("UPDATE notes SET status = ? WHERE id = ?", status["deleted_status"], current_id)
                return redirect("/")
            
            return redirect("/")

        elif request.form['action'] == 'Archive Note':
            current_id = request.form.get("current-note-id")
            
            if current_id:
                db.execute("UPDATE notes SET status = ? WHERE id = ?", status["archived_status"], current_id)
                return redirect("/")
            
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
                
                db.execute("UPDATE notes SET title = ?, description = ?, tag = ?, status = ?, date = CURRENT_TIMESTAMP WHERE id = ?", title, text, tag, status["active_status"], current_id)
            else:     
                db.execute("INSERT INTO notes (title, description, tag, status) VALUES (?, ?, ?, ?)", title, text, tag, status["active_status"])
            
            return redirect("/")

        elif request.form['action'] == '+':

            text =" "
            return render_template("index.html", textarea=text, notes=active_notes, tags=tags)

        else:
            return render_template("index.html", notes=active_notes, tags=tags)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", notes=active_notes, tags=tags)

