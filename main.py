"""
An implementation of the OpenglContext tutorials without OpenglContext
http://pyopengl.sourceforge.net/context/tutorials/index.html
"""
from functools import lru_cache
import pygame as pg
from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import array
from OpenGL.GL import shaders


@lru_cache(1)
def vertex_shader():
    return shaders.compileShader(
        """#version 120
        void main() {
            // This is not really working because OpenGLContext did not set the projection matrix up for us 
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }""",
        GL_VERTEX_SHADER
    )


@lru_cache(1)
def fragment_shader():
    return shaders.compileShader(
        """#version 120
        void main() {
            gl_FragColor = vec4( 0, 1, 0, 1 );
        }""",
        GL_FRAGMENT_SHADER
    )


@lru_cache(1)
def shader():
    return shaders.compileProgram(vertex_shader(), fragment_shader())


@lru_cache()
def buildVbo():
    return vbo.VBO(
        array([
            [0, 1, 0],
            [-1, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [4, -1, 0],
            [4, 1, 0],
            [2, -1, 0],
            [4, 1, 0],
            [2, 1, 0],
        ], 'f')
    )


def render():
    shaders.glUseProgram(shader())
    vbo = buildVbo()
    try:
        vbo.bind()
        try:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointerf(vbo)
            glDrawArrays(GL_TRIANGLES, 0, 9)
        finally:
            vbo.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)

    finally:
        shaders.glUseProgram(0)


def screen_init():
    pg.init()
    # Initialize a new version of OpenGL that can do shaders
    # https://github.com/pygame/pygame/issues/1124
    # (It seems to not really be needed as it works on my T440s without this, and I needed to play with the version
    # numbers a bit to make it work because the version from the URL above did not work for me)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 0)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

    display = (1600, 800)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)


def main_lopp():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        render()

        pg.display.flip()
        pg.time.wait(10)


def main():
    screen_init()
    main_lopp()


if __name__ == "__main__":
    main()
