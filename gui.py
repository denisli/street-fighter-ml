import sys, pygame
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
    
    # initialize game fighting
    blocky = SimpleRenderingWrapper(Blocky(10, 300), 
        pygame.image.load('blocky.png'),
        pygame.image.load('blocky-punch.png'),
        pygame.image.load('blocky-kick.png'),
        pygame.image.load('blocky-hurt.png'))
    player1 = blocky
    noob = SimpleRenderingWrapper(Blocky(400, 300),
        pygame.image.load('blocky.png'),
        pygame.image.load('blocky-punch.png'),
        pygame.image.load('blocky-kick.png'),
        pygame.image.load('blocky-hurt.png'))
    player2 = noob
    game_objects = GameObjects(player1, player2)
    health_bar1 = HealthBar(50, 50, 100)
    health_bar2 = HealthBar(400, 50, 100)
    controller1 = Player1Controller(player1)
    controller2 = Player2Controller(player2)
    physics = SimplePhysics(game_objects, -0.0001)
    countdown_label = Label(300, 50, str(physics.countdown / 1000))

    # handle game loop
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

        # apply character interaction
        physics.update(30)

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

        # stop consuming the processor
        pygame.time.delay(3)


if __name__ == '__main__':
    main()