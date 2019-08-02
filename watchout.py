import math
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import  SimpleControllerState
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3 as vector3, Rotator

from objects import *
from states import *
from routines import *

class watchout(BaseAgent):
    def initialize_agent(self):
        self.c = SimpleControllerState()
        self.me = carObject(self.index)
        self.ball = ballObject()
        
        field_info = self.get_field_info()

        self.all_boosts = []
        self.small_boosts = []
        self.large_boosts = []
        for i in range(field_info.num_boosts):
            boost = field_info.boost_pads[i]
            temp = boostObject(i,boost.location)
            self.all_boosts.append(temp)
            if boost.is_full_boost:
                self.large_boosts.append(temp)
            else:
                self.small_boosts.append(temp)
 
        self.friends = []
        self.foes = []
        self.friend_goal = Vector3(0,5150*side(self.team),10)
        self.foe_goal = Vector3(0,5150*-side(self.team),10)
        
        self.states = [atba()]
        self.time = 0.0
        self.setup = True
        self.kickoff = False
        self.made_kickoff_routine = False

    def test(self):
        car = CarState(boost_amount=100, physics=Physics(velocity=vector3(0,0,0),angular_velocity=vector3(0,0,0),location=vector3(3000,3000,20),rotation=Rotator(0,1.5,0)))
        ball = BallState(physics=Physics(location=vector3(0,-side(self.team)*3000,94),angular_velocity=vector3(0,0,0), velocity=vector3(0,0,3000)))
        game = GameState(ball=ball, cars = {self.index: car})
        self.set_game_state(game)
        self.state = vector_shot_test()

    def overwatch(self):
        if self.kickoff == True and self.made_kickoff_routine == False:
            self.states.append(kickoff())
            self.made_kickoff_routine = True
        elif self.kickoff == False and self.made_kickoff_routine == True:
            self.made_kickoff_routine = False
        
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.preprocess(packet)
        self.c.__init__()
        self.overwatch()
        self.states[-1].execute(self)
        return self.c

    def preprocess(self,packet):
        self.time = packet.game_info.seconds_elapsed
        
        self.ball.update(packet.game_ball)
        self.me.update(packet.game_cars)

        for friend in self.friends: friend.update(packet.game_cars)
        for foe in self.foes: foe.update(packet.game_cars)
        for pad in self.all_boosts: pad.update(packet.game_boosts)

        self.kickoff = packet.game_info.is_round_active and packet.game_info.is_kickoff_pause

        if self.setup:
            for i in range(packet.num_cars):
                if i != self.index:
                    if packet.game_cars[i].team == self.team:
                        self.friends.append(carObject(i,packet.game_cars))
                    else:
                        self.foes.append(carObject(i,packet.game_cars))
            self.setup = False
