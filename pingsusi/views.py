import django.http
import json
import game_server
from django.shortcuts import render


def processThat(requestType=None, additionalArgs=None, uuid=None, roomName=None):
    if additionalArgs:
        additionalArgs = json.loads(additionalArgs)

    if requestType == "newGame":
        if roomName:
            uuid2 = str(uuid.uuid4())
            return game_server.addGame(uuid2, roomName)
        else:
            return "no room name specified, dirty cheater"
    elif requestType == "ping":
        if uuid and additionalArgs:
            return game_server.ping(uuid, additionalArgs)
        else:
            return "stop hacking my game, is it so hard to???"
    elif requestType == "joinGame" and additionalArgs:
        return game_server.joinGame(additionalArgs)
    return "bruh, can you just not?"


def pingsusiapi(request: django.http.HttpRequest):
    process = processThat(requestType=request.GET.get("requestType", None), roomName=request.GET.get("roomName", None), uuid=request.GET.get("uuid", None), additionalArgs=dict(request.GET))
    return django.http.HttpResponse(process)


def nopage(request, exception):
    return render(request, 'index.html')
