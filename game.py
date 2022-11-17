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
        
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
    
    def get_z(self):
        return self.position[2]
    
    def set_x(self, x):
        pos = self.get_player_position()
        pos[0] = x
        self.set_player_position(pos)
        
    def set_y(self, y):
        pos = self.get_player_position()
        pos[1] = y
        self.set_player_position(pos)
        
    def set_z(self, z):
        pos = self.get_player_position()
        pos[2] = z
        self.set_player_position(pos)
    
    def jump_step(self, t):
        z = -GRAVITY*np.square(t)+self.strength*t
        if z >= 0:
            self.set_z(z)
        else:
            self.set_z(0)

    def get_damage(self, amount):
        self.iframes = 10
        self.healing = 200
        self.hp_bar.sprite.get_damage(amount)

    def get_heal(self, amount):
        self.hp_bar.sprite.get_heal(amount)

class Spike(Body):
    def __init__(self, mesh=None, position=..., hitbox_size=None, solid=False):
        self.hitbox_size = np.array(hitbox_size, dtype=float)
        self.solid = solid
        super().__init__(mesh, position)
        
def colliding(body, player):
    l, w, h = body.hitbox_size / 2
    body_pos = body.get_position()
    x, y, z = player.get_player_position() - body_pos

    if abs(x) < l and abs(y) < w and abs(z) < h:
        if not body.solid and not player.iframes:
            player.get_damage(20)
        elif body.solid:
            if abs(y/x) < w/l:
                player.set_x(body_pos[0] + np.sign(x)*l)
            if abs(y/x) >= w/l:
                player.set_y(body_pos[1] + np.sign(y)*w)

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
    
    vertices_2 = ((1,1,2), (1,1,-2), (1,-1,2), (1,-1,-2), (-1,1,2), (-1,1,-2), (-1,-1,2), (-1,-1,-2))
    triangles_2 = ((2,1,0),(1,2,3),(0,1,4),(5,4,1),(4,7,6),(7,4,5),(6,7,2),(3,2,7),(4,2,0),(2,4,6))
    mesh_2 = Mesh(vertices_2, triangles_2)
    
    spike = Spike(mesh_1, (20,0,0), (2,2,1), False)
    wall = Spike(mesh_2, (20,0,0), (3,3,4), True)
    
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
            new_spike = copy.copy(np.random.choice([wall,spike]))
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
        
        player.set_player_position(player.get_player_position() + displacement)    

        if abs(player.get_player_position()[0]) >= 10:
            player.set_x(10*np.sign(player.get_player_position()[0]))
        if abs(player.get_player_position()[1]) >= 4:
            player.set_y(4*np.sign(player.get_player_position()[1]))
    
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
            colliding(i, player)
            if i.get_position()[0] < -10:
                obstacles.remove(i)
            else:
                i.set_position(i.get_position() - (spikes_speed*delta_time, 0, 0))

        if player.dead():
            game_running = False

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