import sys, pygame
import neural_network as nn
#import softmax_neural_network as smnn
import single_dimension_logistic_regression as lr
import tri_class_single_dimension_logistic_regression as tclr
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
    
    energy_ball_image = pygame.image.load('energy_ball.png')
    # initialize the players
    # player 1
    blocky = SimpleRenderingWrapper(Blocky(10, 300), 
        pygame.image.load('blocky.png'),
        pygame.image.load('blocky-punch.png'),
        pygame.image.load('blocky-kick.png'),
        pygame.image.load('blocky-hurt.png'))
    player1 = blocky

    # player 2
    noob = SimpleRenderingWrapper(Blocky(450, 300),
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
    
    # AI controller to avoid energy balls
    # controller2 = EarlynessAwareAvoidEnergyBallsController(player2, 
    #     physics, tclr.TriClassSingleDimensionLogisticRegression())

    # AI controller to walk to a certain location
    controller2 = GoToLocationController(player2, 
        physics, nn.NeuralNetwork(1, 50, 3), 100)
  
    # Softmax AI controller to walk to a certain location
    # controller2 = SoftmaxGoToLocationController(player2, 
    #     physics, smnn.SoftmaxNeuralNetwork(), 200)

    # AI controller to punch a "punching bag"
    # controller2 = BeatPunchingBagController(player2, 
    #     physics, nn.NeuralNetwork(1, 10, 5))
    
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

        # update the animation of the characters
        player1.update_animation(time)
        player2.update_animation(time)

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

        # render energy balls
        for energy_ball in game_objects.energy_balls:
            renderable_energy_ball = EnergyBallRenderingWrapper(energy_ball, energy_ball_image)
            renderable_energy_ball.render(screen)

        # render the timer
        countdown_label.update_value(str(physics.countdown / 1000))
        countdown_label.render(screen)

        pygame.display.flip()

def autotrain_main():
    pygame.init()

    player1 = InfiniteManaBlocky(10, 300)
    player2 = Blocky(450, 300)

    # create game objects container
    game_objects = GameObjects(player1, player2)

    # establish physics
    physics = SimplePhysics(game_objects, -0.003)

    # AI controllers
    controller1 = AvoidEnergyBallTeacherController(player1, physics)
    controller2 = EarlynessAwareAvoidEnergyBallsController(player2, 
        physics, tclr.TriClassSingleDimensionLogisticRegression())

    milliseconds_per_frame = 10
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

        # update time in the game
        physics.update(milliseconds_per_frame)

if __name__ == '__main__':
    main()