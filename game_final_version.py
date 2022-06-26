#!/usr/bin/env python3
# Summary!
# Installing Python and Pygame
# Python language basics (variables, collections, control flow, functions, classes)
# Developing our game while learning about Pygame

# Gain access to the pygame library
import pygame
from pygame.locals import *

# Size of the screen
SCREEN_TITLE = 'PokeAdventure! (dont sue me plz)'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
# Colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.RESIZABLE)


class Game:

    # Typical rate of 60, equivalent to FPS
    TICK_RATE = 70

    # Initializer for the game class to set up the width, height, and title
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.game_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        # Set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        # Load and set the background image for the scene
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
                                            
    def run_game_loop(self, level_speed):
        def changeImage(image_path):
            object_image = pygame.image.load(image_path)
            player_character.image = pygame.transform.scale(object_image, (50, 50))
        is_game_over = False
        did_win = False
        direction = 0
        sides = 0
        

        player_character = PlayerCharacter('main.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('ghastly.png', 20, 300, 50, 50)
        # Speed increased as we advance in difficulty
        enemy_0.SPEED *= level_speed

        # Create another enemy
        enemy_1 = NonPlayerCharacter('ghastly.png', self.width - 60, 500, 65, 65)
        enemy_1.SPEED *= level_speed
        # Create another enemy
        enemy_2 = NonPlayerCharacter('ghastly.png', 20, 200, 75, 75)
        enemy_2.SPEED *= level_speed

        treasure = GameObject('treasure.png', 375, 50, 50, 50)
        enemies = [enemy_0, enemy_1, enemy_2]

        #Variables and images
        
        walking = False
        counter = 0
        counterNew = 1
        facing = []
        up_ = ['up1.png','up2.png']
        down_ = ['down1.png','down2.png']
        left_ = ['left1.png','left2.png']
        right_ = ['right1.png','right2.png']

        # Main game loop, used to update all gameplay such as movement, checks, and graphics
        # Runs until is_game_over = True
            
        while not is_game_over:
            if walking == True:
                if counterNew < 1:
                    counter = (counter + 1) % len(facing)
                    changeImage(facing[counter])
                elif counterNew > 500000000000:
                    counterNew == 0 
                else:
                    counterNew += 1
            # A loop to get all of the events occuring at any given time
            # Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                # If we have a quite type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 0.5
                        facing = up_
                    # Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -0.5
                        facing = down_
                    elif event.key == pygame.K_LEFT:
                        sides = -0.5
                        facing = left_
                    elif event.key == pygame.K_RIGHT:
                        sides = 0.5
                        facing = right_
                    walking = True
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP:
                        changeImage('main.png')
                        direction = 0
                    elif event.key == pygame.K_DOWN:
                        changeImage('down_stop.png')
                        direction = 0
                    elif event.key == pygame.K_LEFT:
                        changeImage('left_stop.png')
                        sides = 0
                    elif event.key == pygame.K_RIGHT:
                        changeImage('right_stop.png')
                        sides = 0
                    walking = False
                    counterNew = 0
                    print(event)
                
                
            

            # Redraw the screen to be a blank white window
            self.game_screen.fill(WHITE_COLOR)
            # Draw the image onto the background
            self.game_screen.blit(self.image, (0, 0))

            # Draw the treasure
            treasure.draw(self.game_screen)
            
            # Update the player position
            player_character.move(direction, sides, self.height)
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            # Move and draw the enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            # Move and draw more enemies when we reach higher levels of difficulty
            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            # End game if collision between enemy and treasure
            # Close game if we lose
            # Restart game loop if we win
            for enemy in enemies:
                if player_character.detect_collision(enemy):
                    is_game_over = False
                    did_win = False
                    text = font.render(' oh   :( ', True, BLACK_COLOR)
                    player_character.x_pos = 375
                    player_character.y_pos = 700
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)

                if player_character.detect_collision(treasure):
                    is_game_over = True
                    did_win = True
                    text = font.render('WINNER', True, BLACK_COLOR)
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)

            # Update all game graphics
            pygame.time.delay(10)
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        # Restart game loop if we won
        # Break out of game loop and quit if we lose
        if did_win:
            self.run_game_loop(level_speed + 0.25)
        else:
            return

# Generic game object class to be subclassed by other objects in the game
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        # Scale the image up
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y


        self.width = width
        self.height = height

    # Draw the object by blitting it onto the background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))



# Class to represent the character contolled by the player
class PlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

        self.x_pos = x
        self.y_pos = y
    

    # Move function will move character up if direction > 0 and down if < 0
    def move(self, direction, sides, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        elif sides > 0:
            self.x_pos += self.SPEED
        elif sides < 0:
            self.x_pos -= self.SPEED
            
        # Make sure the character never goes past the bottom of the screen
        if self.y_pos >= max_height - self.height:
            self.y_pos = max_height - self.height

    # Return False (no collision) if y positions and x positions do not overlap
    # Return True x and y positions overlap
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True

# Class to represent the enemies moving left to right and right to left
class NonPlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)


    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
            #b = pygame.image.load('ghastly.png')
            #enemy_0.image = pygame.transform.scale(b,(50, 50))
        elif self.x_pos >= max_width - (20 + self.width):
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
            
pygame.init()

new_game = Game('gamy.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(2)

# Quit pygame and the program
pygame.quit()
quit()


# Load the player image from the file directory
# player_image = pygame.image.load('player.png')
# Scale the image up
# player_image = pygame.transform.scale(player_image, (50, 50))

# Draw a rectangle on top of the game screen canvas (x, y, width, height)
            # pygame.draw.rect(game_screen, BLACK_COLOR, [350, 350, 100, 100])
            # Draw a circle on top of the game screen (x, y, radius)
            # pygame.draw.circle(game_screen, BLACK_COLOR, (400, 300), 50)

            # Draw the player image on top of the screen at (x, y) position
            # game_screen.blit(player_image, (375, 375))
