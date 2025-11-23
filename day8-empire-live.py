from flask import Flask, render_template_string, request, jsonify, Response
import os
from datetime import datetime
from queue import Queue

app = Flask(__name__)

GUESTBOOK = "guestbook.txt"
PASSWORD = "kleeon2222"

# banned words (lowercase)
BAD_WORDS = ["fuck", "shit", "bitch", "asshole", "cunt", "nigger", "faggot"]

# SSE clients
clients = []  # list of Queue


def load_messages():
    if os.path.exists(GUESTBOOK):
        with open(GUESTBOOK, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f]
    return []


def save_message(msg):
    """Append a message to the guestbook and notify SSE clients.
    Raises ValueError if message contains banned words.
    """
    lower = msg.lower()
    for bad in BAD_WORDS:
        if bad in lower:
            raise ValueError("profanity")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    from flask import Flask, render_template_string, request, jsonify, Response
    import os
    from datetime import datetime
    from queue import Queue

    app = Flask(__name__)

    GUESTBOOK = "guestbook.txt"
    PASSWORD = "kleeon2222"

    # banned words (lowercase)
    BAD_WORDS = ["fuck", "shit", "bitch", "asshole", "cunt", "nigger", "faggot"]

    # SSE clients
    clients = []  # list of Queue


    def load_messages():
        if os.path.exists(GUESTBOOK):
            with open(GUESTBOOK, "r", encoding="utf-8") as f:
                return [line.rstrip("\n") for line in f]
        return []


    def save_message(msg):
        """Append a message to the guestbook and notify SSE clients.
        Raises ValueError if message contains banned words.
        """
        lower = msg.lower()
        for bad in BAD_WORDS:
            if bad in lower:
                raise ValueError("profanity")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        line = f"[{timestamp}] {msg}"
        with open(GUESTBOOK, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        # notify SSE clients
        for q in list(clients):
            try:
                q.put(line)
            except Exception:
                pass


    HTML = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>KLEEON GUESTBOOK - LIVE EDITION</title>
      <style>
        body {font-family: Arial; background: black; color:#00ff41; text-align: center; padding: 40px;}
        input, button {padding: 12px; font-size: 16px; margin:8px;}
        button {background: #00ff41; color: black;}
        .msg {margin: 10px; font-size: 16px; text-align:left; width:80%; margin-left:auto; margin-right:auto;}
        .admin {color: red; margin-top: 30px;}
        .ts {font-size:12px; color:#99ffb0}
        #messages {max-height:400px; overflow:auto; margin-top:10px}
      </style>
    </head>
    <body>
      <h1>I AM KLEEON - @a_dary33</h1>
      <h2>LEAVE YOUR MARK BEFORE YOU GO</h2>

      <form id="post-form">
        <input id="msg-input" name="msg" placeholder="speak...(no swearing)" required style="width:60%;">
        <button type="submit">SIGN THE GUESTBOOK</button>
      </form>

      <div id="status" style="height:18px;margin:6px;"></div>

      <h3>VOICES OF THE PEOPLE (<span id="count">0</span>)</h3>
      <div id="messages"></div>

      <div class="admin">
        <form action="/nuke" method="post">
          <input type="password" name="pwd" placeholder="Admin password to erase all">
          <button style="background:red; color:white;">ERASE GUESTBOOK (KLEEON ONLY)</button>
          <a href="/" style="color:#99ffb0;margin-left:10px;">Refresh</a>
        </form>
      </div>

      <p><i>Day 8 of #PythonPower - Live, censored</i></p>

      <script>
        async function loadInitial(){
          const res = await fetch('/messages');
          const data = await res.json();
          const container = document.getElementById('messages');
          container.innerHTML = '';
          data.messages.forEach(line => appendLine(line));
          updateCount();
        }

        function appendLine(line){
          const container = document.getElementById('messages');
          const m = document.createElement('div');
          m.className = 'msg';
          m.innerText = line;
          container.insertBefore(m, container.firstChild);
        }

        function updateCount(){
          const count = document.getElementById('messages').children.length;
          document.getElementById('count').innerText = count;
        }

        // SSE stream for instant updates
        const evtSource = new EventSource('/stream');
        evtSource.onmessage = function(e){
          appendLine(e.data);
          updateCount();
        }

        // submit without reload using JSON
        document.getElementById('post-form').addEventListener('submit', async function(ev){
          ev.preventDefault();
          const input = document.getElementById('msg-input');
          const msg = input.value.trim();
          if(!msg) return;
          const res = await fetch('/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({msg})});
          const data = await res.json();
          const status = document.getElementById('status');
          if(data.ok){
            status.style.color = '#99ffb0'; status.innerText = 'Message accepted';
            input.value = '';
          } else {
            status.style.color = 'red'; status.innerText = data.error || 'Rejected';
          }
        });

        loadInitial();
      </script>

    </body>
    </html>
    """


    @app.route('/messages')
    def messages_api():
        return jsonify(messages=load_messages())


    @app.route('/stream')
    def stream():
        q = Queue()
        clients.append(q)

        def gen():
            try:
                while True:
                    msg = q.get()
                    yield f"data: {msg}\n\n"
            except GeneratorExit:
                pass
            finally:
                try:
                    clients.remove(q)
                except ValueError:
                    pass

        return Response(gen(), mimetype='text/event-stream')


    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            # expect JSON body {msg: ...}
            data = request.get_json() or {}
            msg = (data.get('msg') or '').strip()
            if not msg:
                return jsonify(ok=False, error='Empty message')
            try:
                save_message(msg)
                return jsonify(ok=True)
            except ValueError:
                return jsonify(ok=False, error='Profanity detected — message rejected')
            except Exception as e:
                return jsonify(ok=False, error='Failed to save message')

        # GET -> serve page
        return render_template_string(HTML)


    @app.route('/nuke', methods=['POST'])
    def nuke():
        pwd = request.form.get('pwd', '')
        if pwd != PASSWORD:
            return "<h1 style='color:red;'>INCORRECT PASSWORD. ACCESS DENIED.</h1>", 403
        try:
            open(GUESTBOOK, 'w', encoding='utf-8').close()
            # notify clients that we've nuked (send a message)
            for q in list(clients):
                try:
                    q.put('[SYSTEM] GUESTBOOK NUKED')
                except Exception:
                    pass
        except Exception:
            return "<h1 style='color:red;'>Failed to nuke guestbook</h1>", 500
        return "<h1 style='color:#00ff41;'>GUESTBOOK PURGED BY KLEEON</h1>"


    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)