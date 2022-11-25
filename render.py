import pygame as pg
import numpy as np
from math import sin, cos, pi, tan

CAMERA_SPEED = 10
GRAVITY = 6.5
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
SCREEN_RATIO = SCREEN_WIDTH/SCREEN_HEIGHT
TAN_HALF_FOV = tan((pi/2)/2)
MOUSE_SENSITIVITY = 0.1

#Render package
class Camera:
    """ The reference point to where objects are projected to then be rendered on the screen

    :param position: Coordinates of the camera
    :type position: tuple with 3 float values
    :param rotation: Azimuthal and polar angle of the camera
    :type rotation: tuple with 2 float values. The first ranges from 0 to 2pi and the second from -pi/2 to pi/2
    """
    def __init__(self, position=(0, 0, 0), rotation=(0, 0)):
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
        self.sinphi = sinphi
        self.cosphi = cosphi
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
        self.sinphi = sinphi
        self.cosphi = cosphi
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

#Automaticaly creates the vertices and triangles for a rectangular mesh with the desired length, width and height.
#Then, creates such a mesh
class PlatMesh(Mesh):
    def __init__(self, length, width, height):
        vertices = []
        for x in (1, -1):
            for y in (1, -1):
                for z in (1, -1):
                    vertices.append((x*length/2,y*width/2,z*height/2))

        triangles = ((0,2,1),(1,2,3),(4,0,5),(5,0,1),(6,4,7),(7,4,5),(2,6,3),(3,6,7),(4,6,0),(0,6,2),(1,3,5),(5,3,7))

        self.setup_mesh(vertices, triangles)

#Render package
class Body:
    def __init__(self, mesh=None, position=(0, 0, 0)):
        self.mesh = mesh
        self.position = np.array(position, dtype=float)

    def set_position(self, position):
        self.position = np.array(position, dtype=float)

    def get_position(self):
        return self.position
    
    def set_posx(self, x):
        self.position[0] = x

    def set_posy(self, y):
        self.position[1] = y

    def set_posz(self, z):
        self.position[2] = z

#Render package
class Space:
    def __init__(self, bodies=[]):
        self.bodies = []
        self.bodies.extend(bodies)

    def add_bodies(self, bodies):
        self.bodies.extend(bodies)

    def remove_body(self, body):
        self.bodies.remove(body)

                

#Render package
def project_triangle(vertices, camera):

    #Vertices with coordinates in relation to the camera position
    V = vertices - camera.position

    #Vertices with coordinates in relation to the camera position AND rotation
    M = camera.transform_matrix
    V = np.matmul(M, V.T).T

    if V[0,0] < 1 or V[1,0] < 1 or V[2,0] < 1:
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
def project_space(space, camera, ps):
    player_sprite = ps
    drawable_trigs = []
    for body in sorted(space.bodies, key=lambda b: np.linalg.norm((b.position - camera.position), ord=1), reverse=True):
        mesh = body.mesh

        if mesh == None:
            pass

        #this will catch Mesh and all its subclasses
        elif isinstance(mesh, Mesh):
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

    drawable_trigs.append(player_sprite)

    return drawable_trigs

#End of package things

def draw_wireframes(surface, triangles):
    for tri in triangles:
        pg.draw.aalines(surface, (255, 255, 255), points=tri[:,:2].tolist(), closed=True)
def draw_flat_shade(surface, triangles, light_direction):
    for tri in triangles:
        if isinstance(tri, np.ndarray):
            shade = ((np.dot(tri[:,2], light_direction) + 1)*75) + 50
            if shade > 255:
                shade = 255

            pg.draw.polygon(surface, (shade, shade, shade), points=tri[:,:2].tolist())
            pg.draw.aalines(surface, (shade/4, shade/4, shade/4), points=tri[:,:2].tolist(), closed=True)

        elif isinstance(tri, pg.Surface):
            print("drawing player")
            w = tri.get_width()
            h = tri.get_height()
            surface.blit(tri, [(SCREEN_WIDTH - w)/2, (SCREEN_HEIGHT - h)/2])
