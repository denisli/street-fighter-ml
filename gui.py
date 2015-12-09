import sys, pygame
import neural_network as nn
#import softmax_neural_network as smnn
import single_dimension_logistic_regression as lr
import tri_class_single_dimension_logistic_regression as tclr
import qlearning as ql
from shapes import *
from controllers import *
from character import *
from character_rendering import *
from template_characters import *
from physics import *
from bars import *
from gui_components import *
import pickle

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
    mana_bar1 = ManaBar(50, 100, 100)
    mana_bar2 = ManaBar(400, 100, 100)

    # player 1 controller
    # controller1 = AvoidEnergyBallTeacherController(player1, physics)
    controller1 = Player1Controller(player1)

    # player 2 controller
    # controller2 = Player2Controller(player2)
    
    # AI controller to avoid energy balls
    # controller2 = EarlynessAwareAvoidEnergyBallsController(player2, 
    #    physics, tclr.TriClassSingleDimensionLogisticRegression())

    # controller2 = NaiveAvoidEnergyBallsController(player2, 
    #    physics, lr.SingleDimensionLogisticRegression())

    controller2 = NeuralNetworkAvoidEnergyBallsController(player2, 
       physics, nn.NeuralNetwork(1, 50, 2))

    # AI controller to walk to a certain location
    # controller2 = TwoMoveNaiveGoToLocationController(player2, 
    #     physics, nn.NeuralNetwork(1, 50, 3), 200)

    # AI controller to walk to a certain location
    # controller2 = AllMovesGoToLocationController(player2, 
    #     physics, nn.NeuralNetwork(1, 50, 7), 200)
  
    # Two Move Softmax AI controller to walk to a certain location
    # controller2 = TwoMoveSoftmaxGoToLocationController(player2, 
    #     physics, smnn.SoftmaxNeuralNetwork(), 200)

    # All Moves Softmax AI controller to walk to a certain location
    # controller2 = AllMovesSoftmaxGoToLocationController(player2, 
    #     physics, smnn.SoftmaxNeuralNetwork(), 200)

    # AI controller to punch a "punching bag"
    # controller2 = BeatPunchingBagController(player2, 
    #     physics, nn.NeuralNetwork(1, 10, 5))

    # AI controller with smarter fighting abilities against a passive opponent
    brain = pickle.load(open('save.p', 'r'))
    #brain = nn.NeuralNetwork(2, 10, 5)
    controller2 = SmarterBeatPunchingBagController(player2,
        physics, brain)
    controller2.stop_training()
    
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
        mana_bar1.update_value(player1.mana)
        mana_bar2.update_value(player2.mana)

        # render background
        screen.fill(color)

        # render characters
        player1.render(screen)
        player2.render(screen)
        health_bar1.render(screen)
        health_bar2.render(screen)
        mana_bar1.render(screen)
        mana_bar2.render(screen)

        # render energy balls
        for energy_ball in game_objects.energy_balls:
            renderable_energy_ball = EnergyBallRenderingWrapper(energy_ball, energy_ball_image)
            renderable_energy_ball.render(screen)

        # render the timer
        countdown_label.update_value(str(physics.countdown / 1000))
        countdown_label.render(screen)
        # if controller2.classification_count > 10:
        #     print physics.countdown
        #     break

        key = pygame.key.get_pressed()
        if key[pygame.K_p]:
            pickle.dump(brain, open("save.p", "wb"))

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
    controller2 = AllMovesSoftmaxGoToLocationController(player2, 
        physics, smnn.SoftmaxNeuralNetwork(), 200)
    # controller2 = TwoMoveSoftmaxGoToLocationController(player2, 
    #     physics, smnn.SoftmaxNeuralNetwork(), 200)
    # controller2 = AllMovesNaiveGoToLocationController(player2, 
    #     physics, nn.NeuralNetwork(1, 50, 7), 200)
    # controller2 = TwoMoveNaiveGoToLocationController(player2, 
    #     physics, nn.NeuralNetwork(1, 50, 3), 200)
    # controller2 = EarlynessAwareAvoidEnergyBallsController(player2, 
    #    physics, tclr.TriClassSingleDimensionLogisticRegression())
    # controller2 = NaiveAvoidEnergyBallsController(player2, 
    #    physics, lr.SingleDimensionLogisticRegression())

    milliseconds_per_frame = 17
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
        if controller2.count < 0:
            break
    
    return physics.countdown

if __name__ == '__main__':
    # average = 0
    # for i in range(1):
    #     average += autotrain_main()
    #     print average/1
    main()
