import numpy as np
import glfw
from OpenGL.GL import *

gComposedM = np.identity(3)

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    t = 10 * np.pi / 180
    if key == glfw.KEY_Q and action == glfw.PRESS:
        gComposedM[0, 2] -= 0.1
    if key == glfw.KEY_E and action == glfw.PRESS:
        gComposedM[0, 2] += 0.1
    if key == glfw.KEY_A and action == glfw.PRESS:
        T = np.array([[np.cos(t), -np.sin(t), 0.0], [np.sin(t), np.cos(t), 0.0], [0.0, 0.0, 1.0]])
        gComposedM = gComposedM @ T
    if key == glfw.KEY_D and action == glfw.PRESS:
        T = np.array([[np.cos(-t), -np.sin(-t), 0.0], [np.sin(-t), np.cos(-t), 0.0], [0.0, 0.0, 1.0]])
        gComposedM = gComposedM @ T
    if key == glfw.KEY_1 and action == glfw.PRESS:
        gComposedM = np.identity(3)
    if key == glfw.KEY_W and action == glfw.PRESS:
        T = np.identity(3)
        T[0, 0] = 0.9
        gComposedM = T @ gComposedM
    if key == glfw.KEY_S and action == glfw.PRESS:
        T = np.array([[np.cos(t), -np.sin(t), 0.0], [np.sin(t), np.cos(t), 0.0], [0.0, 0.0, 0.0]])
        gComposedM = T @ gComposedM

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "2019097656-4-1", None, None)
    
    if not window:
        glfw.terminate()
        return
        
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)
    
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render(gComposedM)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()

if __name__ == "__main__":
    main()