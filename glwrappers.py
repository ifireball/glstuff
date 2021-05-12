from contextlib import contextmanager
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders


@contextmanager
def gl_enabled_vertex_attrib_array(index: int) -> None:
    glEnableVertexAttribArray(index)
    try:
        yield
    finally:
        glDisableVertexAttribArray(index)


@contextmanager
def boundVBO(the_vbo: vbo.VBO):
    the_vbo.bind()
    try:
        yield
    finally:
        the_vbo.unbind()


@contextmanager
def shader(a_shader: shaders.ShaderProgram):
    shaders.glUseProgram(a_shader)
    try:
        yield
    finally:
        shaders.glUseProgram(0)
