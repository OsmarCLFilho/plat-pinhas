from render import Camera, Mesh, Body, Space
import render as rnr
import copy
import pygame as pg
import numpy as np
from math import pi

CAMERA_SPEED = 10
CAMERA_DISTANCE = 15
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

class Player(Body):
    def __init__(self, height, strength, health, mesh):
        super().__init__(mesh="Lfant.png")

        self.height = height
        self.strength = strength
        self.hp_bar = pg.sprite.GroupSingle(Health_bar(health))
        self.iframes = 0
        self.healing = 0
        self.camera = Camera()

    def dead(self):
        return not bool(self.hp_bar.sprite.health)

    def jump_step(self, t):
        z = -GRAVITY*np.square(t)+self.strength*t
        if z >= 0:
            self.set_posz(z)
        else:
            self.set_posz(0)

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
        
def colliding(body, player, space):
    l, w, h = body.hitbox_size / 2
    body_pos = body.get_position()
    x, y, z = player.get_position() - body_pos

    if abs(x) < l and abs(y) < w and abs(z) < h:
        if not body.solid and not player.iframes:
            player.get_damage(20)
        elif body.solid:
            if abs(y/x) < w/l:
                for i in space.bodies:
                    if type(i) == Spike:
                        vec = body_pos - i.get_position()
                        i.set_position(i.get_position() + vec)
                        i.set_posx(-np.sign(x)*l)
                        i.set_position(i.get_position() - vec)

            if abs(y/x) >= w/l:
                for i in space.bodies:
                    if type(i) == Spike:
                        vec = body_pos - i.get_position()
                        i.set_position(i.get_position() + vec)
                        i.set_posy(-np.sign(y)*w)
                        i.set_position(i.get_position() - vec)

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
    surface = start_game()

    clock = pg.time.Clock()

    #Octahedron
    vertices_1 = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    triangles_1 = ((0,1,2), (1,3,2), (3,4,2), (4,0,2), (0,5,1), (1,5,3), (3,5,4), (4,5,0))
    mesh_1 = Mesh(vertices_1, triangles_1)
    
    vertices_2 = ((1,1,2), (1,1,-2), (1,-1,2), (1,-1,-2), (-1,1,2), (-1,1,-2), (-1,-1,2), (-1,-1,-2))
    triangles_2 = ((2,1,0),(1,2,3),(0,1,4),(5,4,1),(4,7,6),(7,4,5),(6,7,2),(3,2,7),(4,2,0),(2,4,6))
    mesh_2 = Mesh(vertices_2, triangles_2)
    
    spike = Spike(mesh_1, (5,5,0), (2,2,1), False)
    wall = Spike(mesh_2, (10,0,0), (3,3,4), True)
    
    player = Player(2, 15, 100, mesh_2)
    test_obstacles =[wall, spike, player]

    main_space = Space(test_obstacles)

    PLAYER_SPRITE = pg.Surface.convert_alpha(pg.image.load("Lfant.png"))

    game_running = True
    clock.tick()

    #game loop
    direction = [0, 0, 0, 0]
    jumping = 0
    jump_time = 0
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    pg.mouse.get_rel()

    while game_running:
        #Events stuff
        clock.tick(30)
        delta_time = clock.get_time()/1000

        if pg.event.peek(eventtype=pg.QUIT, pump=True):
            game_running = False

        events = pg.event.get(pump=True)

        for e in events:
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

                #key space
                elif e.key == 32 and player.get_position()[2] == 0:
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

        #Camera work
        mouse_rel = pg.mouse.get_rel()
        camera_rot = np.array([-mouse_rel[0],
                               -mouse_rel[1]])*delta_time*MOUSE_SENSITIVITY

        player.camera.set_rotation(player.camera.get_rotation() + camera_rot)

        displacement = np.array([(direction[0] - direction[2])*player.camera.costhe + (direction[3] - direction[1])*player.camera.sinthe,
                                 (direction[0] - direction[2])*player.camera.sinthe - (direction[3] - direction[1])*player.camera.costhe,
                                 0])*delta_time*CAMERA_SPEED        

        for i in main_space.bodies:
            if type(i) == Spike:
                i.set_position(i.get_position() - displacement)

        camera_pos = np.array([-CAMERA_DISTANCE*player.camera.cosphi*player.camera.costhe,
                               -CAMERA_DISTANCE*player.camera.cosphi*player.camera.sinthe,
                               -CAMERA_DISTANCE*player.camera.sinphi])

        player.camera.set_position(player.get_position() + camera_pos)

        if jumping:
            jump_time += delta_time
            player.jump_step(jump_time)
            if player.get_position()[2] == 0:
                jump_time = 0
                jumping = 0

        if player.iframes:
            player.iframes -= 1

        if player.healing:
            player.healing -= 1
        else:
            player.get_heal(1)

        for i in main_space.bodies:
            if type(i) == Spike:
                colliding(i, player, main_space)

        if player.dead():
            game_running = False

        #Render stuff
        light_source = np.array((1,1,1))
        light_source = light_source/np.linalg.norm(light_source, ord=2)

        #draw_wireframes(surface, project_space(main_space, camera))
        rnr.draw_flat_shade(surface, rnr.project_space(main_space, player.camera, PLAYER_SPRITE), light_source)
        player.hp_bar.update(surface)

        pg.display.flip()
        surface.fill((0, 0, 0))

    end_game()

if __name__ == "__main__":
    main()
