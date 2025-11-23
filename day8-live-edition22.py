# DAY 8 — FINAL, TESTED, NO MORE BUGS
from flask import Flask, render_template_string, request
import os
from datetime import datetime

app = Flask(__name__)
GUESTBOOK = "guestbook.txt"
PASSWORD = "kleon2025"
BAD_WORDS = ["fuck", "shit", "bitch", "asshole", "cunt", "nigger", "faggot"]

def load_messages():
    if os.path.exists(GUESTBOOK):
        with open(GUESTBOOK, "r") as f:
            return f.readlines()
    return []

def save_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    clean = " ".join(["*" if any(b in w.lower() for b in BAD_WORDS) else w for w in msg.split()])
    with open(GUESTBOOK, "a") as f:
        f.write(f"[{timestamp}] {clean}\n")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>KLEON EMPIRE</title>
    <meta http-equiv="refresh" content="6">
    <style>
        body {font-family: Arial; background: black; color: #00ff41; text-align: center; padding: 40px;}
        input, button {padding: 15px; font-size: 20px;}
        button {background: #00ff41; color: black; cursor: pointer;}
        .msg {margin: 12px; font-size: 19px;}
        .admin {color: red; margin-top: 60px;}
    </style>
</head>
<body>
    <h1>I AM KLEON – @a_dary33</h1>
    <h2>LEAVE YOUR MARK</h2>
    <form method="post">
        <input name="msg" placeholder="Your message..." required style="width:500px;">
        <button>SIGN</button>
    </form>

    <h3>VOICES ({{ messages|length }})</h3>
    {% for line in messages[::-1] %}
        <div class="msg">{{ line }}</div>
    {% else %}
        <p>No souls yet...</p>
    {% endfor %}

    <div class="admin">
        <form action="/nuke" method="post">
            <input type="password" name="pwd" placeholder="Admin password">
            <button style="background:red;color:white;">NUKE (KLEON ONLY)</button>
        </form>
    </div>
    <p><i>Day 8 – Live + Censored</i></p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        save_message(request.form["msg"])
    return render_template_string(HTML, messages=load_messages())

@app.route("/nuke", methods=["POST"])
def nuke():
    if request.form.get("pwd") == PASSWORD:
        open(GUESTBOOK, "w").close()
        return "<h1 style='color:red;background:black;padding:100px;'>PURGED BY KLEON</h1>"
    return "<h1 style='color:red;background:black;padding:100px;'>WRONG PASSWORD</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)