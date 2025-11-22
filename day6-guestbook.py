# ========================================
# DAY 6: KLEON GUESTBOOK – MESSAGES THAT NEVER DIE
# ========================================

from flask import Flask, render_template_string, request
import os
from datetime import datetime

app = Flask(__name__)

GUESTBOOK_FILE = "guestbook.txt"

def load_messages():
    if os.path.exists(GUESTBOOK_FILE):
        with open(GUESTBOOK_FILE, "r") as f:
            return f.readlines()
    return []

def add_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(GUESTBOOK_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

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
    </style>
</head>
<body>
    <h1>I AM KLEON @a_dary33</h1>
    <h2>LEAVE YOUR MARK BEFORE YOU GO</h2>
    <form action="/" method="post">
        <input name="msg" placeholder="Your message to the empire..." required style="width:500px;">
        <button>SIGN THE GUESTBOOK</button>
    </form>
    <h3>VOICES OF THE CONQUERED</h3>
    {% for line in messages %}
        <div class="msg">{{ line }}</div>
        {% else %}
        <p>No souls yet... be the first</p>
    {% endfor %}
    <p><i>Day 6 of #PythonPower The empire remembers</i></p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        msg = request.form["msg"]
        add_message(msg)
    messages = load_messages()
    return render_template_string(HTML, messages=messages[::-1])  # newest first

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
