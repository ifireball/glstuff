"""
An implementation of the OpenglContext tutorials without OpenglContext
http://pyopengl.sourceforge.net/context/tutorials/index.html
"""
from OpenGLContext import testingcontext

from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGLContext.arrays import array
from OpenGL.GL import shaders


BaseContext = testingcontext.getInteractive("pygame")


class TestContext(BaseContext):
    """Create a simple vertex shader"""

    def OnInit(self):
        vertex_shader = shaders.compileShader(
            """#version 120
            void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            }""",
            GL_VERTEX_SHADER
        )
        fragment_shader = shaders.compileShader(
            """#version 120
            void main() {
                gl_FragColor = vec4( 0, 1, 0, 1 );
            }""",
            GL_FRAGMENT_SHADER
        )
        # noinspection PyAttributeOutsideInit
        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)

        # noinspection PyAttributeOutsideInit
        self.vbo = vbo.VBO(
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


    def Render(self):
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointerf(vbo)
                glDrawArrays(GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)

        finally:
            shaders.glUseProgram(0)


def main():
    TestContext.ContextMainLoop()


if __name__ == "__main__":
    main()
