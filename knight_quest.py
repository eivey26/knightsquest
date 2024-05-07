import pgzrun
# defines the dimensions of the game grid
import random # Makes the functionality in the random module available
GRID_WIDTH = 16
GRID_HEIGHT = 12
GRID_SIZE = 50
GUARD_MOVE_INTERVAL = 0.5 # Sets the time interval for a guard to move onscreen: Can change to make game easier or harder
PLAYER_MOVE_INTERVAL = 0.1 # Time it takes for the player actor to move from one position to another
BACKGROUND_SEED = 123456 # Adds a new constant for the seed value at the top of the file

WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_HEIGHT * GRID_SIZE

MAP = [ 
        "WWWWWWWWWWWWWWWW",  # W represents a wall tile
        "W              W",
        "W              W", # Spaces represent empty squares
        "W  W  KG       W", # K is a Key, G is a guard
        "W  WWWWWWWWWW  W",
        "W              W",
        "W      P       W", # P is the Player
        "W  WWWWWWWWWW  W",
        "W      GK   W  W",
        "W              W",
        "W              D", # D is the Door
        "WWWWWWWWWWWWWWWW"
        ]

# draws the floor of the dungeon as a grid of floor tiles filling the game window.
def screen_coords(x,y): #converts a grid position to screen coordinates
    return (x * GRID_SIZE, y * GRID_SIZE)

def grid_coords(actor): # Determines which grid square the actor is in
    return (round(actor.x / GRID_SIZE) , round(actor.y / GRID_SIZE)) # Determines the position of an actor on the grid

def setup_game(): # This function will create an actor for the player and set its starting position on the map.
    global game_over,  player_won, player, keys_to_collect, guards #Defines game_over, player_won, player, guards and keys_to_collect as a global variable
    game_over = False # Sets the variable to false initially
    player_won = False # Sets the variable to False initially
    player = Actor("player", anchor=("left", "top")) #Creates a new Actor object and sets its anchor position
    keys_to_collect = [] #Sets keys to collect to an empty list initially
    guards = [] # Sets guards to an empty list initially
    for y in range(GRID_HEIGHT): #Loops over each grid position
        for x in range(GRID_WIDTH):
            square = MAP[y][x] #Extracts the character from the map representing this grid position
            if square == "P": #Checks if this grid position is the player
                player.pos = screen_coords(x, y) #Sets the position of player to the screen coordinates of this grid position
            elif square == "K": # Creates a key if the square is K
                key = Actor("key", anchor=("left", "top") , \
                            pos=screen_coords(x, y)) # Creates the key actor with an image, anchor, and position
                keys_to_collect.append(key) # Adds this actor to the list of keys created above
            elif square == "G": # Creates a guard if the square is G 
                guard = Actor("guard", anchor=("left", "top"), \
                            pos=screen_coords(x, y)) # Creates the guard actor
                guards.append(guard) # Adds this actor to the list of guards created above

def draw_background():
    random.seed(BACKGROUND_SEED) # Tells the program to pick random numbers starting from BACKGROUND_SEED
    for y in range(GRID_HEIGHT): #loops over each grid row
        for x in range(GRID_WIDTH): #loops over each grid column
            if x % 2 == y % 2: # Checks if the x and y values are either both odd or both even. Used for checkerboard background
            # screen blit draws the named image at the given screen position
                screen.blit("floor1", screen_coords(x, y)) # Draws the floor 1 tile at this position if the above condition is true
            else:
                screen.blit("floor2", screen_coords(x, y)) # Draws the floor 2 tile if either of the x and y values are odd and even
            n = random.randint(0, 99) # Picks a random number between 0 and 99
            if n < 5: # Checks if n is less than 5
                screen.blit("crack1", screen_coords(x, y)) # Draws crack1 on top of the floor tile at this position if n is less than 5
            elif n < 10: # Checks if n is less than 10
                screen.blit("crack2", screen_coords(x, y)) # Draws crack2 on top of the floor tile at this position if n is less than 10 but not less than 5


def draw_scenery():
    for y in range(GRID_HEIGHT): # this line and next line loops over each grid position
        for x in range(GRID_WIDTH):
            square = MAP[y][x] # extracts the character from the map represented by this grid position
            if square == "W": # Draws a wall tile at the screen position represented by W
                screen.blit("wall", screen_coords(x,y))
            elif square == "D": # Draws a door tile at position D
                screen.blit("door", screen_coords(x,y))

def draw_actors(): #After initializing the player, you need to draw it onscreen.
    player.draw() #Draws the player actor onscreen at its current position
    for key in keys_to_collect: # Draws all the actors in the list keys_to_collect
        key.draw()
    for guard in guards:
        guard.draw() # Draws all the actors in the list guards

def draw_game_over():
    screen_middle = (WIDTH / 2, HEIGHT / 2) # Sets the position of the GAME OVER message onscreen
    screen.draw.text("GAME OVER", midbottom=screen_middle, \
                    fontsize=GRID_SIZE, color="cyan", owidth=1) # Anchors text by its bottom edge at the middle
    if player_won:
        screen.draw.text("You won!", midtop=screen_middle, \
                        fontsize=GRID_SIZE, color="green", owidth=1) # Draws the message onscreen in green
    else:
        screen.draw.text("You lost!", midtop=screen_middle, \
                        fontsize=GRID_SIZE, color="red", owidth=1) # Draws the message onscreen in red
    screen.draw.text("Press SPACE to play again", midtop=(WIDTH / 2, \
                    HEIGHT / 2 + GRID_SIZE), fontsize=GRID_SIZE /2, \
                    color="cyan", owidth=1) # Draws the press space to play again onscreen


def draw(): # This function is called automatically from the game loop
    draw_background() # draws the dungeon floor as a background onscreen
    draw_scenery() # draws the scenery after (on top of) the background has been drawn
    draw_actors() # draws the actors after the background and scenery have been closed
    if game_over:
        draw_game_over()

def on_key_up(key): # Allows game to restart by pressing the spacebar
    if key == keys.SPACE and game_over: # Checks if the spacebar has been pressed once the game is over
        setup_game() # Calls setup_game() to reset the game

def on_key_down(key): # Reacts when the user presses down on a key
    if key == keys.LEFT:
        move_player(-1, 0) # Moves player left by one grid square
    elif key == keys.UP:
        move_player(0, -1) # Moves player up by one grid square
    elif key == keys.RIGHT:
        move_player(1, 0) # Moves player right by one grid square
    elif key == keys.DOWN:
        move_player(0, 1) # Moves player down by one grid square

def move_player(dx, dy): # function takes the distance in grid squares that a player moves on the x and y axes
    global game_over, player_won
    if game_over: # Checks if game_over is set
        return # Returns immediately without moving
    (x, y) = grid_coords(player) # Gets the current grid position of player
    x += dx # Adds the x axis distance to x
    y += dy # Adds the y axis distance to y
    square = MAP[y][x] # Gives the tile at this position
    if square == "W":
        return # Stops the execution of the move_player function if the player touches the wall
    elif square == "D":
        if len(keys_to_collect) > 0: # Checks to see if the keys to collect list is not empty
            return # Returns immediately if it is a door and if list is not empty
        else:
            game_over = True # Sets game_over to True and continues the move
            player_won = True # Sets it to True when the player wins the game
    for key in keys_to_collect: # Loops over each of the key actors in the list
        (key_x, key_y) = grid_coords(key) # Gets the grid position of a key actor
        if x == key_x and y == key_y:
            keys_to_collect.remove(key) # Removes this key from the list if player position matches key position
            break # breaks out of the for loop, as each square can only contain one key
        animate(player, pos=screen_coords(x, y), \
                duration=PLAYER_MOVE_INTERVAL) # Updates the player's position after 0.1 seconds
    player.pos = screen_coords(x, y) # Updates position of player the the new coordinates

def move_guard(guard):
    global game_over # Defines game_over as a global variable
    if game_over: #Returns immediately, without moving, if the game is over
        return
    (player_x, player_y) = grid_coords(player) # Gets the grid position of the player actor
    (guard_x, guard_y) = grid_coords(guard) # Gets the grid position of this guard actor
    if player_x > guard_x and MAP[guard_y][guard_x + 1] != "W": # Checks if the player it to the right of the guard and whether the square to the right is a wall
        guard_x += 1 # Increases the guard's x grid position by 1 if the above condition is true
    elif player_x < guard_x and MAP[guard_y][guard_x - 1] != "W": # Checks if the player is to the left of the guard
        guard_x -= 1
    elif player_y > guard_y and MAP[guard_y + 1][guard_x] != "W":
        guard_y += 1
    elif player_y < guard_y and MAP[guard_y - 1][guard_x] != "W":
        guard_y -= 1
    animate(guard, pos=screen_coords(guard_x, guard_y), \
            duration=GUARD_MOVE_INTERVAL) # Moves the actor smoothly instead of changing its position suddenly
    guard.pos = screen_coords(guard_x, guard_y) # Updates the guard actor's position to the screen coordinates of the (possibly updated) grid position
    if guard_x == player_x and guard_y == player_y: # Ends the game if the guard's grid position is the same as the player's grid position
        game_over = True
    
def move_guards():
        for guard in guards: # Loops through each guard actor in guards list
            move_guard(guard) # Moves all the guard actors in the list

setup_game()
clock.schedule_interval(move_guards, GUARD_MOVE_INTERVAL) # Schedules regular calls to the move_guards function
pgzrun.go()
