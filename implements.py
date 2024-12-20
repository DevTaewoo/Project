import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self, blocks: list):
        # ============================================
        # TODO: Implement an event when block collides with a ball
        self.alive = False      
        if not self.alive:
            blocks.remove(self)


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list , items: list):
        # ============================================
        # TODO: Implement an event when the ball hits a block
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.dir = 360 - self.dir + random.randint(-5, 5)

                if random.random() < 0.2:
                    item_color = random.choice([config.paddle_long_color, config.add_score_color])
                    new_item = Item(item_color, block.rect.center)
                    items.append(new_item)
                block.collide(blocks)

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        # 좌우 벽 충돌
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:
            self.dir = 180 - self.dir
        # 상단 벽 충돌
        if self.rect.top <= 0:
            self.dir = -self.dir + random.randint(-5, 5)

    def alive(self):
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        if self.rect.bottom >= config.display_dimension[1]:
            return False
        return True
    
    def set_upward_direction(self):
        self.dir = random.randint(45, 135)  # 새로운 공 발사각을 45도에서 135도 사이로 랜덤 설정
class Item(Basic):
    def __init__(self, color, pos):
        if color == config.paddle_long_color:
            self.type = "blue"
        else:
            self.type = "red"
        
        super().__init__(color, config.ball_speed, pos, config.ball_size)
        
       

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def move(self):
        
        self.rect.move_ip(0, config.ball_speed)
        self.center = (self.rect.centerx, self.rect.centery)

    def collide(self, paddle: Paddle, balls: list):
        # 패들과 충돌하면 효과 적용
        if self.rect.colliderect(paddle.rect):
            if self.type == "blue":
                pass
            elif self.type == "red":
                new_ball = Ball(pos=(paddle.rect.centerx, paddle.rect.top - config.ball_size[1]-5))  # 패들 위치에서 공 발사
                new_ball.set_upward_direction()
                balls.append(new_ball) 
               

                
            return True  
        return False
#