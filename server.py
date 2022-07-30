import flask
import threading
import time
import math
import random
import json

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


currentGames = []


class Game:
    def __init__(self, initialPlayer, roomName):
        self.time = 300
        self.players = [initialPlayer]
        self.last_ping = [5, 5]
        self.id = roomName

        print()
        print("GAME STARTED")
        print(self.id)
        print(self.players)

        self.match_on = False

        self.gridSize = (800, 400)
        self.ballSpeed = self.gridSize[0]/2
        self.pongBall = (self.gridSize[0]/2, self.gridSize[1]/2, self.ballSpeed, 0)
        self.ballR = self.gridSize[0]/32
        self.paddleSize = (self.gridSize[0]/80, self.gridSize[1]/4)
        self.offset = self.gridSize[0]/80
        self.playerPoses = [self.gridSize[1]/2, self.gridSize[1]/2]
        self.score = [0, 0]

    def join_player_2(self, plr):
        self.players.append(plr)
        self.match_on = True
        print()
        print("2ND PLAYER JOINED")
        print(self.id)
        print(self.players)

    def ping(self, plr, pingInfo):
        if "leave" in pingInfo.keys():
            plrIndex = self.players.index(plr)
            if plrIndex == 1:
                self.players.remove(plr)
                self.match_on = False
                self.pongBall = (self.gridSize[0] / 2, self.gridSize[1] / 2, self.ballSpeed, 0)
                self.playerPoses = [self.gridSize[1] / 2, self.gridSize[1] / 2]
                self.score = [0, 0]
            else:
                self.last_ping[0] = [5, 5]
                self.players[0] = self.players[1]
                del self.players[1]
                self.match_on = False
                self.pongBall = (self.gridSize[0] / 2, self.gridSize[1] / 2, self.ballSpeed, 0)
                self.playerPoses = [self.gridSize[1] / 2, self.gridSize[1] / 2]
                self.score = [0, 0]
            return "left"
        else:
            print("br")
            if self.match_on:
                newPos = pingInfo['plrPos']
                plrIndex = self.players.index(plr)
                self.playerPoses[plrIndex] = float(newPos)

                ret = {
                    'otherPlrPos': self.playerPoses[1-plrIndex],
                    'ballTransform': self.pongBall,
                    'score': self.score,
                    'time': round(self.time*10)/10
                }

                return json.dumps(ret)
            else:
                self.last_ping[0] = 5
                return "not started"

    def endGame(self):
        print("game ended: "+self.id)
        currentGames.remove(self)
        del self

    def tick(self, deltaTime):
        self.time -= deltaTime
        if not self.match_on:
            print()
            print("ping")
            print(self.last_ping)
            self.last_ping[0] -= deltaTime
            if self.last_ping[0] < 0:
                self.endGame()
        else:
            x, y = self.pongBall[0], self.pongBall[1]
            sX, sY = self.pongBall[2], self.pongBall[3]
            x2 = x+sX*deltaTime
            y2 = y+sY*deltaTime

            if self.offset-self.paddleSize[0]/2-self.ballR <= x2 <= self.offset+self.ballR+self.paddleSize[0]/2 and self.playerPoses[0]-self.paddleSize[1]/2-self.ballR <= y2 <= self.playerPoses[0]+self.paddleSize[1]/2+self.ballR:
                sX = -sX
                degrees = math.atan2(sY, sX)/math.pi*180
                degrees += random.randint(0, 30)-15
                degrees = degrees*math.pi/180
                sX, sY = math.cos(degrees)*self.ballSpeed, math.sin(degrees)*self.ballSpeed
            elif x2+self.ballR*2 < 0:
                x2 = 400
                y2 = 200
                sX = self.ballSpeed
                sY = 0
                self.score[0] += 1
            if self.gridSize[0]-self.offset+self.paddleSize[0]/2+self.ballR >= x2 >= self.gridSize[0]-self.offset-self.ballR-self.paddleSize[0]/2 and self.playerPoses[1]-self.paddleSize[1]/2-self.ballR <= y2 <= self.playerPoses[1]+self.paddleSize[1]/2+self.ballR:
                sX = -sX
                degrees = math.atan2(sY, sX)/math.pi*180
                degrees += random.randint(0, 30)-15
                degrees = degrees*math.pi/180
                sX, sY = math.cos(degrees)*self.ballSpeed, math.sin(degrees)*self.ballSpeed
            elif x2-self.ballR*2 > self.gridSize[0]:
                x2 = 400
                y2 = 200
                sX = self.ballSpeed
                sY = 0
                self.score[1] += 1

            if y2-self.ballR > self.gridSize[1]:
                sY = -sY
                degrees = math.atan2(sY, sX)/math.pi*180
                degrees += random.randint(0, 30)-15
                degrees = degrees*math.pi/180
                sX, sY = math.cos(degrees)*self.ballSpeed, math.sin(degrees)*self.ballSpeed
            elif y2+self.ballR < 0:
                sY = -sY
                degrees = math.atan2(sY, sX)/math.pi*180
                degrees += random.randint(0, 30)-15
                degrees = degrees*math.pi/180
                sX, sY = math.cos(degrees)*self.ballSpeed, math.sin(degrees)*self.ballSpeed

            self.pongBall = (x2, y2, sX, sY)

            self.last_ping[0] -= deltaTime
            self.last_ping[1] -= deltaTime
            if self.last_ping[0] <= 0 or self.last_ping[1] <= 0:
                self.endGame()
        if self.time <= 0:
            self.endGame()


@app.route("/ping-susi/")
def api():
    requestType = flask.request.args.get("type")
    ip = flask.request.remote_addr
    if requestType == "newGame":
        for game in currentGames:
            if game.players.count(ip) > 0:
                return "bruh cheater, kys"
        if flask.request.args.get("roomName"):
            currentGames.append(Game(ip, flask.request.args.get("roomName")))
            return "success"
        else:
            return "no roomname specified, dirty cheater"
    elif requestType == "ping":
        for game in currentGames:
            print(game.players)
            print(ip)
            if game.players.count(ip) > 0:
                return game.ping(ip, dict(flask.request.args))
        return "match ended"
    elif requestType == "joinGame":
        for game in currentGames:
            if game.players.count(ip) > 0:
                return "bruh cheater, stop trying breaking my game, dud, literally why"
        for game in currentGames:
            if game.id == flask.request.args.get("roomName"):
                if len(game.players) == 1:
                    game.join_player_2(flask.request.remote_addr)
                    return "success"
                else:
                    return "too much players"
    return "bruh, can you just not?"


tps = 60


def loop():
    print("app run")
    app.run(debug=True, use_reloader=False, port=80)



threading.Thread(target=loop, args=()).start()
while 1:
    print("While")
    prevTime = time.time()
    time.sleep(1/tps)
    deltaTime = time.time()-prevTime
    for game in currentGames:
        game.tick(deltaTime)
