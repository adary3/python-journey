#=================================================
# REAL-TIME+ VISITOR COUNTER + CUSTOM DOMAIN READY
#==================================================

# DAY 9 — REAL-TIME + VISITOR COUNTER + CUSTOM DOMAIN READY
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
GUESTBOOK = "guestbook.txt"
VISITORS = "visitors.txt"
PASSWORD = "kleon2025"
BAD_WORDS = ["fuck", "shit", "bitch", "asshole", "cunt", "nigger", "faggot"]

def load_messages():
    if os.path.exists(GUESTBOOK):
        with open(GUESTBOOK, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    clean = " ".join(["***" if any(b in w.lower() for b in BAD_WORDS) else w for w in msg.split()])
    with open(GUESTBOOK, "a") as f:
        f.write(f"[{timestamp}] {clean}\n")

def get_visitors():
    if os.path.exists(VISITORS):
        with open(VISITORS, "r") as f:
            return int(f.read().strip() or 0)
    return 0

def increment_visitor():
    count = get_visitors() + 1
    with open(VISITORS, "w") as f:
        f.write(str(count))
    return count

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>KLEON EMPIRE</title>
    <style>
        body {font-family: Arial; background: black; color: #00ff41; text-align: center; padding: 40px; margin:0;}
        input, button {padding: 15px; font-size: 20px;}
        button {background: #00ff41; color: black; cursor: pointer;}
        .msg {margin: 10px; font-size: 19px;}
        .admin {color: red; margin-top: 60px;}
        #count {font-size: 28px; margin: 20px;}
    </style>
</head>
<body>
    <h1>I AM KLEON – @a_dary33</h1>
    <h2>THE EMPIRE IS ALIVE</h2>
    <div id="count">Souls conquered: <b>{{ visitors }}</b></div>

    <form id="form">
        <input name="msg" id="msg" placeholder="Speak..." required style="width:500px;">
        <button>SIGN</button>
    </form>

    <div id="messages">
        {% for line in messages[::-1] %}
            <div class="msg">{{ line }}</div>
        {% else %}
            <p>No souls yet...</p>
        {% endfor %}
    </div>

    <div class="admin">
        <form action="/nuke" method="post">
            <input type="password" name="pwd" placeholder="Admin password">
            <button style="background:red;color:white;">NUKE</button>
        </form>
    </div>

    <script>
        const form = document.getElementById('form');
        const input = document.getElementById('msg');
        form.onsubmit = async (e) => {
            e.preventDefault();
            await fetch('/', {method: 'POST', body: new FormData(form)});
            input.value = '';
            loadMessages();
        };
        async function loadMessages() {
            const res = await fetch('/messages');
            const data = await res.json();
            document.getElementById('messages').innerHTML = data.messages.map(m =>
                `<div class="msg">${m}</div>`).join('') || '<p>No souls yet...</p>';
            document.getElementById('count').innerHTML = `Souls conquered: <b>${data.visitors}</b>`;
        }
        setInterval(loadMessages, 3000);
        loadMessages();
    </script>
    <p><i>Day 9 – Real-time. Unstoppable.</i></p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        save_message(request.form["msg"])
    visitors = increment_visitor()
    return render_template_string(HTML, messages=load_messages(), visitors=visitors)

@app.route("/messages")
def messages_json():
    return jsonify({"messages": load_messages(), "visitors": get_visitors()})

@app.route("/nuke", methods=["POST"])
def nuke():
    if request.form.get("pwd") == PASSWORD:
        open(GUESTBOOK, "w").close()
        return "PURGED"
    return "DENIED", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)