#=====================================================================
# Day 5: Kleeon Empire - Dark Mode + Todo List @a_dary33 |PythonPower
# ======================================================================

from flask import Flask, render_template_string, request, redirect
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

        <button id="toggle-mode">
        TOGGLE DARK MODE
        </button>

        <h3>MY MISSIONS (LIVE FROM FILE)</h3>
        <form id="add-form" method="POST" action="/add" style="margin-bottom:20px;">
            <input name="todo" placeholder="Add a mission" style="padding:10px; font-size:16px; width:300px;" required />
            <button type="submit" style="padding:10px; font-size:16px;">Add</button>
        </form>

        <ul>
        {% for todo in todos %}
        <li style="font-size: 20px;">{{ todo }}</li>
        {% else %}
        <li>No missions yet. Add one, Kleeon!</li>
        {% endfor %}
        </ul>

        <p><i>Day 5 of #PytonPower - KLEEON EMPIRE</i></p>

        <script>
        // Cookie helpers
        function setCookie(name, value, days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "")  + expires + "; path=/";
        }
        function getCookie(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }

        function applyMode(mode) {
            document.body.className = mode;
            setCookie('mode', mode, 365);
        }

        document.getElementById('toggle-mode').addEventListener('click', function(){
            var current = document.body.className === 'dark' ? 'dark' : 'light';
            var next = current === 'dark' ? 'light' : 'dark';
            applyMode(next);
        });

        // On load, read cookie and apply
        (function(){
            var mode = getCookie('mode') || '{{ mode }}' || 'light';
            document.body.className = mode;
        })();
        </script>
        </body>
    </html>
    """

@app.route("/")
def home():
    visitors = add_visitor()
    # Reload todos from file so newly-added items appear immediately
    current_todos = load_todos()
    mode = request.cookies.get('mode', 'light')
    return render_template_string(HTML, visitors=visitors, todos=current_todos, mode=mode)


@app.route('/add', methods=['POST'])
def add():
    item = request.form.get('todo','').strip()
    if item:
        with open(TODO_FILE, 'a', encoding='utf-8') as f:
            f.write(item + '\n')
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)