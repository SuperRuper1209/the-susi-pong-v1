import multiprocessing
import flask
import uuid
import os
import socket
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print(IPAddr)
print(hostname)

print(os.environ)


app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route("/ping-susi/")
def api():
    uuid2 = flask.request.args.get("uuid")
    requestType = flask.request.args.get("type")
    if flask.request.headers.getlist("X-Forwarded-For"):
        ip = flask.request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = flask.request.remote_addr
    if requestType == "newGame":
        if flask.request.args.get("roomName"):
            uuid2 = str(uuid.uuid4())
            changeAddGame(uuid2, flask.request.args.get("roomName"))
            return uuid2
        else:
            return "no roomname specified, dirty cheater"
    elif requestType == "ping":
        if uuid2:
            print()
            print(currentGames)
            print(uuid2)
            print(ip)
            return ping(uuid2, flask.request.args)
        else:
            return "stop hacking my game, is it so hard to???"
    elif requestType == "joinGame":
        return joinGame(flask.request.args)
    return "bruh, can you just not?"


if __name__ == "__main__":
    multiprocessing.Process(target=loop, args=()).start()
    app.run(debug=True, use_reloader=False, threaded=True)
