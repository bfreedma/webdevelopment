import os
import requests
import datetime
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {"home": []}
channel_names = ["home"]

users = []
curr_channel = ""
curr_user = ""


@app.route("/")
def index():
    return render_template("index.html", curr_channel=curr_channel, channel_names=channel_names, channels=channels, users=users, curr_user=curr_user)


@socketio.on("start up")
def startup(data):
    current_user = data["curr_user"]
    current_channel = data["curr_channel"]
    emit("fix delete", {"curr_user": current_user,
                        "curr_channel": current_channel, "channels": channels})


@socketio.on("new user")
def usercreate(data):
    user = data["curr_user"]
    texts = data["texts"]
    if user == curr_user or texts == "yes":
        mess = "true"
        emit("create user", {"curr_user": user, "mess": mess})
    else:
        if user in users:
            mess = "false"
            emit("create user", {"curr_user": user, "mess": mess})
        else:
            mess = "true"
            users.append(user)

            emit("create user", {"curr_user": user, "mess": mess})


@socketio.on("submit message")
def message(data):
    message = data["message"]
    curr_user = data["curr_user"]
    curr_channel = data["curr_channel"]
    time = '{:%I:%M %p}'.format(datetime.datetime.now())

    message = message + \
        "<span style='color: #808080'> (" + time + ")" + \
        " -" + curr_user + "</span>"
    if len(channels[curr_channel]) >= 100:
        channels[curr_channel].pop(0)
    into = [curr_user, message]
    channels[curr_channel].append(into)

    emit("announce message", {"message": message, "curr_channel": curr_channel,
                              "curr_user": curr_user, "channels": channels}, broadcast=True)


@socketio.on("create channel")
def channel_create(data):
    chan = data["chan_name"]
    channel_names.append(chan)
    channels[chan] = []
    emit("update channels", {"channel_names": channel_names}, broadcast=True)


@socketio.on("change channel")
def channel_change(data):
    chan = data["chan"]
    curr_channel = chan
    emit("update messages channel", {
         "curr_channel": curr_channel, "channels": channels})


@socketio.on("delete")
def delete(data):
    text = data["text"]
    curr_channel = data["curr_channel"]
    user = data["curr_user"]

    for u in channels[curr_channel]:
        if u[0] == user:
            updated_text = u[1] + "<button class='hide'>Delete</button>"
            updated_text = updated_text.replace('"', '')
            updated_text = updated_text.replace("'", '')
            text = text.replace('"', '')
            text = text.replace("'", '')
            if updated_text == text:
                channels[curr_channel].remove(u)
                break
    emit("update messages", {"curr_channel": curr_channel,
                             "channels": channels}, broadcast=True)
