from os import write
import struct
from obj import Obj
from collections import namedtuple

V2 = namedtuple('Point2D', ['x', 'y'])
V3 = namedtuple('Point3D', ['x', 'y', 'z'])

def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    return xs[0], xs[-1], ys[0], ys[-1]

#escribir en bytes
def char(c):
    return struct.pack('=c',c.encode('ascii'))

#escribir en bytes
def word(w):
    #short
    return struct.pack('=h',w)

#escribir en bytes
def dword(w):
    #long
    return struct.pack('=l',w)

def color(r,g,b):
    return bytes([b,g,r])

def cross(v0, v1):
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):    
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    
    if cz == 0:
        return -1, -1, -1
    
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)
    
    return w, v, u

def sub(v0, v1):
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
        v0.z - v1.z
    )

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2) ** 0.5

def norm(v0):
    l = length(v0)
    
    if l == 0:
        return V3(0, 0, 0)
    
    return V3(
        v0.x / l,
        v0.y / l,
        v0.z / l
    )

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def glClearColor(r,g,b):
    return bytes([b,g,r])

BLACK = color(0,0,0)
WHITE = color(255,255,255)
clear_color = glClearColor(12, 50, 229)

def glInit(width, height):
    glCreateWindow(width, height)
    
def glCreateWindow(width, height):
    global framebuffer, zbuffer
    framebuffer = [
            [BLACK for x in range(width)]
            for y in range(height)
        ]
    
    zbuffer = [
            [-999999 for x in range(width)]
            for y in range(height)
        ]    

def glViewport(xV, yV, widthV, heightV):
    global viewPortX, viewPortY, viewWidth, viewHeight
    viewPortX = xV
    viewPortY = yV
    viewWidth = widthV
    viewHeight = heightV
    
def glVertex(x_v, y_v, color=None):
    framebuffer[y_v][x_v]=color or current_color

def glLine(x0, y0, x1, y1):
    #x0 = int((x0 + 1) * (viewWidth / 2) + viewPortX)
    #y0 = int((y0 + 1) * (viewWidth / 2) + viewPortX)
    #x1 = int((x1 + 1) * (viewWidth / 2) + viewPortX)
    #y1 = int((y1 + 1) * (viewWidth / 2) + viewPortX)
    
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    steep = dy > dx

    if steep:      
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    offset = 0 * 2 * dx
    threshold = 0.5
    y = y0

    # y = mx + b
    points = []
    for x in range(x0, x1+1):
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))

        offset += 2 * dy
        if offset >= threshold:
            y += 1 if y0 < y1 else -1
            threshold += 1 * 2 * dx
        
    for point in points:        
        glVertex(*point)

def glLineT(A, B):
    '''
    x0 = round(((A.x + 1) * (viewWidth / 2) + viewPortX)/100)
    y0 = round(((A.y + 1) * (viewHeight / 2) + viewPortY)/100)
    x1 = round(((B.x + 1) * (viewWidth / 2) + viewPortX)/100)
    y1 = round(((B.y + 1) * (viewHeight / 2) + viewPortY)/100)
    '''
    x0 = A.x
    y0 = A.y
    x1 = B.x
    y1 = B.y    
    
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    steep = dy > dx

    if steep:      
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    offset = 0 * 2 * dx
    threshold = 0.5
    y = y0

    # y = mx + b
    points = []
    for x in range(x0, x1+1):
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))

        offset += 2 * dy
        if offset >= threshold:
            y += 1 if y0 < y1 else -1
            threshold += 1 * 2 * dx
        
    for point in points:        
        glVertex(*point)

def glFinish(filename, width, height):
    with open(filename, "bw") as f:
    #file header 14 bytes
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3 *(width * height)))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #info header 40 bytes
        f.write(dword(40))
        f.write(dword(width))
        f.write(dword(height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword( 3 *(width * height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        #bitmap
        for y in range(height):
            for x in range(width):
                f.write(framebuffer[y][x])

def Transform(v, translate, scale):
    return V3(
        round((v[0] + translate[0]) * scale[0]),
        round((v[1] + translate[1]) * scale[1]),
        round((v[2] + translate[2]) * scale[2])
    )

def load(filename, translate, scale):
    model = Obj(filename)
    
    light = V3(0, 0, 0.8)
    
    for face in model.faces:
        vcount = len(face)
        
        if vcount == 3:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            
            A = Transform(model.vertices[f1], translate, scale)
            B = Transform(model.vertices[f2], translate, scale)
            C = Transform(model.vertices[f3], translate, scale)
            
            normal = norm(cross(
                sub(B, A),
                sub(C, A)
            ))
            
            intensity =  dot(normal, light)
            # 1 si esta en frente
            # 0 si esta de lado
                            
            grey = round(255 * intensity)
            
            if intensity < 0:
                continue
                            
            triangle(A, B, C,
                color(
                    grey,
                    grey,
                    grey
                )
            )
        
        elif vcount == 4:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1 
            f4 = face[3][0] - 1
            
            A = Transform(model.vertices[f1], translate, scale)
            B = Transform(model.vertices[f2], translate, scale)
            C = Transform(model.vertices[f3], translate, scale)
            D = Transform(model.vertices[f4], translate, scale)
            
            normal = norm(cross(
                sub(A, B),
                sub(B, C)
            ))
            
            intensity =  dot(normal, light)
            # 1 si esta en frente
            # 0 si esta de lado
                            
            grey = round(255 * intensity)
            
            if intensity < 0:
                continue
            
            c1 = 0
            c2 = 0
            c3 = 0
            
            if f1 < 600 and f2 < 300:
                c1 = 1
                c2 = 0.4
                c3 = 0.2
            else:
                c1 = 0.2
                c2 = 0.4
                c3 = 0.1
                            
            triangle(A, B, C,
                color(
                    round(grey*c1),
                    round(grey*c2),
                    round(grey*c3)
                )
            )
            
            triangle(A, C, D,
                color(
                    round(grey*c1),
                    round(grey*c2),
                    round(grey*c3)
                )
            )
            
def triangle_wireframe(A, B, C):
    glLine(A, B)
    glLine(B, C)
    glLine(C, A)
        
def triangle(A, B, C, color=None):
    
    xmin, xmax, ymin, ymax = bbox(A, B, C)
    
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            P = V2(x, y)
            w, v, u = barycentric(A, B, C, P)
            if w < 0 or v < 0 or u < 0:
                continue
            
            z = A.z * w + B.z * v + C.z * u
            
            if z > zbuffer[x][y]:
                glVertex(x, y, color)
                zbuffer[x][y] = z
