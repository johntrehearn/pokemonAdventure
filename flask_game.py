import json
import os
import random
 
#these are the locations the player can visit, the names match the map page
rooms = ["Pallet Town", "Viridian Forest", "Altering Cave"]


#these are the pokemon that can hide in the bushes and how easy they are to catch (0-255, higher is easier) 
pokemon_scores = {
    "Pikachu": 35,
    "Eevee": 20,
    "Mewtwo": 13,
    "Eternatus": 56,
    "Lickitung": 76,
    "Snorlax": 34
}

#this is the folder of this file, so the save files are always found next to it no matter where the server is started from 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
#this class holds the game logic, the server only calls these methods 
class Game:

    #the players are kept in a dictionary, the player's name is the key and their game data is the value
    def __init__(self):
        self.players = {}
    
    #this saves the player's data to their own save file, it is called after every action so no progress is lost
    def save(self, name):
        lower_name = name.lower()
        file_name = f"save_{lower_name}.json"
        file_path = os.path.join(BASE_DIR, file_name)
        with open(file_path, "w") as file:
            json.dump(self.players[name], file)

    #this starts the game for the player. If a save file with their name exists the game is loaded from it,
    #if not a new player is created in the first location and saved straight away.    
    def start(self, name):
        lower_name = name.lower()
        file_name = f"save_{lower_name}.json"
        file_path = os.path.join(BASE_DIR, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.players[name] = json.load(file)
        else:
            bushes = self.make_bushes()
            self.players[name] = {
                "name": name,
                "location": rooms[0],
                "pokemon_list": [],
                "bushes": bushes
            }
            self.save(name)
        return self.players[name]

    #this makes the 3 bushes of a location. Every bush starts empty (None),
    #then 1 or 2 pokemon are put in random empty bushes so the player never knows which ones hide something. 
    def make_bushes(self):
        bushes = [None, None, None]

        #collects the pokemon names from the dictionary into a list so one can be picked by its index
        names = []
        for pokemon in pokemon_scores:
            names.append(pokemon)
 
        pokemon_count = random.randint(1, 2)
        placed = 0

        #the loop keeps going until the rolled number of pokemon are placed, a bush that already has a pokemon is skipped
        while placed < pokemon_count:
            position = random.randint(0, 2)
            if bushes[position] is None:
                last = len(names) - 1
                index = random.randint(0, last)
                bushes[position] = names[index]
                placed = placed + 1
 
        return bushes

    #this moves the player to another location and makes new bushes for it.
    #if the location doesn't exist it returns None so the server can send an error instead. 
    def move(self, name, room):
        if room not in rooms:
            return None
        player = self.players[name]
        player["location"] = room
        player["bushes"] = self.make_bushes()
        self.save(name)
        return player

    #this is the catch mechanic, the player picks a bush (0, 1 or 2) by clicking it.
    #a bush number outside of that returns None so the server can send an error instead. 
    def catch(self, name, bush):
        player = self.players[name]
        if bush < 0 or bush > 2:
            return None

        #takes what is in the chosen bush and empties it, so the same bush can't be tried again
        bushes = player["bushes"]
        pokemon = bushes[bush]
        bushes[bush] = None
 
        caught_list = player["pokemon_list"]

        #the bush can be empty, hide a pokemon the player already has, or a new one.
        #a new pokemon is caught if the random roll is the same or lower than its score, so easy pokemon are caught more often.
        #if the roll is higher the pokemon escapes. 
        if pokemon is None:
            result = "empty"
        elif pokemon in caught_list:
            result = "already caught"
        else:
            score = pokemon_scores[pokemon]
            roll = random.randint(1, 255)
            if roll <= score:
                caught_list.append(pokemon)
                result = "caught"
            else:
                result = "escaped"
 
        self.save(name)

        #the player wins when they have caught 6 pokemon
        caught_count = len(caught_list)
        won = caught_count >= 6
        
        #this is what is sent back to the page: what happened, which pokemon it was, if the player won and their updated data
        answer = {
            "result": result,
            "pokemon": pokemon,
            "won": won,
            "player": player
        }
        return answer
 