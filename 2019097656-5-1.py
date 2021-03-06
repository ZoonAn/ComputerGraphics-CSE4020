import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    myOrtho(-5,5, -5,5, -8,8)
    myLookAt(np.array([5,3,5]), np.array([1,1,-1]), np.array([0,1,0]))
    # Above two lines must behaves exactly same as the below two lines
    #glOrtho(-5,5, -5,5, -8,8)
    #gluLookAt(5,3,5, 1,1,-1, 0,1,0)
    drawFrame()
    glColor3ub(255, 255, 255)
    drawCubeArray()


def myLookAt(eye, at, up):
    forwardVec = eye - at
    norm_forwardVec = forwardVec / np.sqrt(np.dot(forwardVec, forwardVec))
    
    sideVec = np.cross(up, norm_forwardVec)
    norm_sideVec = sideVec / np.sqrt(np.dot(sideVec, sideVec))
    
    upVec = np.cross(norm_forwardVec, norm_sideVec)
    
    pos = np.array([np.dot(-eye, norm_sideVec), np.dot(-eye, upVec), np.dot(-eye, norm_forwardVec)])
    
    viewMatrix = np.identity(4)
    for i in range (0,3):
        viewMatrix[i] = [norm_sideVec[i], upVec[i], norm_forwardVec[i], 0.0]
    viewMatrix[3] = [pos[0], pos[1], pos[2], 1.0]
    
    glMultMatrixf(viewMatrix)
    
def myOrtho(left, right, bottom, top, zNear, zFar):
    orthoMatrix = np.identity(4)
    orthoMatrix[0][0] = 2 /(right - left)
    orthoMatrix[0][3] = - (right + left) / ( right - left)
    orthoMatrix[1][1] = 2 / (top - bottom)
    orthoMatrix[1][3] = - (top + bottom) / (top - bottom)
    orthoMatrix[2][2] = - 2 / (zFar - zNear)
    orthoMatrix[2][3] = - (zFar + zNear) / (zFar - zNear)
    glMultMatrixf(orthoMatrix)

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "2019097656-5-1", None, None)
    
    if not window:
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)
        
    glfw.terminate()

if __name__ == "__main__":
    main()