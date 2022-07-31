import flask
import uuid

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
            server.currentGames.append(server.Game(uuid2, flask.request.args.get("roomName")))
            return uuid2
        else:
            return "no roomname specified, dirty cheater"
    elif requestType == "ping":
        if uuid2:
            print()
            print(server.currentGames)
            print(uuid2)
            print(ip)
            for game in server.currentGames:
                print(game.players)
                if game.players.count(uuid2) > 0:
                    return game.ping(uuid2, dict(flask.request.args))
            return "match ended"
        else:
            return "stop hacking my game, is it so hard to???"
    elif requestType == "joinGame":
        for game in server.currentGames:
            if game.id == flask.request.args.get("roomName"):
                if len(game.players) == 1:
                    uuid2 = str(uuid.uuid4())
                    game.join_player_2(uuid2)
                    return uuid2
                else:
                    return "too much players"
    return "bruh, can you just not?"


if __name__ == "__main__":
    print("app run")
    import server
    app.run(debug=True, use_reloader=False)