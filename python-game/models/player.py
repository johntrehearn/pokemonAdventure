import random

class Player:
    def __init__(self, name, location):
        self.name=name
        self.items = []
        # a new player starts with no pokemon
        self.pokemon_list = []
        self.location = location
    def move(self, room):
        self.location = room
        print(f"You have moved to {room.name}")
    def collect_item(self):
        #if current room has an item, add it to player's items
        if self.location.item is not None:
            self.items.append(self.location.item)
            print(f"{self.location.item.name} has been added to your list.")
            #the room is now empty
            self.location.item = None
        else:
            print("There is nothing in the room.")
    def show_inventory(self):
        if len(self.items) == 0:
           print("Your items list is empty.")
        else: 
           for item in self.items:
                print(f"{item.name} {item.effect}")

    #show user's caught pokemon
    def show_pokemon_list(self):
        if len(self.pokemon_list) == 0:
            print("Your pokemon list is empty.")
        else:
            for pokemon in self.pokemon_list:
                print(pokemon)

    def generate_pokemon_bushes(self, all_pokemon, selection):
        bushes = []
        pokecount = random.randint(1, 2) #randomly gen the amount of bushes with pokemon in them
        for i in pokecount:
            bushes.append(random.choice(all_pokemon))
        if i in bushes.count - 3: # should make it so if there is only one bush with pokemon, then two empty bushes are generated, and vise versa
            bushes.append(None)
        random.shuffle(bushes) # shuffle the bushes like the cup game so the empty ones will be random
        match (selection):
            case 1: return bushes.index(1)
            case 2: return bushes.index(2)
            case 3: return bushes.index(3)

    # gather user input of what bush they picked between 1-3 by clicking
    def catch_pokemon(self, all_pokemon, selection): # i think this function moreso reprisents "pick bush" maybe we rename?

        pokemonToCatch = self.generate_pokemon_bushes(selection) # get pokemon from bush (might be None intentionally to say the bush was empty)

        # consider adding catch chance ran against api for odds and the particular ball used
        # e.g. poke ball = 50% catch chance, rare pokemon = 50% catch chance so 50%*50% = 25% catch chance
        # then run a random number, if it rolls above 25% then its caught
        # only add the pokemon if the player does not have it yet
        if pokemonToCatch in self.pokemon_list:
            print(f"A wild {pokemonToCatch} pokemon has appeared, but you already have it.")
        else:
            print(f"A wild {pokemonToCatch} pokemon has appeared and you caught it!")
            self.pokemon_list.append(pokemonToCatch)