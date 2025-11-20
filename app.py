#=====================================================================
# Day 5: Kleeon Empire - Dark Mode + Todo List @a_dary33 |PythonPower
# ======================================================================

from flask import Flask, render_template_string, request
import os
app = Flask(__name__)

TODO_FILE = "my_missions.txt"
VISITOR_FILE = "visitors.txt"

# Load todos
def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return ["Conquer the galaxy", "KLEEON mode activated"]

todos = load_todos()

# Visitor counter
def get_visitors():
    if os.path.exists(VISITOR_FILE):
        with open(VISITOR_FILE, "r") as f:
            try:

                return int(f.read().strip() or 0)
            except ValueError:
                return 0
    return 0

def add_visitor():
    count = get_visitors() + 1
    with open(VISITOR_FILE, "w") as f:
        f.write(str(count))
    return count

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Kleeon Empire</title>
    <style>
    body{ font-family: Arial; text-align: center; padding: 50px; transition: 0.5s; }
    .dark { background: black; color: #00ff41; }
    .light { background: white; color: black; }
    h1 {font-size: 70px; }
    button { padding: 15px; font-size: 20px; margion: 20px; }
    </style>
    </head>
    <body class ="{{ mode }}">
    <h1>I AM KLEEON - @a_dary33</h1>
    <h2>Humble Enough to know i can be replaced, Wise Enough to know that there is nobody else like me.</h2>
    <p>Visitors conquered: <b>{{ visitors }}</b></p>
    <button onclick="document.body.classList.toggle('dark'); document.body.classList.toggle('light')">
    TOGGLE DARK MODE
    </button>

    <h3>MY MISSIONS (LIVE FROM FILE)</h3>
    <ul>
    {% for todo in todos %}
    <li style="font-size: 20px;">{{ todo }}</li>
    {% else %}
    <li>No missions yet. Add one, Kleeon!</li>
    {% endfor %}
    </ul>

    <p><i>Day 5 of #PytonPower - KLEEON EMPIRE</i></p>
    </body>
    </html>
    """

@app.route("/")
def home():
    visitors = add_visitor()
    mode = request.args.get("mode", "light")
    return render_template_string(HTML, visitors=visitors, todos=todos, mode=mode)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)