import uuid
import math
import random
import json
import time

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
        self.ballSpeed = self.gridSize[0] / 2
        self.pongBall = (self.gridSize[0] / 2, self.gridSize[1] / 2, self.ballSpeed, 0)
        self.ballR = self.gridSize[0] / 32
        self.paddleSize = (self.gridSize[0] / 80, self.gridSize[1] / 4)
        self.offset = self.gridSize[0] / 80
        self.playerPoses = [self.gridSize[1] / 2, self.gridSize[1] / 2]
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
                    'otherPlrPos': self.playerPoses[1 - plrIndex],
                    'ballTransform': self.pongBall,
                    'score': self.score,
                    'time': round(self.time * 10) / 10
                }

                return json.dumps(ret)
            else:
                self.last_ping[0] = 5
                return "not started"

    def endGame(self):
        print("game ended: " + self.id)
        currentGames.remove(self)
        del self

    def tick(self, deltaTime):
        self.time -= deltaTime
        if not self.match_on:
            self.last_ping[0] -= deltaTime
            if self.last_ping[0] < 0:
                self.endGame()
        else:
            x, y = self.pongBall[0], self.pongBall[1]
            sX, sY = self.pongBall[2], self.pongBall[3]
            x2 = x + sX * deltaTime
            y2 = y + sY * deltaTime

            if self.offset - self.paddleSize[0] / 2 - self.ballR <= x2 <= self.offset + self.ballR + self.paddleSize[
                0] / 2 and self.playerPoses[0] - self.paddleSize[1] / 2 - self.ballR <= y2 <= self.playerPoses[0] + \
                    self.paddleSize[1] / 2 + self.ballR:
                sX = -sX
                degrees = math.atan2(sY, sX) / math.pi * 180
                degrees += random.randint(0, 30) - 15
                degrees = degrees * math.pi / 180
                sX, sY = math.cos(degrees) * self.ballSpeed, math.sin(degrees) * self.ballSpeed
            elif x2 + self.ballR * 2 < 0:
                x2 = 400
                y2 = 200
                sX = self.ballSpeed
                sY = 0
                self.score[0] += 1
            if self.gridSize[0] - self.offset + self.paddleSize[0] / 2 + self.ballR >= x2 >= self.gridSize[
                0] - self.offset - self.ballR - self.paddleSize[0] / 2 and self.playerPoses[1] - self.paddleSize[
                1] / 2 - self.ballR <= y2 <= self.playerPoses[1] + self.paddleSize[1] / 2 + self.ballR:
                sX = -sX
                degrees = math.atan2(sY, sX) / math.pi * 180
                degrees += random.randint(0, 30) - 15
                degrees = degrees * math.pi / 180
                sX, sY = math.cos(degrees) * self.ballSpeed, math.sin(degrees) * self.ballSpeed
            elif x2 - self.ballR * 2 > self.gridSize[0]:
                x2 = 400
                y2 = 200
                sX = self.ballSpeed
                sY = 0
                self.score[1] += 1

            if y2 - self.ballR > self.gridSize[1]:
                sY = -sY
                degrees = math.atan2(sY, sX) / math.pi * 180
                degrees += random.randint(0, 30) - 15
                degrees = degrees * math.pi / 180
                sX, sY = math.cos(degrees) * self.ballSpeed, math.sin(degrees) * self.ballSpeed
            elif y2 + self.ballR < 0:
                sY = -sY
                degrees = math.atan2(sY, sX) / math.pi * 180
                degrees += random.randint(0, 30) - 15
                degrees = degrees * math.pi / 180
                sX, sY = math.cos(degrees) * self.ballSpeed, math.sin(degrees) * self.ballSpeed

            self.pongBall = (x2, y2, sX, sY)

            self.last_ping[0] -= deltaTime
            self.last_ping[1] -= deltaTime
            if self.last_ping[0] <= 0 or self.last_ping[1] <= 0:
                self.endGame()
        if self.time <= 0:
            self.endGame()


def joinGame(args):
    for game in currentGames:
        if game.id == args.get("roomName"):
            if len(game.players) == 1:
                uuid2 = str(uuid.uuid4())
                tasks.append({"type": "joinGame", "game": game, "uuid": uuid2})
                return uuid2
            else:
                return "too much players"


def ping(uuid2, args):
    for game in currentGames:
        print(game.players)
        if game.players.count(uuid2) > 0:
            return game.ping(uuid2, dict(args))
    return "match ended"


prevTime = time.time()


tps = 1
tasks = [
    {"type": "addGame", "uuid": "dwadwa", "roomName": "dawdaw"}
]


def tick():
    global prevTime
    global currentGames

    for task in tasks:
        if task["type"] == "addGame":
            currentGames.append(Game(task["uuid"], task["roomName"]))
        elif task["type"] == "joinGame":
            task["game"].join_player_2(task["uuid"])

    deltaTime = time.time() - prevTime
    for game in currentGames:
        game.tick(deltaTime)
    prevTime = time.time()


def addGame(uuid2, roomName):
    tasks.append({"type": "addGame", "uuid": uuid2, "roomName": roomName})
    return uuid2
