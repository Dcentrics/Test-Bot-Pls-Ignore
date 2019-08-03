from objects import *
from util import *
import os
import math

class gui:
    def __init__(self,agent,enabled):
        self.enabled = enabled
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.average = 3.0
        self.resolution = [220*3,140*3]
        self.field_center = [self.resolution[0]//2,self.resolution[1]//2]
        if self.enabled:
            global pygame
            import pygame
            pygame.init()
            self.window = pygame.display.set_mode(self.resolution,pygame.RESIZABLE)
            path = os.path.dirname(os.path.realpath(__file__))
            self.sheet = pygame.image.load(path+"/SpriteSheet.png").convert_alpha()
            self.small_boost = self.get_sprite((0,0,4,4))
            self.large_boost = self.get_sprite((4,0,8,8))
            self.large_blue = self.get_sprite((12,0,7,11))
            self.medium_blue = self.get_sprite((19,0,5,9))
            self.large_orange = self.get_sprite((27,0,7,11))
            self.medium_orange = self.get_sprite((34,0,5,9))
            self.large_ball = self.get_sprite((42,0,5,5))
            self.small_ball = self.get_sprite((47,0,5,5))
            self.small_boost_empty = self.get_sprite((51,0,4,4))
            self.large_boost_empty = self.get_sprite((55,0,8,8))
            self.field = self.get_sprite((0,12,217,140))
            pygame.display.set_icon(pygame.transform.scale(self.large_boost,(32,32)))
            pygame.display.set_caption("Gosling V6.0")
            
    def get_sprite(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size,pygame.SRCALPHA)
        image.blit(self.sheet,(0,0),rect)
        return image

    def resize(self,event):
        average = sum([cap(event.dict['size'][0],217,2170)/self.resolution[0],cap(event.dict['size'][1],135,1350)/self.resolution[1]])/ 2
        self.resolution = [int(self.resolution[0]*average),int(self.resolution[1]*average)]
        self.average = self.resolution[0] / 217
        self.field_center = [self.resolution[0]//2,self.resolution[1]//2]
        self.window = pygame.display.set_mode(self.resolution, pygame.RESIZABLE)

    def render(self,surface,location,center=False):
        size = surface.get_rect()
        if center:
            location = (location[0]-(size[2]*self.average//2),location[1]-(size[3]*self.average//2))
        surface = pygame.transform.scale(surface,(int(size[2]*self.average),int(size[3]*self.average)))
        self.window.blit(surface,location,surface.get_rect())
        
    def render_car(self,car):
        rotation = -math.degrees(math.atan2(car.matrix[0][1],car.matrix[0][0]))+180
        if car.team == 1:
            surface = pygame.transform.rotate(self.medium_orange,rotation)
        else:
            surface = pygame.transform.rotate(self.medium_blue,rotation)
        self.render(surface,self.convert(car.location),True)
        
        
    def render_field(self,agent):
        self.render(self.field,self.field_center,True)
        for boost in agent.large_boosts:
            if boost.active:
                self.render(self.large_boost,self.convert(boost.location),True)
            else:
                self.render(self.large_boost_empty,self.convert(boost.location),True)
        for boost in agent.small_boosts:
            if boost.active:
                self.render(self.small_boost,self.convert(boost.location),True)
            else:
                self.render(self.small_boost_empty,self.convert(boost.location),True)
        
        for friend in agent.friends:
            self.render_car(friend)
        for foe in agent.foes:
            self.render_car(foe)
        self.render_car(agent.me)
        self.render(self.large_ball,self.convert(agent.ball.location),True)
            

    def convert(self,point):
        point = (point * (1/64)) * self.average
        point = [int(-point[1]+self.field_center[0]+1),int(point[0]+self.field_center[1]-5)]
        return point
        
    def update(self,agent):
        if self.enabled:
            shutdown = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.enabled = False
                    shutdown = True
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event)
            if shutdown:
                pygame.quit()
            else:
                self.window.fill(self.white)
                self.render_field(agent)
                '''
                self.render(self.field,(0,0))
                self.render(self.small_boost,(10,100))
                self.render(self.large_boost,(50,100))
                self.render(self.large_blue,(100,100))
                self.render(self.large_orange,(150,100))
                self.render(self.medium_blue,(200,100))
                self.render(self.medium_orange,(250,100))
                self.render(self.large_ball,(300,100))
                self.render(self.small_ball,(350,100))
                '''
                pygame.display.flip()
                #pygame.display.update()
                
                
            
        
        
            
            
            
        
