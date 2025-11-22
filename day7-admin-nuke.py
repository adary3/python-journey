# ========================================
# DAY 7: KLEON GUESTBOOK WITH ADMIN NUKE – MESSAGES THAT NEVER DIE
# ========================================

from flask import Flask, render_template_string, request, redirect
import os
from datetime import datetime

app = Flask(__name__)

GUESTBOOK_FILE = "guestbook.txt"
PASSWORD = "kleeon2222"

def load_messages():
    if os.path.exists(GUESTBOOK_FILE):
        with open(GUESTBOOK_FILE, "r") as f:
            return f.readlines()
    return []

def add_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(GUESTBOOK_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def clear_guestbook(pwd):
    if pwd == PASSWORD:
        open(GUESTBOOK_FILE, "w").close()
        return True
    return False

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>KLEON GUESTBOOK</title>
    <style>
        body {font-family: Arial; background: black; color: #00ff41; text-align: center; padding: 50px;}
        input, button {padding: 15px; font-size: 20px; margin: 10px;}
        button {background: #00ff41; color: black;}
        .msg {margin: 20px; font-size: 18px;}
        .admin {color: red; margin-top: 50px;}
    </style>
<body>
    <h1>I AM KLEON @a_dary33</h1>
    <h2>LEAVE YOUR MARK BEFORE YOU GO</h2>
    <form action="/" method="post">
        <input name="msg" placeholder="Your message to the empire..." required style="width:500px;">
        <button>SIGN THE GUESTBOOK</button>
    </form>

    {% if cleared %}
    <h2 style="color:red;">Guestbook wiped by Kleeon!</h2>
    {% endif %}
    <h3>VOICES OF THE CONQUERED ({{ messages|length }})</h3>
    {% for line in messages[::-1] %}
        <div class="msg">{{ line }}</div>
        {% else %}
        <p>No souls yet... be the first</p>
    {% endfor %}

    <div class="admin">
    <form action="/clear" method="post">
        <input type="password" name="pwd" placeholder="Admin password to clear guestbook">
        <button style="background:red;">CLEAR GUESTBOOK(KLEEON ONLY)</button>
        </form>
        </div>

    <p><i>Day 6 of #PythonPower Only KLEEON can erase history</i></p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    cleared = False
    if request.method == "POST":
        if "msg" in request.form:
            add_message(request.form["msg"])
    messages = load_messages()
    return render_template_string(HTML, messages=messages, cleared=cleared)

@app.route("/clear", methods=["POST"])
def clear():
    if clear_guestbook(request.form.get("pwd", "")):
        messages = load_messages()
        return render_template_string(HTML, messages=messages, cleared=True)
    else:
        return "<h1 style='color:red; text-align:center; padding:100px;'>ACCESS DENIED - WRONG PASSWORD</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
