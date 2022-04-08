import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import time


class Car(pygame.sprite.Sprite):
       #all the car variables
       def __init__(self, x, y, angle=0.0, length=0.5, max_steering=45, max_acceleration=50.0):
              super(Car, self).__init__()
              # position and motion  
              self.position = Vector2(x, y)
              self.velocity = Vector2(0.0, 0.0)
              self.angle = angle
              self.length = length
              self.max_acceleration = max_acceleration #degrees
              self.max_steering = max_steering

              self.max_velocity = 7
              self.brake_deceleration = 500
              self.free_deceleration = 500
              self.acceleration = 0.0
              self.steering = 0.0

              #sprite
              """current_dir = os.path.dirname(os.path.abspath(__file__))
              image_path = os.path.join(current_dir, "car2.png")
              self.image = pygame.transform.rotozoom(pygame.image.load(image_path), 0, 1)"""
              
              weight, height = 70, 40
              self.image = pygame.Surface((weight, height), pygame.SRCALPHA)
              pygame.draw.rect(self.image, (255,0,0), (0,0, weight,height))
              self.rect = self.image.get_rect()
              self.mask = pygame.mask.from_surface(self.image)
              

       #update Car state
       def update(self, dt):
              #user input
              pressed = pygame.key.get_pressed()
              
              #get forwards and backwards movement
              if pressed[pygame.K_UP]:
                     if self.velocity.x < 0:
                            self.acceleration = self.brake_deceleration
                     else:
                            self.acceleration += self.max_acceleration*dt
              elif pressed[pygame.K_DOWN]:
                     if self.velocity.x > 0:
                            self.acceleration = -self.brake_deceleration
                     else:
                            self.acceleration -= self.max_acceleration*dt 
              #avoiding car vibration
              else:
                     if abs(self.velocity.x) > dt*self.free_deceleration:
                            self.acceleration = -copysign(self.free_deceleration,self.velocity.x)
                     else:
                            if dt != 0:
                                   self.acceleration = -self.velocity.x / dt
              #max acceleration control
              self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

              #get right and left movement
              if pressed[pygame.K_RIGHT]: 
                     if self.steering > 0: #reset the wheel before changing direction to avoid delay
                            self.steering = 0
                     self.steering -= self.max_steering * dt
              elif pressed[pygame.K_LEFT]:
                     if self.steering < 0:
                            self.steering = 0
                     self.steering += self.max_steering * dt
              else:
                     self.steering = 0
              #max steering control
              self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

              #calculate velocity variation
              self.velocity += (self.acceleration*dt,0)
              self.velocity.x = max(-self.max_velocity, min(self.velocity.x,self.max_velocity))

              #calculate steering
              if self.steering:
                     turning_radius = self.length/sin(radians(self.steering))
                     angular_velocity = self.velocity.x/turning_radius
              else:
                     angular_velocity = 0
              #calculate position variaton and orientate it
              self.position += self.velocity.rotate(-self.angle)*dt
              self.angle += degrees(angular_velocity)*dt

              #sprite state
              self.rotated = pygame.transform.rotate(self.image,self.angle)
              self.rect = self.rotated.get_rect()



class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
       super(Wall, self).__init__()
       self.x = x
       self.y = y
       self.w = w
       self.h = h
       self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
       pygame.draw.rect(self.image, (0,255,0), (0,0, self.w, self.h))
       self.rect = self.image.get_rect()
       self.mask = pygame.mask.from_surface(self.image)


class Game:
       def __init__(self):
              pygame.init()
              pygame.font.init()
              pygame.display.set_caption("car")
              size = 1600, 900
              self.screen = pygame.display.set_mode(size)
              self.exit = False

              self.clock = pygame.time.Clock()
              self.ticks = 50
       

       def run(self):

              t0 = time.time()

              init_x,init_y = 7,5
              car = Car(init_x,init_y) 
              walls= pygame.sprite.Group( Wall(800, 200, 10, 110), Wall(700, 200, 100, 10),
                                          Wall(700, 300, 100, 10) )
              ppu = 50 #pixels per unit

              while not self.exit:

                     dt = self.clock.get_time()/1000

                     for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                   self.exit = True

                     #update car state 
                     car.update(dt)

                     #drawing backgrownd
                     self.screen.fill((100,100,100))
                     #drawing the car
                     self.screen.blit(car.rotated, car.position*ppu - (car.rect.width/2, car.rect.height/2))

                     #drawing the walls
                     #for wall in walls:
                     #       self.screen.blit(wall.image, (wall.x, wall.y))



                     #drawing the car collider in new position
                     """car_collider = pygame.Rect(10,10, 70, 40)
                     car_collider.x = car.position.x * ppu - car_collider.width / 2
                     car_collider.y = car.position.y * ppu - car_collider.height / 2
                     pygame.draw.rect(self.screen,(0, 255, 0),  car_collider, 3)"""
                     #collision logic
                     """if car_collider.right >= 1600 or car_collider.left <= 0:
                            car.position = init_x,init_y
                            car.velocity.x, car.angle = 0, 0
                            car.angle = 0
                            t0 = t1 
                     elif car_collider.bottom >= 900 or car_collider.top <= 0:
                            car.position = init_x,init_y
                            car.velocity.x, car.angle = 0, 0
                            t0 = t1"""
                     




                     #display timer
                     t1 = time.time()
                     clock_time = t1-t0
                     font = pygame.font.Font(pygame.font.get_default_font(), 36)
                     timer = font.render(str(clock_time)[0:4], True, (255, 255, 255))
                     self.screen.blit(timer,(1470, 10))

                     pygame.display.flip()

                     self.clock.tick(self.ticks) #mesure fps

              pygame.quit()

if __name__ == '__main__':
       Game().run()