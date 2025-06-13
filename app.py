from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

online_users = {}  # session_id: username

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('register')
def handle_register(data):
    username = data.get('username')
    mobile = data.get('mobile')
    session_id = request.sid
    online_users[session_id] = username
    emit('user_list', list(online_users.values()), broadcast=True)

@socketio.on('message')
def handle_message(data):
    msg = data.get('msg')
    sender = online_users.get(request.sid, "Unknown")
    emit('new_message', {'user': sender, 'msg': msg}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in online_users:
        del online_users[request.sid]
    emit('user_list', list(online_users.values()), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5000)
