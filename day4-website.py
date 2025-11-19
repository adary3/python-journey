# ===============================================================
# Day 4: Simple web server with Flask - @a_dary33 | #PythonPower
# ===============================================================

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
<h1 style="text-align:center; margin-top:100px; font-size:80px; color:#00ff41;">
I AM @a_daryy33 - KLEEON
</h1>
<h2 style="text-align:center; color:white; background-color:black; padding:20px;">
Welcome to my Flask-powered web server!<br>
YOU CAN'T HIDE FROM KLEEON!
</h2>
<p style="text-align:center; font-size:30px;">
Day 4 of 'PythonPower<br>
YOU COULD NEVER ESCAPE ME!
</p>
"""

if __name__ == "__main__":
    app.run(debug=True)
