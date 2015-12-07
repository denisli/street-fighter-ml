import pygame
import numpy as np

class Controller(object):
    def __init__(self, character):
        self.character = character

    def make_action(self):
        raise NotImplementedError('Implement this in a subclass')

class Player1Controller(Controller):
    def __init__(self, character):
        super(Player1Controller, self).__init__(character)

    def make_action(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.character.move_left()
        if key[pygame.K_RIGHT]:
            self.character.move_right()
        if key[pygame.K_UP]:
            self.character.jump()
        if key[pygame.K_m]:
            self.character.do_punch()
        if key[pygame.K_n]:
            self.character.do_kick()
        if key[pygame.K_b]:
            self.character.fire_energy_ball()

class Player2Controller(Controller):
    def __init__(self, character):
        super(Player2Controller, self).__init__(character)

    def make_action(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.character.move_left()
        if key[pygame.K_d]:
            self.character.move_right()
        if key[pygame.K_s]:
            self.character.jump()
        if key[pygame.K_g]:
            self.character.do_punch()
        if key[pygame.K_f]:
            self.character.do_kick()
        if key[pygame.K_h]:
            self.character.fire_energy_ball()

class GoToLocationController(Controller):
    def __init__(self, character, physics, brain, location):
        super(GoToLocationController, self).__init__(character)
        '''
        For this controller, our brain is a neural network, which classifies 
        based on a given state what move to make.

        The neural network is trained during the game, and will be improved as such.

        The state is decided by:
        - the distance between character and location
        '''
        self.physics = physics
        self.brain = brain
        self.location = location

        self.decision = None # useless initialization

        # mapping from the neural net output to the actual move
        self.move_map = {0: self.character.move_left, 1: self.character.move_right, 2: lambda *args: None}
        self.first_turn = True
        self.previous_absolute_distance_away = abs(get_character_center(self.character) - location)

        # threshold for committing to a move
        self.commitment_threshold = 0.5

    def make_action(self):
        # set the inputs into the neural network
        distance = get_character_center(self.character) - self.location

        # train the brain if it is not the first turn (use previous round's results to do this)
        if self.first_turn:
            self.first_turn = False
        else:
            # we only need to train if we think we are far away
            if abs(distance) >= 3:
                # if we at same position or further, pretend the correct classification is doing everything else
                # we must include delay as being further
                if self.previous_absolute_distance_away <= abs(distance) + 5 * self.character.delay * self.character.movement_speed:
                    self.brain.backward(self.decision, -1)
                    print 'misclassified. distance:', distance
                # otherwise, our classification is considered correct
                else:
                    self.brain.backward(self.decision, 1)
                    print 'correctly classified'


        # set the absolute distance away for use in the next iterations (to tell if we got closer or not)
        self.previous_absolute_distance_away = abs(distance)
        
        # get the output from the network based on current state
        self.brain.forward([distance])
        self.decision = np.copy(self.brain.oOutput)
        print self.decision
        # make the move based on the output
        index = np.argmax(self.decision)
        self.decision[:][0] = 0
        self.decision[index][0] = 1
        self.move_map[index]()

class SoftmaxGoToLocationController(Controller):
    def __init__(self, character, physics, brain, location):
        super(SoftmaxGoToLocationController, self).__init__(character)
        '''
        For this controller, our brain is a neural network, which classifies 
        based on a given state what move to make.

        The neural network is trained during the game, and will be improved as such.

        The state is decided by:
        - the distance between character and location
        '''
        self.physics = physics
        self.brain = brain
        self.location = location

        self.decision = None # useless initialization

        # mapping from the neural net output to the actual move
        self.move_map = {0: self.character.move_left, 1: self.character.move_right, 2: lambda *args: None}
        self.first_turn = True
        self.previous_distance_away = get_character_center(self.character) - location

    def make_action(self):
        # set the inputs into the neural network
        distance = get_character_center(self.character) - self.location

        # train the brain if it is not the first turn (use previous round's results to do this)
        if not self.first_turn:
            # we only need to train if we think we are far away
            if abs(distance) >= 0:
                # any output coordinate >= 0.5 was used, so set it to 1
                # otherwise set it to 0
                # if we at same position or further, pretend the correct classification is doing everything else
                # we must include delay as being further
                if abs(self.previous_distance_away) <= abs(distance) + 5 * self.character.delay * self.character.movement_speed:
                    index = np.argmax(self.decision[0])
                    self.decision = np.array([[0 for i in range(len(self.move_map))]])
                    i = index
                    while i == index:
                        i = np.random.randint(0, len(self.move_map))
                    self.decision[0][i] = 1
                    self.brain.train(np.array([[self.previous_distance_away]]), self.decision)
                    print 'misclassified. distance:', distance
                # otherwise, our classification is considered correct
                else:
                    self.brain.train(np.array([[self.previous_distance_away]]), self.decision)
                    print 'correctly classified'


        # set the absolute distance away for use in the next iterations (to tell if we got closer or not)
        self.previous_distance_away = distance
        
        # get the output from the network based on current state
        if not self.first_turn:
            self.decision = self.brain.predict(np.array([[distance]]))
        else:
            self.decision = np.array([[0, 1, 0]])
            self.first_turn = False
        # print self.decision
        # make the move based on the output
        index = np.argmax(self.decision[0])
        print index
        self.move_map[index]()

def get_character_center(character):
    return character.bounding_box.x + character.bounding_box.width / 2

class NaiveAvoidEnergyBallsController(Controller):
    def __init__(self, character, physics, brain):
        super(NaiveAvoidEnergyBallsController, self).__init__(character)
        '''
        Our brain is a logistic regression, which decides whether or not the character
        should jump. The brain will be trained to learn how to avoid energy balls by learning
        the best time to jump.

        This brain will be trained in an environment in which there may only be at most 
        1 energy ball fired.
        '''
        self.physics = physics
        self.brain = brain
        self.training_example_in_progress = False
        self.already_jumped_for_example = False # ensure that you only jump once per example
        self.commitment_threshold = 0.5
        self.jumping_distance = 0 # some stupid initialization

    def make_action(self):
        # sense that a training example is in progress
        if len(self.physics.game_objects.energy_balls) > 0:
            if not self.training_example_in_progress: # new training example
                self.already_jumped_for_example = False
                self.training_example_in_progress = True

        # train the logistic regression
        if self.training_example_in_progress:
            if self.character.is_hurt: # get hit by energy ball (misclassified)
                self.brain.train(self.jumping_distance, False)
                self.training_example_in_progress = False
                print 'Misclassified :-('

            elif len(self.physics.game_objects.energy_balls) == 0: # managed to avoid ball (correctly classified)
                self.brain.train(self.jumping_distance, True)
                self.training_example_in_progress = False
                self.commitment_threshold = min(0.525, self.commitment_threshold * 1.01)
                print 'Yay :-)!'

        if self.training_example_in_progress:
            # make a decision if you haven't
            if not self.already_jumped_for_example:
                energy_ball = self.physics.game_objects.energy_balls[0]
                distance = min(abs(self.character.bounding_box.x - (energy_ball.bounding_box.x+energy_ball.bounding_box.width)),
                    abs(self.character.bounding_box.x + self.character.bounding_box.width - energy_ball.bounding_box.x))
                decision = self.brain.predict(distance)
                print 'probability:', decision
                if decision >= self.commitment_threshold:
                    print 'jumping distance:', distance
                    self.jumping_distance = distance
                    self.character.jump()
                    self.already_jumped_for_example = True

class EarlynessAwareAvoidEnergyBallsController(Controller):
    def __init__(self, character, physics, brain):
        super(EarlynessAwareAvoidEnergyBallsController, self).__init__(character)
        '''
        Our brain is a logistic regression, which decides whether or not the character
        should jump. The brain will be trained to learn how to avoid energy balls by learning
        the best time to jump.

        This brain will be trained in an environment in which there may only be at most 
        1 energy ball fired.
        '''
        self.physics = physics
        self.brain = brain
        self.training_example_in_progress = False
        self.already_jumped_for_example = False # ensure that you only jump once per example
        self.jumping_distance = 0 # some stupid initialization

        # variables for giving the bot a chance to learn
        self.num_times_not_jumped = 0
        self.make_learning_jump = False # used to force character to have training samples

        # variable for weighing the gains
        self.correctness_weight = 1.0

    def make_action(self):
        # sense that a training example is in progress
        if len(self.physics.game_objects.energy_balls) > 0:
            if not self.training_example_in_progress: # new training example
                self.already_jumped_for_example = False
                self.training_example_in_progress = True

        # train the logistic regression
        if self.training_example_in_progress:
            # get hit by energy ball (misclassified)
            if self.character.is_hurt:
                # the character did not even bother to jump...
                if not self.already_jumped_for_example:
                    self.num_times_not_jumped += 1
                    print 'Did not jump for this many times:', self.num_times_not_jumped
                else: # there is no need to make a learning jump if we tried to jump
                    self.make_learning_jump = False
                # if the character was early in jumping...
                if self.already_jumped_for_example and self.character.vertical_speed >= 0:
                    for i in range(10): # put more weight into misclassifications
                        self.brain.train(self.jumping_distance, [1,0,0])
                    print 'Misclassified, too early :-('
                # if the character was late in jumping
                else:
                    if self.already_jumped_for_example:
                        for i in range(10): # put more weight into misclassifications
                            self.brain.train(self.jumping_distance, [0,0,1])
                    else:
                        for i in range(10):
                            self.brain.train(0, [0,0,1])
                    print 'Misclassified, too late :-('
                self.training_example_in_progress = False
            # managed to avoid ball (correctly classified)
            elif len(self.physics.game_objects.energy_balls) == 0:
                self.brain.train(self.jumping_distance, [0,1,0], self.correctness_weight)
                self.correctness_weight = self.correctness_weight / 1.01
                self.training_example_in_progress = False
                print 'Yay :-)!'

        # if a training example is in progress you should decide on what to do
        if self.training_example_in_progress:
            # make a decision if you haven't
            if not self.already_jumped_for_example:
                energy_ball = self.physics.game_objects.energy_balls[0]
                distance = min(abs(self.character.bounding_box.x - (energy_ball.bounding_box.x+energy_ball.bounding_box.width)),
                    abs(self.character.bounding_box.x + self.character.bounding_box.width - energy_ball.bounding_box.x))
                decision = self.brain.predict(distance)
                # find the maximum index
                best_index = 2
                best_probability = decision[2]
                for i in range(2):
                    if decision[i] > best_probability:
                        best_index = i
                        best_probability = decision[i]

                # if best_index is 1 (just the right time to jump!) then jump
                if best_index == 1:
                    print 'jumping distance:', distance, ', best_index:', best_index
                    self.jumping_distance = distance
                    self.character.jump()
                    self.already_jumped_for_example = True
                    self.num_times_not_jumped = 0
                # if the character has not tried to jump for the previous energy ball, force him to want to
                elif self.num_times_not_jumped >= 1:
                    print 'will try to jump due to lack of interest in jumping :-('
                    self.make_learning_jump = True
                    self.num_times_not_jumped = 0
                # actually force the character to jump if it senses that it is best_index = 2 (too late to avoid energy ball)
                if not self.already_jumped_for_example and self.make_learning_jump and best_index == 2:
                    print 'make a learning jump'
                    print 'jumping distance:', distance, ', best_index:', best_index
                    self.jumping_distance = distance
                    self.character.jump()
                    self.already_jumped_for_example = True
                    self.num_times_not_jumped = 0

class AvoidEnergyBallTeacherController(Controller):
    '''
    Basically a controller where the character will fire energy balls whenever the enemy has is not hurt
    and there are no energy balls on the field
    '''
    def __init__(self, character, physics):
        super(AvoidEnergyBallTeacherController, self).__init__(character)
        self.physics = physics

    def make_action(self):
        energy_balls = self.physics.game_objects.energy_balls
        if len(energy_balls) == 0 and self.character.mana >= self.character.energy_ball_attack.mana_consumption and not self.physics.get_opponent(self.character).is_hurt:
            self.character.fire_energy_ball()

class BeatPunchingBagController(Controller):
    '''
    Basically a controller where the character will fire energy balls whenever the enemy has is not hurt
    and there are no energy balls on the field
    '''
    def __init__(self, character, physics, brain):
        super(BeatPunchingBagController, self).__init__(character)
        self.physics = physics
        self.brain = brain
        self.first_turn = True
        self.was_in_attack_range = False
        self.move_map = {0: self.character.move_left, 1: self.character.move_right, 2: self.character.do_kick, 3: self.character.do_punch, 4: lambda *args: None}
        self.prev_move = [] # useless initialization
        self.prev_distance = 0 # useless initialization
        self.decision = None # useless initialization

    def make_action(self):
        if self.character.delay > 0: return
        opponent = self.physics.get_opponent(self.character)
        distance_from_enemy = self.character.bounding_box.x - opponent.bounding_box.x
        attack_range = min(self.character.punch.bounding_box.width, self.character.kick.bounding_box.width)
        is_in_attack_range = abs(distance_from_enemy) - self.character.bounding_box.width < attack_range
        
        print distance_from_enemy
        # Do not train if first turn
        if self.first_turn:
            self.first_turn = False
        # Do training if not first turn
        else:
            # if enemy was in attack range
            if self.was_in_attack_range:
                # classify correctly if enemy is hurt
                if opponent.is_hurt:
                    index = np.argmax(self.decision)
                    self.decision[:] = 0
                    self.decision[index] = 1
                    self.brain.backward(self.decision, 1)
                    print "Classified: Enemy is hurt"
                # misclassify if enemy not hurt
                else:
                    index = np.argmax(self.decision)
                    self.decision[:] = 1
                    self.decision[index] = 0
                    self.brain.backward(self.decision, 1)
                    print "Misclassified: Enemy is not hurt"
            # if enemy was not in attack range
            else:
                # classify correctly if enemy in attack range
                if abs(self.prev_distance) - (self.character.delay * 5) > abs(distance_from_enemy):
                    index = np.argmax(self.decision)
                    self.decision[:] = 0
                    self.decision[index] = 1
                    self.brain.backward(self.decision, 1)
                    print "Classified: Enemy in attack range"
                # misclassify if enemy not hurt
                else:
                    index = np.argmax(self.decision)
                    self.decision[:] = 1
                    self.decision[index] = 0
                    self.brain.backward(self.decision, 1)
                    print "Misclassified: Enemy not in attack range"
        
        # get the output from the network based on current state
        self.brain.forward([distance_from_enemy])
        self.decision = np.copy(self.brain.oOutput)
        print self.decision
        # make the move based on the output

        move_index = np.argmax(self.decision)

        self.prev_distance = distance_from_enemy
        self.was_in_attack_range = is_in_attack_range
        self.move_map[move_index]()
