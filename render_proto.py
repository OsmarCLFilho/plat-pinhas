import pygame as pg
import numpy as np
from math import sin, cos, pi, sqrt, tan

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
SCREEN_RATIO = SCREEN_WIDTH/SCREEN_HEIGHT
TAN_HALF_FOV = tan((pi/2)/2)
CAMERA_SPEED = 5
MOUSE_SENSITIVITY = 0.1

#Render package
class Camera:
    """ The reference point to where objects are projected to then be rendered on the screen

    :param position: Coordinates of the camera
    :type position: tuple with 3 float values
    :param rotation: Azimuthal and polar angle of the camera
    :type rotation: tuple with 2 float values. The first ranges from 0 to 2pi and the second from -pi/2 to pi/2
    """
    def __init__(self, position, rotation):
        self.position = np.array(position, dtype=float)
        self.rotation = np.array(rotation, dtype=float)
        self.rotation[0] = self.rotation[0]%(2*pi)

        if self.rotation[1] > pi/3:
            self.rotation[1] = pi/3

        elif self.rotation[1] < -pi/3:
            self.rotation[1] = -pi/3

        theta, phi = self.rotation[0], self.rotation[1]

        sinphi = sin(phi)
        cosphi = cos(phi)
        sinthe = sin(theta)
        costhe = cos(theta)

        self.sinthe = sinthe
        self.costhe = costhe
        self.transform_matrix = np.array([[costhe*cosphi, sinthe*cosphi, sinphi],
                                          [-sinthe, costhe, 0],
                                          [-costhe*sinphi, -sinthe*sinphi, cosphi]])

    def set_rotation(self, rotation):
        self.rotation = np.array(rotation, dtype=float)
        self.rotation[0] = self.rotation[0]%(2*pi)

        if self.rotation[1] > pi/3:
            self.rotation[1] = pi/3

        elif self.rotation[1] < -pi/3:
            self.rotation[1] = -pi/3

        theta, phi = self.rotation[0], self.rotation[1]

        sinphi = sin(phi)
        cosphi = cos(phi)
        sinthe = sin(theta)
        costhe = cos(theta)

        self.sinthe = sinthe
        self.costhe = costhe
        self.transform_matrix = np.array([[costhe*cosphi, sinthe*cosphi, sinphi],
                                          [-sinthe, costhe, 0],
                                          [-costhe*sinphi, -sinthe*sinphi, cosphi]])

    def set_position(self, position):
        self.position = np.array(position, dtype=float)

    def get_rotation(self):
        return self.rotation

    def get_position(self):
        return self.position

#Render package
class Mesh:
    def __init__(self, vertices, triangles):
        self.setup_mesh(vertices, triangles)

    def setup_mesh(self, vertices, triangles):
        #Vertices -> each row is a set of coordinates for a vertex
        self.vertices = np.array(vertices, dtype=float)
        #Triangles -> each row is a set of indices for selecting the triangle's vertices
        self.triangles = np.array(triangles, dtype=int)

        self.normals = []

        for tri in self.triangles:
            v1 = self.vertices[tri[1]] - self.vertices[tri[0]]
            v2 = self.vertices[tri[2]] - self.vertices[tri[1]]
            perp = np.cross(v1,v2)

            self.normals.append(perp/np.linalg.norm(perp, ord=2))

        self.normals = np.array(self.normals)

class PlatMesh(Mesh):
    def __init__(self, length, width, height):
        #Calculo dos vértices a partir das dimensões

#Render package
class Body:
    def __init__(self, mesh=None, position=(0, 0, 0)):
        self.mesh = mesh
        self.position = np.array(position, dtype=float)

#Render package
class Space:
    def __init__(self, bodies=[]):
        self.bodies = []
        self.bodies.extend(bodies)

    def add_bodies(self, bodies):
        self.bodies.extend(bodies)

#Render package
def project_triangle(vertices, camera):

    #Vertices with coordinates in relation to the camera position
    V = vertices - camera.position

    #Vertices with coordinates in relation to the camera position AND rotation
    M = camera.transform_matrix
    V = np.matmul(M, V.T).T

    if V[0,0] < 0 or V[1,0] < 0 or V[2,0] < 0:
        return None

    #Scaled vectors such that the first component is 1
    V[0] = V[0]/V[0,0]
    V[1] = V[1]/V[1,0]
    V[2] = V[2]/V[2,0]

    if ((V[0,1] > TAN_HALF_FOV and V[1,1] > TAN_HALF_FOV and V[2,1] > TAN_HALF_FOV) or
        (V[0,1] < -TAN_HALF_FOV and V[1,1] < -TAN_HALF_FOV and V[2,1] < -TAN_HALF_FOV) or
        (V[0,2] < -TAN_HALF_FOV/SCREEN_RATIO and V[1,2] < -TAN_HALF_FOV/SCREEN_RATIO and V[2,2] < -TAN_HALF_FOV/SCREEN_RATIO) or
        (V[0,2] > TAN_HALF_FOV/SCREEN_RATIO and V[1,2] > TAN_HALF_FOV/SCREEN_RATIO and V[2,2] > TAN_HALF_FOV/SCREEN_RATIO)):

        return None


    return V[:,1:]

#Render package
def project_space(space, camera):
    drawable_trigs = []
    for body in sorted(space.bodies, key=lambda b: np.linalg.norm((b.position - camera.position), ord=1), reverse=True):
        mesh = body.mesh

        if mesh == None:
            pass

        else:
            for index, trig in enumerate(mesh.triangles):
                trig_vertices = np.array([mesh.vertices[trig[0]],
                                          mesh.vertices[trig[1]],
                                          mesh.vertices[trig[2]]], dtype=float) + body.position

                if np.dot(mesh.normals[index], trig_vertices[0] - camera.position) > 0:
                    continue

                projection = project_triangle(trig_vertices, camera)

                if isinstance(projection, np.ndarray):
                    projection = projection*(-1)
                    projection[:,0] = (projection[:,0] + TAN_HALF_FOV)*(SCREEN_WIDTH/2*TAN_HALF_FOV)
                    projection[:,1] = (projection[:,1] + TAN_HALF_FOV/SCREEN_RATIO)*(SCREEN_HEIGHT*SCREEN_RATIO/2*TAN_HALF_FOV)

                    #Bad life choices right here, change this later, add a triangle class or whatever
                    drawable_trigs.append(np.column_stack((projection, mesh.normals[index])))

    return np.array(drawable_trigs)

#End of package things

def draw_wireframes(surface, triangles):
    for tri in triangles:
        pg.draw.aalines(surface, (255, 255, 255), points=tri[:,:2].tolist(), closed=True)

def draw_flat_shade(surface, triangles, light_direction):
    for tri in triangles:
        shade = ((np.dot(tri[:,2], light_direction) + 1)*75) + 50
        if shade > 255:
            shade = 255

        pg.draw.polygon(surface, (shade, shade, shade), points=tri[:,:2].tolist())
        pg.draw.aalines(surface, (shade/4, shade/4, shade/4), points=tri[:,:2].tolist(), closed=True)

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

    body_1 = Body(mesh_1, (8,0,0))
    body_2 = Body(mesh_1, (4,8,0))
    body_3 = Body(mesh_1, (0,0,0))
    body_4 = Body(mesh_1, (-8,0,0))
    body_5 = Body(mesh_1, (3,0,0))

    main_space = Space((body_1, body_2, body_3, body_4, body_5))

    camera = Camera((0, 0, 2), (0, -pi/6))

    game_running = True
    clock.tick()

    #game loop
    direction = [0, 0, 0, 0, 0, 0]
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
        camera.set_rotation(camera.get_rotation() + camera_rot)

        displacement = np.array([(direction[0] - direction[2])*camera.costhe + (direction[3] - direction[1])*camera.sinthe,
                                 (direction[0] - direction[2])*camera.sinthe - (direction[3] - direction[1])*camera.costhe,
                                 (direction[5] - direction[4])])*delta_time*CAMERA_SPEED

        camera.set_position(camera.get_position() + displacement)

        #Render stuff
        surface.fill((0, 0, 0))

        light_source = np.array((1,1,1))
        light_source = light_source/np.linalg.norm(light_source, ord=2)

        #draw_wireframes(surface, project_space(main_space, camera))
        draw_flat_shade(surface, project_space(main_space, camera), light_source)

        pg.display.flip()

    end_game()

if __name__ == "__main__":
    main()
