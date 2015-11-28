import sys, pygame
import neural_network as nn
from shapes import *
from controllers import *
from character import *
from character_rendering import *
from template_characters import *
from physics import *
from bars import *
from gui_components import *

def main():
    pygame.init()
    size = (width, height) = (720, 480)
    color = 255, 255, 255 # this is just white
    screen = pygame.display.set_mode(size)
    
    # initialize the players
    # player 1
    blocky = SimpleRenderingWrapper(Blocky(10, 300), 
        pygame.image.load('blocky.png'),
        pygame.image.load('blocky-punch.png'),
        pygame.image.load('blocky-kick.png'),
        pygame.image.load('blocky-hurt.png'))
    player1 = blocky

    # player 2
    noob = SimpleRenderingWrapper(Blocky(10, 300),
        pygame.image.load('blocky.png'),
        pygame.image.load('blocky-punch.png'),
        pygame.image.load('blocky-kick.png'),
        pygame.image.load('blocky-hurt.png'))
    player2 = noob

    # create game objects container
    game_objects = GameObjects(player1, player2)

    # establish physics
    physics = SimplePhysics(game_objects, -0.003)

    # health bars
    health_bar1 = HealthBar(50, 50, 100)
    health_bar2 = HealthBar(400, 50, 100)

    # player 1 controller
    controller1 = Player1Controller(player1)

    # player 2 controller
    #controller2 = Player2Controller(player2)
    
    # AI controller
    num_moves = 6 # left, right, jump, punch, kick, and do nothing
    target_location = 600
    controller2 = GoToLocationController(player2, physics, nn.NeuralNetwork(1, 10, num_moves), target_location)

    countdown_label = Label(300, 50, str(physics.countdown / 1000))

    clock = pygame.time.Clock()
    # handle game loop
    clock.tick() # start the clock
    while 1:
        # handle user input
        events = pygame.event.get()
        controller1.make_action()
        controller2.make_action()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        # update the clock
        time = clock.tick(60)

        # update time in the game
        physics.update(time)

        # update displays
        health_bar1.update_value(player1.health)
        health_bar2.update_value(player2.health)

        # render background
        screen.fill(color)

        # render characters
        player1.render(screen)
        player2.render(screen)
        health_bar1.render(screen)
        health_bar2.render(screen)

        # render the timer
        countdown_label.update_value(str(physics.countdown / 1000))
        countdown_label.render(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()