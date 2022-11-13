from render import Camera, Mesh, Body, Space
import render as rnr
import copy
import pygame as pg
import numpy as np
from math import pi

pg.display

CAMERA_SPEED = 10
GRAVITY = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
SCREEN_RATIO = SCREEN_WIDTH/SCREEN_HEIGHT
MOUSE_SENSITIVITY = 0.1

class Health_bar(pg.sprite.Sprite):
    def __init__(self, health):
        self.health = 100
        self.max_health = health
        self.health_bar_length = 400
        self.health_ratio = self.max_health/self.health_bar_length
        super().__init__()

    def update(self, surface):
        self.basic_health(surface)

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            self.health = 0

    def get_heal(self, amount):
        if self.health < self.max_health:
            self.health += amount
        if self.health >= self.max_health:
            self.health = self.max_health
    
    def basic_health(self, surface):
        pg.draw.rect(surface, (255,0,0),(10,10,self.health/self.health_ratio,25))
        pg.draw.rect(surface, (255,255,255),(10,10,self.health_bar_length,25),4)

class Player(Camera):
    def __init__(self, height, strength, health, position, rotation):
        self.height = height
        self.strength = strength
        self.player_position = position
        self.hp_bar = pg.sprite.GroupSingle(Health_bar(health))
        self.iframes = 0
        self.healing = 0
        cam_position = position + (0,0,self.height)
        super().__init__(cam_position, rotation)

    def dead(self):
        return not bool(self.hp_bar.sprite.health)

    def get_player_position(self):
        return self.player_position

    def set_player_position(self, position):
        self.player_position = position
        self.position = position + (0,0,self.height)

    def jump_step(self, t):
        y = -GRAVITY*np.square(t)+self.strength*t
        pos = self.player_position
        if y >= 0:
            pos[2] = y
        else:
            pos[2] = 0
        self.set_player_position(pos)

    def get_damage(self, amount):
        self.hp_bar.sprite.get_damage(amount)

    def get_heal(self, amount):
        self.hp_bar.sprite.get_heal(amount)

class Spike(Body):
    def __init__(self, mesh=None, position=..., hitbox_size=None):
        self.hitbox_size = np.array(hitbox_size, dtype=float)
        super().__init__(mesh, position)

    def colliding(self, point):
        l, w, h = self.hitbox_size / 2
        x1, y1, z1 = self.position
        x2, y2, z2 = point

        x = x2 > x1-l and x2 < x1+l
        y = y2 > y1-w and y2 < y1+w
        z = z2 > z1-h and z2 < z1+h

        if x and y and z:
            return True
        else:
            return False

def start_game():
    """ Starts pygame modules and creates a surface for the game.

    :return: Pygame surface used by the game
    :rtype: pygame.Surface
    """

    print("Starting game")
    pg.display.init()
    surface = pg.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    print("Display init:", pg.display.get_init())
    print("Display set mode:", pg.display.get_active())

    return surface

def end_game():
    """ Quits all pygame modules

    :rtype: None
    """
    print("Ending game")
    pg.display.quit()

def main():
    pg.init()
    surface = start_game()

    clock = pg.time.Clock()

    #Octahedron
    vertices_1 = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    triangles_1 = ((0,1,2), (1,3,2), (3,4,2), (4,0,2), (0,5,1), (1,5,3), (3,5,4), (4,5,0))
    mesh_1 = Mesh(vertices_1, triangles_1)

    spike = Spike(mesh_1, (20,0,0), (2,2,1))

    obstacles =[]

    main_space = Space(obstacles)

    player = Player(2, 15, 100, (0, 0, 0), (0, -pi/6))

    game_running = True
    clock.tick()

    #game loop
    direction = [0, 0, 0, 0, 0, 0]
    jumping = 0
    jump_time = 0
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    pg.mouse.get_rel()
    time_instant = 0
    spikes_speed = 10

    while game_running:
        #Events stuff
        clock.tick(30)
        delta_time = clock.get_time()/1000
        
        time_instant += delta_time

        #Spawn new spike
        if time_instant > 0.5:
            time_instant -= 0.5
            new_spike = copy.copy(spike)
            x = np.random.randint(0, 5)-2
            new_spike.set_position(new_spike.get_position() - (spikes_speed*time_instant,x*2,0))
            obstacles.append(new_spike)
        
        if pg.event.peek(eventtype=pg.QUIT, pump=True):
            game_running = False

        events = pg.event.get(pump=True)

        for e in events:
            print(e)
            if e.type == pg.KEYDOWN:
                #key w
                if e.key == 119:
                    direction[0] = 1

                #key a
                elif e.key == 97:
                    direction[1] = 1

                #key s
                elif e.key == 115:
                    direction[2] = 1

                #key d
                elif e.key == 100:
                    direction[3] = 1

                #key q
                elif e.key == 113:
                    direction[4] = 1

                #key e
                elif e.key == 101:
                    direction[5] = 1

                #key space
                elif e.key == 32 and player.get_player_position()[2] == 0:
                    jumping = 1

                #esc
                elif e.key == 27:
                    game_running = False

            elif e.type == pg.KEYUP:
                #key w
                if e.key == 119:
                    direction[0] = 0

                #key a
                elif e.key == 97:
                    direction[1] = 0

                #key s
                elif e.key == 115:
                    direction[2] = 0

                #key d
                elif e.key == 100:
                    direction[3] = 0

                #key q
                elif e.key == 113:
                    direction[4] = 0

                #key e
                elif e.key == 101:
                    direction[5] = 0

        #Camera work
        mouse_rel = pg.mouse.get_rel()
        camera_rot = np.array([-mouse_rel[0],
                               -mouse_rel[1]])*delta_time*MOUSE_SENSITIVITY
        player.set_rotation(player.get_rotation() + camera_rot)

        displacement = np.array([(direction[0] - direction[2])*player.costhe + (direction[3] - direction[1])*player.sinthe,
                                 (direction[0] - direction[2])*player.sinthe - (direction[3] - direction[1])*player.costhe,
                                 (direction[5] - direction[4])])*delta_time*CAMERA_SPEED

        if jumping:
            jump_time += delta_time
            player.jump_step(jump_time)
            if player.get_player_position()[2] == 0:
                jump_time = 0
                jumping = 0
                
        if player.iframes:
            player.iframes -= 1

        if player.healing:
            player.healing -= 1
        else:
            player.get_heal(1)

        for i in obstacles:
            if i.colliding(player.get_player_position()) and not player.iframes:
                player.iframes = 10
                player.healing = 200
                player.get_damage(20)
            if i.get_position()[0] < -10:
                obstacles.remove(i)
            else:
                i.set_position(i.get_position() - (spikes_speed*delta_time, 0, 0))

        if player.dead():
            game_running = False

        player.set_player_position(player.get_player_position() + displacement)

        #Render stuff
        player.hp_bar.update(surface)
        main_space = Space(obstacles)

        light_source = np.array((1,1,1))
        light_source = light_source/np.linalg.norm(light_source, ord=2)

        #draw_wireframes(surface, project_space(main_space, camera))
        rnr.draw_flat_shade(surface, rnr.project_space(main_space, player), light_source)

        pg.display.flip()
        surface.fill((0, 0, 0))

    end_game()

if __name__ == "__main__":
    main()