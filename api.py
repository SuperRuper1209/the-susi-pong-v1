import json
import time
from fastapi import FastAPI
import server


app = FastAPI()


@app.get("/ping-susi/")
def api(requestType, uuid=None, roomName=None, additionalArgs=None):
    if additionalArgs:
        additionalArgs = json.loads(additionalArgs)

    if requestType == "newGame":
        if roomName:
            uuid2 = str(uuid.uuid4())
            return server.addGame(uuid2, roomName)
        else:
            return "no room name specified, dirty cheater"
    elif requestType == "ping":
        if uuid and additionalArgs:
            print()
            print(server.currentGames)
            print(uuid)
            return server.ping(uuid, additionalArgs)
        else:
            return "stop hacking my game, is it so hard to???"
    elif requestType == "joinGame" and additionalArgs:
        return server.joinGame(additionalArgs)
    return "bruh, can you just not?"


while 1:
    time.sleep(1/server.tps)
    server.tick()