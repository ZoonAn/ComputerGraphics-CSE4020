import numpy as np
import glfw
from OpenGL.GL import *

glPrimitiveType = ["GL_POLYGON", "GL_POINTS", "GL_LINES", "GL_LINE_STRIP", "GL_LINE_LOOP", "GL_TRIANGLES", "GL_TRIANGLE_STRIP", "GL_TRIANGLE_FAN", "GL_QUADS", "GL_QUAD_STRIP"]
pt = 4

def render():
    x = np.linspace(0, np.pi * 2 - (np.pi /6), 12)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(eval(glPrimitiveType[pt]))
    for i in x:
        glVertex2f(np.cos(i), np.sin(i))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global pt
    if key == glfw.KEY_0 and action == glfw.PRESS:
        print("0")
        pt = 0
    elif key == glfw.KEY_1 and action == glfw.PRESS:
        print("1")
        pt = 1
    elif key == glfw.KEY_2 and action == glfw.PRESS:
        print("2")
        pt = 2
    elif key == glfw.KEY_3 and action == glfw.PRESS:
        print("3")
        pt = 3
    elif key == glfw.KEY_4 and action == glfw.PRESS:
        print("4")
        pt = 4
    elif key == glfw.KEY_5 and action == glfw.PRESS:
        print("5")
        pt = 5
    elif key == glfw.KEY_6 and action == glfw.PRESS:
        print("6")
        pt = 6
    elif key == glfw.KEY_7 and action == glfw.PRESS:
        print("7")
        pt = 7
    elif key == glfw.KEY_8 and action == glfw.PRESS:
        print("8")
        pt = 8
    elif key == glfw.KEY_9 and action == glfw.PRESS:
        print("9")
        pt = 9

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "2019097656-3-1", None, None)
    
    if not window:
        glfw.terminate()
        return
        
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
if __name__ == "__main__":
    main()