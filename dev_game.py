from render import Camera, Mesh, PlatMesh, Body, Space
import render as rnr
import copy
import pygame as pg
import numpy as np
from math import pi

PLAYER_SPEED = 10
CAMERA_DISTANCE = 15
GRAVITY = 40
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

    def apply_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            self.health = 0

    def apply_heal(self, amount):
        if self.health < self.max_health:
            self.health += amount
        if self.health >= self.max_health:
            self.health = self.max_health
    
    def basic_health(self, surface):
        pg.draw.rect(surface, (255,0,0),(10,10,self.health/self.health_ratio,25))
        pg.draw.rect(surface, (255,255,255),(10,10,self.health_bar_length,25),4)

class Player(Body):
    def __init__(self, size, strength, health, mesh=None):
        #super().__init__(mesh=mesh)
        super().__init__(mesh="Lfant.png")

        self.size = size
        self.strength = strength
        self.hp_bar = pg.sprite.GroupSingle(Health_bar(health))
        self.iframes = 0
        self.healing = 0
        self.camera = Camera()
        self.vertical_speed = 0
        self.able_to_jump = True

    def dead(self):
        return not bool(self.hp_bar.sprite.health)

    def gravity_step(self, t):
        self.vertical_speed = self.vertical_speed - GRAVITY*t
        self.set_posz(self.get_position()[2] + t*(self.vertical_speed))

    def jump(self):
        if self.able_to_jump:
            self.vertical_speed = self.strength
            self.able_to_jump = False

    def apply_damage(self, amount):
        self.iframes = 10
        self.healing = 200
        self.hp_bar.sprite.apply_damage(amount)

    def apply_heal(self, amount):
        self.hp_bar.sprite.apply_heal(amount)

class Obstacle(Body):
    def __init__(self, mesh=None, position=(0, 0, 0), hitbox_size=None, solid=False, timer=10):
        self.timer = timer
        self.hitbox_size = np.array(hitbox_size, dtype=float)
        self.solid = solid
        super().__init__(mesh, position)
        
def colliding(body, player, space):
    l, w, h = (body.hitbox_size + player.size)/2
    body_pos = body.get_position()
    x, y, z = player.get_position() - body_pos

    if abs(x) < l and abs(y) < w and abs(z) < h:

        if not body.solid and not player.iframes:
            player.apply_damage(20)

        elif body.solid:
            if l - abs(x) < w - abs(y):
                if l - abs(x) < h - abs(z):
                    for b in space.bodies:
                        if type(b) == Obstacle:
                            b.set_posx(b.get_position()[0] - np.sign(x)*(l-abs(x)))

                else:
                    player.set_posz(player.get_position()[2] + np.sign(z)*(h-abs(z)))
                    player.able_to_jump = True
                    player.vertical_speed = 0

            elif l - abs(x) < h - abs(z) or w - abs(y) < h - abs(z):
                for b in space.bodies:
                    if type(b) == Obstacle:
                        b.set_posy(b.get_position()[1] - np.sign(y)*(w-abs(y)))

            else:
                player.set_posz(player.get_position()[2] + np.sign(z)*(h-abs(z)))
                if np.sign(z) == 1:
                    player.able_to_jump = True
                player.vertical_speed = 0

            #if abs(y/x) < w/l:
                #for i in space.bodies:
                    #if type(i) == Obstacle:
                        #vec = body_pos - i.get_position()
                        #i.set_position(i.get_position() + vec)
                        #i.set_posx(-np.sign(x)*l)
                        #i.set_position(i.get_position() - vec)

            #if abs(y/x) >= w/l:
                #for i in space.bodies:
                    #if type(i) == Obstacle:
                        #vec = body_pos - i.get_position()
                        #i.set_position(i.get_position() + vec)
                        #i.set_posy(-np.sign(y)*w)
                        #i.set_position(i.get_position() - vec)

def rotation(theta):
    return np.array([[np.cos(theta),np.sin(theta),0],[-np.sin(theta),np.cos(theta),0],[0,0,1]])

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
    pg.mixer.init()
    pg.mixer.music.load('song.mp3')
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play()
    surface = start_game()

    clock = pg.time.Clock()
    plat_vec = (0,20,0)

    #Obstacle
    vertices_1 = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    triangles_1 = ((0,1,2), (1,3,2), (3,4,2), (4,0,2), (0,5,1), (1,5,3), (3,5,4), (4,5,0))
    mesh_1 = Mesh(vertices_1, triangles_1)
    
    mesh_plat = PlatMesh(5, 5, 4)
    
    platform1 = Obstacle(mesh_plat, (0, 0, -5), (5, 5, 4), True)
    
    player = Player(2, 15, 100)
    bodies = [player, platform1]

    main_space = Space(bodies, 1)

    PLAYER_SPRITE = pg.image.load("Lfant.png")
    PLAYER_SPRITE = pg.transform.scale(PLAYER_SPRITE, np.array(PLAYER_SPRITE.get_rect()[2:])/1.6)

    game_running = True
    clock.tick()

    #game loop
    direction = [0, 0, 0, 0]
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
                elif e.key == 32:
                    player.jump()

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

        #Platform timer stuff
        for platform in reversed(main_space.bodies):
            if isinstance(platform, Obstacle):
                platform.timer -= delta_time

                if platform.timer < 0:
                    main_space.remove_body(platform)

        if main_space.countdown_platform(delta_time):
            angle = np.radians(np.random.uniform(0,90)-45)

            if np.random.rand() > 0.9:
                sign = np.random.choice([1,-1])
                plat_vec = rotation(np.radians(sign*90)) @ plat_vec
                angle = np.radians(-sign*45)

            old_pos = main_space.bodies[-1].get_position()
            new_pos = old_pos + rotation(angle) @ plat_vec

            main_space.add_bodies((Obstacle(mesh_plat, new_pos, (5, 5, 4), True, 3),))

        #Camera work
        mouse_rel = pg.mouse.get_rel()
        camera_rot = np.array([-mouse_rel[0],
                               -mouse_rel[1]])*delta_time*MOUSE_SENSITIVITY

        player.camera.set_rotation(player.camera.get_rotation() + camera_rot)

        displacement = np.array([(direction[0] - direction[2])*player.camera.costhe + (direction[3] - direction[1])*player.camera.sinthe,
                                 (direction[0] - direction[2])*player.camera.sinthe - (direction[3] - direction[1])*player.camera.costhe,
                                 0])*delta_time*PLAYER_SPEED

        displacement_norm = np.linalg.norm(displacement, ord=2)
        if displacement_norm == 0:
            displacement_norm = 1

        for i in main_space.bodies:
            if type(i) == Obstacle:
                i.set_position(i.get_position() - displacement/displacement_norm)

        camera_pos = np.array([-CAMERA_DISTANCE*player.camera.cosphi*player.camera.costhe,
                               -CAMERA_DISTANCE*player.camera.cosphi*player.camera.sinthe,
                               -CAMERA_DISTANCE*player.camera.sinphi])

        player.camera.set_position(player.get_position() + camera_pos)

        #Camera stuff done

        #if jumping:
            #jump_time += delta_time
            #player.gravity_step(jump_time)
            #if player.get_position()[2] == 0:
                #jump_time = 0
                #jumping = 0

        player.gravity_step(delta_time)

        if player.iframes:
            player.iframes -= 1

        if player.healing:
            player.healing -= 1
        else:
            player.apply_heal(1)

        player.able_to_jump = False
        for i in main_space.bodies:
            if type(i) == Obstacle:
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
