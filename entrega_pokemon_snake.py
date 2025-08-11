import os
import random
import readchar
import time

# --- General Settings ---
MAP_WIDTH = 20
MAP_HEIGHT = 15
NUM_OF_TRAINERS = 5
PLAYER_NAME = "Pikachu"
PLAYER_HP = 80

POS_X, POS_Y = 0, 1

# --- Game State ---
my_position = [1, 1]
map_trainers = []
trainers_defeated = 0
end_game = False

# --- Draw Map ---
obstacle_map = '''\
####################    
#   ##     ###     #
# ##   ###     ##  #
#    ##    ##      #
###      ####   ####
#   ####       ##  #
# ##    ## ###     #
#    ##        ### #
#  ####   ##       #
#    ##     ## ### #
###     ####     ###
#   ##       ##    #
# ##    ####    ## #
#     ##    ##     #
####################'''

obstacle_map = [list(row) for row in obstacle_map.split('\n')]

# --- trainers & pokemons ---
trainers = [
    {"name": "Squirtle", "hp": 95, "attacks": {"Pistola Agua": 15, "Placaje": 10}},
    {"name": "Charmander", "hp": 90, "attacks": {"Ascuas": 18, "Arañazo": 12}},
    {"name": "Bulbasaur", "hp": 100, "attacks": {"Latigo Cepa": 13, "Placaje": 9}},
    {"name": "Psyduck", "hp": 85, "attacks": {"Confusión": 16, "Pistola Agua": 11}},
    {"name": "Eevee", "hp": 90, "attacks": {"Placaje": 10, "Ataque Rápido": 8}},
]

random.shuffle(trainers)
available_trainers = trainers[:NUM_OF_TRAINERS]

# --- Utilities ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPresiona Enter para continuar...")

def text_effect(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# --- Combat ---
def pokemon_combat(player_name, player_hp, rival_name, rival_hp, rival_attacks):
    clear_screen()
    text_effect(f"\n¡Un entrenador salvaje aparece con un {rival_name}!")
    text_effect(f"¡{player_name}, yo te elijo!\n")

    max_player_hp = player_hp
    max_rival_hp = rival_hp

    while player_hp > 0 and rival_hp > 0:
        clear_screen()

        print(f"{player_name}:  [{'#' * int(player_hp * 20 / max_player_hp):20}] ({player_hp}/{max_player_hp})")
        print(f"{rival_name}: [{'#' * int(rival_hp * 20 / max_rival_hp):20}] ({rival_hp}/{max_rival_hp})")

        print("\nElige un ataque:")
        print("1. Bola Voltio (10–15)")
        print("2. Ataque Rápido (8–18)")

        choice = ""
        while choice not in ["1", "2"]:
            choice = readchar.readchar()

        if choice == "1":
            dmg = random.randint(10, 15)
            text_effect(f"\n{player_name} usa Bola Voltio. ¡Causa {dmg} de daño!")
        else:
            dmg = random.randint(8, 18)
            text_effect(f"\n{player_name} usa Ataque Rápido. ¡Causa {dmg} de daño!")

        rival_hp = max(rival_hp - dmg, 0)
        if rival_hp == 0:
            text_effect(f"\n¡{rival_name} ha sido derrotado!")
            return True
        pause()

        # Adversary attacks
        clear_screen()
        attack, dmg = random.choice(list(rival_attacks.items()))
        text_effect(f"\n{rival_name} usa {attack}. Causa {dmg} de daño.")
        player_hp = max(player_hp - dmg, 0)
        if player_hp == 0:
            text_effect(f"\n¡Tu {player_name} ha sido derrotado!")
            return False
        pause()

# --- Generate trainers ---
def generate_trainers():
    while len(map_trainers) < NUM_OF_TRAINERS:
        pos = [random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)]
        if (pos not in map_trainers and pos != my_position and
                obstacle_map[pos[POS_Y]][pos[POS_X]] != "#"):
            map_trainers.append(pos)

# --- Map ---
def draw_map():
    print("+" + "---" * MAP_WIDTH + "+")
    for y in range(MAP_HEIGHT):
        print("|", end="")
        for x in range(MAP_WIDTH):
            char = " "
            if [x, y] == my_position:
                char = "P"
            elif [x, y] in map_trainers:
                char = "T"
            elif obstacle_map[y][x] == "#":
                char = "#"
            print(f" {char} ", end="")
        print("|")
    print("+" + "---" * MAP_WIDTH + "+")

# --- Principal loop ---
while not end_game:
    clear_screen()
    generate_trainers()
    draw_map()
    print(f"\nEntrenadores derrotados: {trainers_defeated}/{NUM_OF_TRAINERS}")
    print("Controles: [W] Arriba | [S] Abajo | [A] Izquierda | [D] Derecha | [Q] Salir")

    move = readchar.readchar().lower()
    new_position = my_position[:]

    if move == "w":
        new_position[POS_Y] -= 1
    elif move == "s":
        new_position[POS_Y] += 1
    elif move == "a":
        new_position[POS_X] -= 1
    elif move == "d":
        new_position[POS_X] += 1
    elif move == "q":
        end_game = True
        continue

    # obstacles
    if obstacle_map[new_position[POS_Y]][new_position[POS_X]] == "#":
        continue

    my_position = new_position

    # Match with trainers
    if my_position in map_trainers:
        rival = available_trainers.pop(0)
        result = pokemon_combat(PLAYER_NAME, PLAYER_HP, rival["name"], rival["hp"], rival["attacks"])
        if result:
            map_trainers.remove(my_position)
            trainers_defeated += 1
        else:
            end_game = True
            clear_screen()
            text_effect("\n💥 Has perdido el combate. Fin del juego.")
            break

    # Winning
    if trainers_defeated == NUM_OF_TRAINERS:
        end_game = True
        clear_screen()
        text_effect("\n🎉 ¡Has derrotado a todos los entrenadores y eres el Campeón Pokémon!")
        break

pause()
