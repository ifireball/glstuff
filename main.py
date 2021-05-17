from ctypes import byref, c_uint

import pyglet
from pyglet.gl import *
import pyshaders
from pyglbuffers import Buffer


pyshaders.load_extension('pyglbuffers_bindings')


theProgram: pyshaders.ShaderProgram


def initialize_program():
    global theProgram

    vertex_shader = \
        """#version 330 core

        in vec4 position;
        in vec4 color;

        smooth out vec4 vertex_color;

        void main()
        {
           gl_Position = position;
           vertex_color = color;
        }
        """

    fragment_shader = \
        """#version 330 core

        smooth in vec4 vertex_color;

        out vec4 final_color;

        void main()
        {
            final_color = vertex_color;
        }
        """

    theProgram = pyshaders.from_string(vertex_shader, fragment_shader)
    print(theProgram)
    print(theProgram.attributes)


positionBufferObject: Buffer = None
vao: GLuint = c_uint(0)


def initialize_vertex_buffer():
    global positionBufferObject
    positionBufferObject = Buffer.array('(4f)[position] (4f)[color]', GL_STATIC_DRAW)
    positionBufferObject.init((
        ((0.0,     0.5, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0)),
        ((0.5,  -0.366, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0)),
        ((-0.5, -0.366, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0)),
    ))


def init():
    initialize_program()
    initialize_vertex_buffer()

    global vao
    glGenVertexArrays(1, byref(vao))
    glBindVertexArray(vao)


def display():
    global theProgram

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    positionBufferObject.bind()

    theProgram.use()
    try:
        theProgram.enable_all_attributes()
        theProgram.map_attributes(positionBufferObject)
        glDrawArrays(GL_TRIANGLES, 0, 3)
    finally:
        theProgram.clear()


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(resizable=True)
        init()

    def on_draw(self):
        display()


def main():
    MainWindow()
    pyglet.app.run()


if __name__ == "__main__":
    main()
