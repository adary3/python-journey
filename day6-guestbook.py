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

HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>KLEON GUESTBOOK</title></head>
<style>
    body {font-family: Arial; text-align: center; padding: 50px; background: black; color: #00ff41;}
    input, button {padding: 15px; font-size: 20px; margin: 10px;}
    button {background: #00ff41; color: black; cursor: pointer;}
</style>
<body>
    <h1>I AM KLEON - @a_dary33</h1>
    <h2>YOU CAN'T HIDE. LEAVE YOUR MARK.</h2>
    <form action="/submit" method="post">
        <input name="message" placeholder="Your message to the empire..." required style="width:400px;">
        <button type="submit">SIGN THE GUESTBOOK</button>
    </form>
    <p><i>Day 6 of #PythonPower - Messages live forever</i></p>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


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

    return "<h1 style='color:#00ff41; background:black; text-align:center; padding:100px;'>MESSAGE ETCHED INTO ETERNITY</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
