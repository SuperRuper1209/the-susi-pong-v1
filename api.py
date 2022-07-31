import flask
import uuid
import server
import threading

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
            server.addGame = server.Game(uuid2, flask.request.args.get("roomName"))
            return uuid2
        else:
            return "no roomname specified, dirty cheater"
    elif requestType == "ping":
        if uuid2:
            print()
            print(server.currentGames)
            print(uuid2)
            print(ip)
            return server.ping(uuid2, flask.request.args)
        else:
            return "stop hacking my game, is it so hard to???"
    elif requestType == "joinGame":
        return server.joinGame(flask.request.args)
    return "bruh, can you just not?"


if __name__ == "__main__":
    print("app run")
    threading.Thread(target=server.loop, args=()).start()
    app.run(debug=True, use_reloader=False)