from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
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
@login_required
def index():

    current_username = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

    id = request.form.get("note-id")

    # list of possible notes statuses
    status = {"active_status": "active", "deleted_status": "deleted", "archived_status": "archived"}

    # group tags to display in navbar
    tags = db.execute(
        "SELECT tag, COUNT(*) AS number FROM notes WHERE user_id = ? AND status = ? GROUP BY tag", session["user_id"], status["active_status"])
    
    # possible views of notes
    all_notes = db.execute("SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC ", session["user_id"])
    active_notes = db.execute("SELECT * FROM notes WHERE user_id = ? AND status = ? ORDER BY id DESC ", session["user_id"], status["active_status"])
    deleted_notes = db.execute("SELECT * FROM notes WHERE user_id = ? AND status = ? ORDER BY id DESC ", session["user_id"], status["deleted_status"])
    archived_notes = db.execute("SELECT * FROM notes WHERE user_id = ? AND status = ? ORDER BY id DESC ", session["user_id"], status["archived_status"])


    # User reached route via POST
    if request.method == "POST":

        if request.form['action'] == 'All notes':
            return render_template('index.html', notes=all_notes, tags=tags, current_username=current_username)
        
        elif request.form['action'] == 'Active':
            return render_template('index.html', notes=active_notes, tags=tags, current_username=current_username)

        elif request.form['action'] == 'Archive':
            return render_template('index.html', notes=archived_notes, tags=tags, current_username=current_username)

        elif request.form['action'] == 'Trash bin':
            return render_template('index.html', notes=deleted_notes, tags=tags, current_username=current_username)

        elif request.form['action'] == 'New note':
            return render_template('index.html', notes=active_notes, tags=tags, current_username=current_username)
        
        elif request.form['action'] == 'Empty note':
            
            return render_template('index.html', notes=active_notes, tags=tags, current_username=current_username)

        elif request.form['action'] == 'Edit':
            note = db.execute("SELECT id, title, tag, description, user_id FROM notes WHERE id = ? AND user_id = ?", id, session["user_id"])

            textarea = note[0]["description"]
            title = note[0]["title"]
            tag = note[0]["tag"]
            id = note[0]["id"]

            return render_template("index.html", id=id, notes=active_notes, tag=tag, tags=tags, title=title, textarea=textarea, current_username=current_username)

        elif request.form['action'] == 'Delete':
            db.execute("UPDATE notes SET status = ? WHERE id = ? AND user_id = ?", status["deleted_status"], id, session["user_id"])
            return redirect("/")
        
        elif request.form['action'] == 'Delete Note':
            current_id = request.form.get("current-note-id")
            
            if current_id:
                db.execute("UPDATE notes SET status = ? WHERE id = ? AND user_id = ?", status["deleted_status"], current_id, session["user_id"])
                return redirect("/")
            
            return redirect("/")

        elif request.form['action'] == 'Archive Note':
            current_id = request.form.get("current-note-id")
            
            if current_id:
                db.execute("UPDATE notes SET status = ? WHERE id = ? AND user_id = ?", status["archived_status"], current_id, session["user_id"])
                return redirect("/")
            
            return redirect("/")        

        elif request.form['action'] == 'Save Note':
            
            title = request.form.get("note-title").capitalize()
            tag = request.form.get("note-tag").lower()
            text = request.form.get("text-area")
            current_id = request.form.get("current-note-id")

            if current_id:
                current_note = db.execute("SELECT * FROM notes WHERE id = ? AND user_id = ?", current_id, session["user_id"])[0]

                if not title:
                    title = current_note["title"]
                if not tag:
                    tag = current_note["tag"]
                if not text:
                    text = current_note["description"]
                
                db.execute("UPDATE notes SET title = ?, description = ?, tag = ?, status = ?, date = CURRENT_TIMESTAMP WHERE id = ? and user_id = ?", title, text, tag, status["active_status"], current_id, session["user_id"])
            else:     
                db.execute("INSERT INTO notes (title, description, tag, status, user_id) VALUES (?, ?, ?, ?, ?)", title, text, tag, status["active_status"], session["user_id"])
            
            return redirect("/")

        elif request.form['action'] == '+':

            text =" "
            return render_template("index.html", textarea=text, notes=active_notes, tags=tags, current_username=current_username)

        else:
            return render_template("index.html", notes=active_notes, tags=tags, current_username=current_username)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", notes=active_notes, tags=tags, current_username=current_username)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            flash("Must provide email")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")
        
        email = request.form.get("email")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?",
                          email)
        
                # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("You are successfuly logged in!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    title = "Password must contain at least 8 characters, and at least one lowercase, one uppercase, one number and one special character."
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&-.,])[A-Za-z\d@$!%*?&-.,]{8,}$'
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Require username. Render apology if user’s input is blank or the username already exists.
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("register.html", title=title)

        # Require email. Render apology if user’s input is blank or the email already exists.
        if not request.form.get("email"):
            flash("Must provide email")
            return render_template("register.html", title=title)

        # Require password. Render an apology if password is blank or the passwords do not match
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("register.html", title=title)

        # Require users’ passwords to have at least 1 upper, 1 lower, 1 number and 1 symbol
        if not re.match(regex, request.form.get("password")):
            flash("Password must be at least 8 characters and contain uppercase, lowercase, number and symbol")
            return render_template("register.html", title=title)


        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Render an apology if passwords do not match
        if password != confirmation:
            flash("Passwords don't match")
            return render_template("register.html", title=title)

        # Query database for email
        user_db = db.execute("SELECT * FROM users WHERE email = ?",
                             email)

        # Render apology if email already exists
        if user_db:
            flash("User already exist")
            return render_template("register.html", title=title)

        # INSERT the new user into users
        db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), email)

        # Redirect user to home page
        flash("You are successfuly registered!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", title=title)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("You are now logged out!")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.75")