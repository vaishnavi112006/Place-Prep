from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aptitude INTEGER,
        coding INTEGER,
        technical INTEGER,
        communication INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS companies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        aptitude_required INTEGER,
        coding_required INTEGER,
        technical_required INTEGER,
        communication_required INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- INSERT DEFAULT COMPANIES ----------
def insert_companies():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM companies")
    count = cur.fetchone()[0]

    if count == 0:
        companies = [
            ("TCS",60,50,55,60),
            ("Infosys",65,60,60,65),
            ("Amazon",75,80,80,70)
        ]

        cur.executemany(
            "INSERT INTO companies(company_name,aptitude_required,coding_required,technical_required,communication_required) VALUES(?,?,?,?,?)",
            companies
        )

    conn.commit()
    conn.close()

insert_companies()

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (request.form["name"], request.form["email"], request.form["password"])
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (request.form["email"], request.form["password"])
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session.get("user"))


@app.route("/enter_scores", methods=["GET","POST"])
def enter_scores():
    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO scores(aptitude,coding,technical,communication) VALUES(?,?,?,?)",
            (
                int(request.form["aptitude"]),
                int(request.form["coding"]),
                int(request.form["technical"]),
                int(request.form["communication"])
            )
        )

        conn.commit()
        conn.close()

        return redirect("/evaluate")

    return render_template("scores.html")


@app.route("/evaluate")
def evaluate():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # latest scores
    cur.execute("""
        SELECT aptitude,coding,technical,communication
        FROM scores ORDER BY id DESC LIMIT 1
    """)
    scores = cur.fetchone()

    if not scores:
        return redirect("/enter_scores")

    # convert safely
    aptitude = int(scores[0])
    coding = int(scores[1])
    technical = int(scores[2])
    communication = int(scores[3])

    # get companies
    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()

    conn.close()

    weaknesses = []
    suggestions = []
    courses = []

    # ---------- SKILL ANALYSIS ----------
    if aptitude < 60:
        weaknesses.append("Aptitude")
        suggestions.append("Practice aptitude daily")
        courses.append({"name":"Aptitude Practice","link":"https://www.indiabix.com/aptitude/"})

    if coding < 60:
        weaknesses.append("Coding")
        suggestions.append("Practice DSA problems")
        courses.append({"name":"DSA Practice","link":"https://leetcode.com/"})

    if technical < 60:
        weaknesses.append("Technical")
        suggestions.append("Revise OS, DBMS, CN")
        courses.append({"name":"Core CS","link":"https://nptel.ac.in/"})

    if communication < 60:
        weaknesses.append("Communication")
        suggestions.append("Improve communication skills")
        courses.append({"name":"English Course","link":"https://www.coursera.org/"})

    # ---------- READINESS ----------
    readiness = (4 - len(weaknesses)) / 4 * 100

    # ---------- ELIGIBLE COMPANIES ----------
    eligible_companies = []

    for company in companies:
        name = company[1]

        apt_req = int(company[2]) if company[2] else 0
        cod_req = int(company[3]) if company[3] else 0
        tech_req = int(company[4]) if company[4] else 0
        comm_req = int(company[5]) if company[5] else 0

        if (aptitude >= apt_req and
            coding >= cod_req and
            technical >= tech_req and
            communication >= comm_req):
            eligible_companies.append(name)

    # ---------- IMPROVEMENT PLAN ----------
    if weaknesses:
        improvement_plan = "Focus on " + ", ".join(weaknesses) + " to unlock more companies."
    else:
        improvement_plan = "Excellent! You are ready for top companies."

    return render_template(
        "evaluate.html",
        scores=(aptitude, coding, technical, communication),
        companies=companies,
        readiness=readiness,
        weaknesses=weaknesses,
        suggestions=suggestions,
        courses=courses,
        eligible_companies=eligible_companies,
        improvement_plan=improvement_plan
    )


@app.route("/progress")
def progress():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT aptitude,coding,technical,communication,date
        FROM scores
    """)
    data = cur.fetchall()

    conn.close()

    return render_template("progress.html", data=data)


@app.route("/admin", methods=["GET","POST"])
def admin():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute(
            "INSERT INTO companies(company_name,aptitude_required,coding_required,technical_required,communication_required) VALUES(?,?,?,?,?)",
            (
                request.form["company"],
                int(request.form["aptitude"]) if request.form["aptitude"] else 0,
                int(request.form["coding"]) if request.form["coding"] else 0,
                int(request.form["technical"]) if request.form["technical"] else 0,
                int(request.form["communication"]) if request.form["communication"] else 0
            )
        )
        conn.commit()

    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()

    conn.close()

    return render_template("admin.html", companies=companies)


@app.route("/tests")
def tests():
    return render_template("tests.html")


if __name__ == "__main__":
    app.run(debug=True)