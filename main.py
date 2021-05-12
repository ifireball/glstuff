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


def vertex_shader() -> GLuint:
    return shaders.compileShader(
        """#version 330
        layout(location = 0) in vec4 position;
        void main()
        {
           gl_Position = position;
        }""",
        GL_VERTEX_SHADER
    )


def fragment_shader() -> GLuint:
    return shaders.compileShader(
        """#version 330
        out vec4 outputColor;
        void main()
        {
           outputColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
        }""",
        GL_FRAGMENT_SHADER
    )


theProgram: shaders.ShaderProgram = None


def initialize_program():
    global theProgram
    theProgram = shaders.compileProgram(vertex_shader(), fragment_shader())


positionBufferObject: vbo.VBO = None
vao: GLuint


def initialize_vertex_buffer():
    global positionBufferObject
    positionBufferObject = vbo.VBO(
        array([
            0.75, 0.75, 0.0, 1.0,
            0.75, -0.75, 0.0, 1.0,
            -0.75, -0.75, 0.0, 1.0,
        ], 'f'),
        usage=GL_STATIC_DRAW
    )


def init():
    initialize_program()
    initialize_vertex_buffer()

    global vao
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

def display():
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    shaders.glUseProgram(theProgram)
    try:
        positionBufferObject.bind()
        try:
            glEnableVertexAttribArray(0)
            try:
                glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)

                glDrawArrays(GL_TRIANGLES, 0, 3)
            finally:
                glDisableVertexAttribArray(0)
        finally:
            positionBufferObject.unbind()

    finally:
        shaders.glUseProgram(0)


def screen_init():
    pg.init()
    # Initialize a new version of OpenGL that can do shaders
    # https://github.com/pygame/pygame/issues/1124
    # (It seems to not really be needed as it works on my T440s without this, and I needed to play with the version
    # numbers a bit to make it work because the version from the URL above did not work for me)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 1)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

    display_size = (1600, 800)
    pg.display.set_mode(display_size, pg.DOUBLEBUF | pg.OPENGL)


def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        display()

        pg.display.flip()
        pg.time.wait(10)


def main():
    screen_init()
    init()
    main_loop()


if __name__ == "__main__":
    main()
