import json
from flask import Flask, Response, send_from_directory
from flask_game import Game

#one game object holds all the players, the server calls its methods
game = Game()

app = Flask(__name__)

#this builds an error response with a message and a status code,
# it's a function so the same lines don't have to be repeated in every endpoint
def error(message, status):
    response = {"message": message}
    json_response = json.dumps(response)
    http_response = Response(response=json_response, status=status, mimetype="application/json")
    return http_response


#this starts the game with the player's name from the address, loads their save or creates a new one
@app.route("/start/<player>")
def start(player):
    data = game.start(player)
    return data

#this sends back the player's current data 
@app.route("/state/<player>")
def state(player):
    if player not in game.players:
        return error("Player not found", 400)
    data = game.players[player]
    return data

#this moves the player to the location in the address, sends an error if the player or the location doesn't exist
@app.route("/move/<player>/<room>")
def move(player, room):
    if player not in game.players:
        return error("Player not found", 400)
    data = game.move(player, room)
    if data is None:
        return error("Room not found", 400)
    return data

#this tries to catch from the bush in the address.
# The bush number comes as text so it is turned into a number first, if it isn't a number an error is sent instead of the server crashing.
@app.route("/catch/<player>/<bush>")
def catch(player, bush):
    if player not in game.players:
        return error("Player not found", 400)
    try:
        bush_number = int(bush)
    except ValueError:
        return error("Invalid bush number", 400)
    data = game.catch(player, bush_number)
    if data is None:
        return error("Bush not found", 400)
    return data


#these serve the pages of the game. The start page opens with just the address,
# images come from the images folder and everything else (html, css, js) from the static folder
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("images", filename)

@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory("static", filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, use_reloader=True)