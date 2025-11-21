#==============================================================
# Day 6: Guestbook Application KLEEON
#===============================================================

from flask import Flask, render_template_string, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

#<<< Put your google sheet or Google Form POST URL here >>>
# NOTE: For Google Forms you typically need the form's `action` URL (not the spreadsheet URL).
SHEET_URL = "https://docs.google.com/spreadsheets/d/12R_GxZlXCPkkQMHTJ9dtbINljC-daLMJfTYe-vcD0ik/edit?usp=sharing"

# Replace this with your Google Form 'action' POST URL if you want submissions to go there.
FORM_URL = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse"

# Local storage for messages so they appear on the homepage
GUESTBOOK_FILE = "guestbook.json"

HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>KLEON GUESTBOOK</title></head>
<style>
        body {font-family: Arial; text-align: center; padding: 50px; background: black; color: #00ff41;}
        input, button {padding: 15px; font-size: 20px; margin: 10px;}
        button {background: #00ff41; color: black; cursor: pointer;}
        .message {background:#08120a; margin:10px auto; padding:10px; width:700px; border-radius:6px; text-align:left}
        .ts {font-size:12px; color:#99ffb0}
</style>
<body>
        <h1>I AM KLEON - @a_dary33</h1>
        <h2>YOU CAN'T HIDE. LEAVE YOUR MARK.</h2>
        <form action="/submit" method="post">
                <input name="message" placeholder="Your message to the empire..." required style="width:400px;">
                <button type="submit">SIGN THE GUESTBOOK</button>
        </form>
        <p><i>Day 6 of #PythonPower - Messages live forever</i></p>

        <h3>Recent messages</h3>
        {% if messages %}
            {% for m in messages %}
                <div class="message"><div class="ts">{{ m.timestamp }}</div><div>{{ m.message }}</div></div>
            {% endfor %}
        {% else %}
            <p>No messages yet. Be the first to sign the guestbook.</p>
        {% endif %}
</body>
</html>
"""


@app.route("/")
def home():
    messages = load_messages()
    return render_template_string(HTML, messages=messages)


@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message", "").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Send to Google Form / external endpoint via POST if configured.
    payload = {
        # Replace with the correct entry ID for your form; this is a placeholder.
        "entry.123456789": f"{timestamp} - {message}",
    }

    try:
        if FORM_URL and "YOUR_FORM_ID" not in FORM_URL:
            resp = requests.post(FORM_URL, data=payload, timeout=5)
            resp.raise_for_status()
    except Exception as e:
        # Log the error and continue — guestbook should still accept the message locally.
        print("Warning: failed to POST to FORM_URL:", e)

    # Save locally so messages are listed on the homepage
    try:
        save_message(timestamp, message)
    except Exception as e:
        print("Warning: failed to save message locally:", e)

    return "<h1 style='color:#00ff41; background:black; text-align:center; padding:100px;'>MESSAGE ETCHED INTO ETERNITY</h1>"


def load_messages():
    try:
        with open(GUESTBOOK_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # expect a list of {timestamp, message}
            return data[-50:][::-1]  # return last 50, newest first
    except FileNotFoundError:
        return []
    except Exception:
        return []


def save_message(timestamp, message):
    entry = {"timestamp": timestamp, "message": message}
    msgs = []
    try:
        with open(GUESTBOOK_FILE, 'r', encoding='utf-8') as f:
            msgs = json.load(f)
    except FileNotFoundError:
        msgs = []
    msgs.append(entry)
    with open(GUESTBOOK_FILE, 'w', encoding='utf-8') as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
