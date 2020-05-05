import numpy as np
import OpenGL.GL as gl

class Viewer:

    __x, __y, __z = None, None, None
    __array = None
    __texture = None
    __current_layer = 0
    __vbo_texture = None
    __loaded = False
    __need_reload = True

    def set_tomogram(self, shape: tuple, array: np.ndarray):
        self.__x, self.__y, self.__z = shape
        self.__array = array
        self.__loaded = True
        self.__need_reload = True
        __current_layer = 0

    def set_layer(self, layer: int):
        self.__current_layer = layer
        self.__need_reload = True
        
    def setup_view(self, width: int, height: int):
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self.__x, 0, self.__y, -1, 1)
        gl.glViewport(0, 0, width, height)

    def paint_quads(self):
        if self.__loaded:
            self.__draw_quads()

    def paint_texture(self):
        if self.__loaded:
            if self.__need_reload:
                self.__vbo_texture = gl.glGenTextures(1)
                self.__generate_texture_image()
                self.__load_2d_texture()
                self.__need_reload = False
            self.__draw_texture()

    def __transfer_function(self, value: int):
        min, max = 0, 2000
        newValue = int(np.clip((value-min)*255/(max-min), 0, 255))
        return newValue, newValue, newValue, 255

    def __draw_quads(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )
        gl.glBegin(gl.GL_QUADS)
        for x in range(self.__x-1):
            for y in range(self.__y-1):
                value = self.__array[x+y*self.__x+self.__current_layer*self.__x*self.__y]
                gl.glColor(self.__transfer_function(value))
                gl.glVertex(x, y)

                value = self.__array[x+(y+1)*self.__x+self.__current_layer*self.__x*self.__y]
                gl.glColor(self.__transfer_function(value))
                gl.glVertex(x, y+1)

                value = self.__array[(x+1)+(y+1)*self.__x+self.__current_layer*self.__x*self.__y]
                gl.glColor(self.__transfer_function(value))
                gl.glVertex(x+1, y+1)

                value = self.__array[(x+1)+(y+1)*self.__x+self.__current_layer*self.__x*self.__y]
                gl.glColor(self.__transfer_function(value))
                gl.glVertex(x+1, y)
        gl.glEnd()

    def __generate_texture_image(self):
        self.__texture = np.zeros(shape=(self.__x, self.__y, 4), dtype=np.uint8)
        for x in range(self.__x):
            for y in range(self.__y):
                value = self.__array[x+y*self.__x+self.__current_layer*self.__x*self.__y]
                self.__texture[x][y] = self.__transfer_function(value)

    def __load_2d_texture(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__vbo_texture)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA,
            self.__x, self.__y, 0, gl.GL_RGBA, 
            gl.GL_UNSIGNED_BYTE, self.__texture)

    def __draw_texture(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__vbo_texture)
        gl.glBegin(gl.GL_QUADS)

        gl.glTexCoord2f(0, 0)
        gl.glVertex(0, 0)

        gl.glTexCoord2f(0, 1)
        gl.glVertex(0, self.__y)

        gl.glTexCoord2f(1, 1)
        gl.glVertex(self.__x, self.__y)

        gl.glTexCoord2f(1, 0)
        gl.glVertex(self.__x, 0)

        gl.glEnd()
        gl.glDisable(gl.GL_TEXTURE_2D)
