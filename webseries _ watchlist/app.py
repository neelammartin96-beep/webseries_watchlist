from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------- DATABASE --------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------- HOME PAGE --------
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM series")
    data = cursor.fetchall()

    conn.close()
    return render_template("index.html", series=data)

# -------- ADD SERIES --------
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    genre = request.form["genre"]
    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO series (title, genre, status) VALUES (?, ?, ?)",
                   (title, genre, status))

    conn.commit()
    conn.close()

    return redirect("/")

# -------- DELETE --------
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM series WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)
    