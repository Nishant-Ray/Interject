from flask import Flask, render_template, session, request, send_file, Response, redirect, url_for, flash
from flask_session import Session

app = Flask(__name__)

app.secret_key = "hello there"

users = []

admin = {
    "email": "janedoe@gmail.com",
    "password": "hello123",
    "name": "Jane Doe",
    "dob": "1990-08-24",
    "queue": ["", False, False, False, None, ""],
    "xp": 0,
    "rank": "Amateur"
}

user1 = {
    "email": "kevinlewis@gmail.com",
    "password": "hello123",
    "name": "Kevin Lewis",
    "dob": "1990-01-01",
    "queue": ["", False, False, False, None, ""],
    "xp": 0,
    "rank": "Amateur"
}

users.append(admin)
users.append(user1)

@app.route("/", methods=["POST", "GET"])
def index():
    global users
    
    if "currentUser" not in session:
        return redirect(url_for('login'))
    
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    global users

    if request.method == "POST":
        # Get login form data

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        accountMatch = False

        for user in users:
            if newUser.get("email") == user.get("email") and newUser.get("password") == user.get("password"):
                session["currentUser"] = user
                accountMatch = True

        if accountMatch:
            return redirect(url_for('index'))
        else:
            print("Incorrect email or password!")
            return render_template("login.html")
        
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    global users

    if request.method == "POST":
        # Get register form data

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"],
            "name": request.form["nm"],
            "dob": request.form["dob"],
            "queue": ["", False, False, False, None, ""],
            "xp": 0,
            "rank": "Amateur"
        }

        accountExists = False

        for user in users:
            if newUser.get("email") == user.get("email"):
                accountExists = True
        
        if not accountExists:
            print("Registration successful!")

            users.append(newUser)
            session["currentUser"] = newUser

            return redirect(url_for('index'))
        else:
            print("Account with that email exists!")
            return render_template("register.html")
    
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("register.html")

@app.route("/topics:<mode>")
def topics(mode):
    global users
    
    if "currentUser" not in session:
        return redirect(url_for('login'))
    else:
        return render_template("topics.html")

@app.route("/side:<mode>:<q>")
def question(mode, q):
    global users

    if "currentUser" not in session:
        return redirect(url_for('login'))
    else:
        question = q

        for x in range(len(question)):
            if question[x] == '_':
                new = list(question)
                new[x] = ' '
                question = ''.join(new)

        question += "?"

        queue = [question, True, False, False, None, ""] # question, side, isQueueing, inGame, opponent, argument

        session["currentUser"]["queue"] = queue
        updateCurrentUser()

        return render_template("side.html")

@app.route("/findplayer:<side>:<q>")
def findplayer(side, q):
    global users

    if "currentUser" not in session:
        return redirect(url_for('login'))
    else:
        if side == "yes":
            session["currentUser"]["queue"][1] = True
        else:
            session["currentUser"]["queue"][1] = False
        
        session["currentUser"]["queue"][2] = True

        updateCurrentUser()
        restoreCurrentUser()
        for user in users:
            if user["email"] is not session["currentUser"]["email"]:
                #print(session["currentUser"]["email"] + ": " + str(session["currentUser"]["queue"]) + " vs " + user["email"] + ": " + str(user["queue"]))
                #print(1)
                if user["queue"][0] == session["currentUser"]["queue"][0]:
                    #print(2)
                    if user["queue"][1] is not session["currentUser"]["queue"][1]:
                        #print(3)
                        restoreCurrentUser()
                        #print(session["currentUser"]["email"] + ": " + str(session["currentUser"]["queue"]) + " vs " + user["email"] + ": " + str(user["queue"]))
                        #updateNewCurrentUser()
                        
                        #print(session["currentUser"]["queue"][3])
                        if ((True == user["queue"][2]) and (True == session["currentUser"]["queue"][2])) or (opponentFound()):
                            #print(4)
                            session["currentUser"]["queue"][4] = user
                            updateCurrentUser()

                            return redirect(url_for('online'))

        return render_template("findplayer.html")

@app.route("/online", methods=["POST", "GET"])
def online():
    global users

    if "currentUser" not in session:
        return redirect(url_for('login'))

    elif request.method == "POST":
        restoreCurrentUser()
        session["currentUser"]["queue"][5] = request.form["argument"]
        updateCurrentUser()
        
        opponentArg = getCounterArg() #session["currentUser"]["queue"][4]["queue"][5]
        print("opponent: " + opponentArg)

        return render_template("online.html", argument=session["currentUser"]["queue"][5], counterArg=opponentArg, oppName=session["currentUser"]["queue"][4]["name"])
    else:
        restoreCurrentUser()

        session["currentUser"]["queue"][2] = False
        session["currentUser"]["queue"][3] = True
        updateCurrentUser()

        opponent = session["currentUser"]["queue"][4]

        #print(opponent["queue"])

        opponent["queue"][2] = False
        opponent["queue"][3] = True
        
        #print(opponent["queue"])
        updateCurrentUser()

        return render_template("online.html")

@app.route("/offline:<side>:<q>")
def offline(side, q):
    global users

    if "currentUser" not in session:
        return redirect(url_for('login'))
    else:
        if side == "yes":
            session["currentUser"]["queue"][1] = True
        else:
            session["currentUser"]["queue"][1] = False
        updateCurrentUser()

        return render_template("offline.html")

@app.route("/logout")
def logout():
    session.pop("currentUser", None)
    return redirect(url_for("index"), code=302)

@app.context_processor
def context_processor():
    global users

    session.modified = True

    currentUser = None

    if "currentUser" in session:
        currentUser = session["currentUser"]

    return dict(users=users, currentUser=currentUser)

@app.route('/logo.png')
def logo():
    filename = 'logo.png'
    return send_file(filename, mimetype='image/png')

@app.route('/default_profile.png')
def default_profile():
    filename = 'default-profile.png'
    return send_file(filename, mimetype='image/png')

def updateCurrentUser():
    if "currentUser" in session:
        for i in range(len(users)):
            if users[i]["email"] == session["currentUser"]["email"]:
                users[i] = session["currentUser"]
                return

def restoreCurrentUser():
    if "currentUser" in session:
        for i in range(len(users)):
            if users[i]["email"] == session["currentUser"]["email"]:
                session["currentUser"] = users[i]
                return

def opponentFound():
    if "currentUser" in session:
        for i in range(len(users)):
            if users[i]["queue"][4] is not None and users[i]["queue"][4]["email"] == session["currentUser"]["email"]:
                return True
    return False

def getCounterArg():
    if "currentUser" in session:
        for i in range(len(users)):
            if users[i]["email"] == session["currentUser"]["queue"][4]["email"]:
                return users[i]["queue"][5]
    return ""

if __name__ == "__main__":
    app.run(debug=True)