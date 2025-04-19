import ctypes
import numpy as np
import copy
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image

class VBO:
    def __init__(self, vertices):
        self.ID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    def Use(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)
    def Delete(self):
        glDeleteBuffers(1, (self.ID,))

class IBO:
    def __init__(self, indices):
        self.ID = glGenBuffers(1)
        self.count = len(indices)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    def Use(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
    def Delete(self):
        glDeleteBuffers(1, (self.ID,))

class VAO:
    def __init__(self, vbo : VBO, texture=None):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        vbo.Use()

        if texture:
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, ctypes.c_uint(8 * ctypes.sizeof(ctypes.c_float)), ctypes.c_void_p(0))
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, ctypes.c_uint(8 * ctypes.sizeof(ctypes.c_float)), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, ctypes.c_uint(8 * ctypes.sizeof(ctypes.c_float)), ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        else:
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, ctypes.c_uint(6 * ctypes.sizeof(ctypes.c_float)), ctypes.c_void_p(0))
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, ctypes.c_uint(6 * ctypes.sizeof(ctypes.c_float)), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))

    def Use(self):
        glBindVertexArray(self.vao)
    def Delete(self):
        glDeleteVertexArrays(1, (self.vao,))

class Shader:
    def __init__(self, vertex_shader, fragment_shader):
        self.ID = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
        self.Use()
    def Use(self):
        glUseProgram(self.ID)
    def Delete(self):
        glDeleteProgram((self.ID,))

class Camera:
    def __init__(self, height, width):
        self.height = height
        self.width = width
    def Update(self, shader):
        shader.Use()

        camMatrix = np.array([[2.0/self.width, 0,0,0],[0,2.0/self.height,0,0],[0,0,-1/100,0],[0,0,0,1]], dtype = np.float32)

        camMatrixLocation = glGetUniformLocation(shader.ID, "camMatrix".encode('utf-8'))
        glUniformMatrix4fv(camMatrixLocation, 1, GL_TRUE, camMatrix)


class Object:
    def __init__(self, shader, properties, texture_path=None):
        self.properties = copy.deepcopy(properties)

        self.vbo = VBO(self.properties['vertices'])
        self.ibo = IBO(self.properties['indices'])
        self.vao = VAO(self.vbo,texture_path)

        self.properties.pop('vertices')
        self.properties.pop('indices')
        # Create shaders
        self.shader = shader

        # Load texture if provided
        self.texture = None
        if texture_path:
            self.texture = self.load_texture(texture_path)

        # Set default opacity
        self.opacity = self.properties.get('opacity', 1.0)

    def load_texture(self, path):
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.convert("RGBA")  # Ensure the image has an alpha channel
        img_data = image.tobytes()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        # glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture

    def Draw(self):

        position = self.properties['position']
        rotation_z = self.properties['rotation_z']
        scale = self.properties['scale']
        translation_matrix = np.array([[1, 0, 0, position[0]], [0, 1, 0, position[1]], [0, 0, 1, position[2]], [0, 0, 0, 1]], dtype=np.float32)
        rotation_z_matrix = np.array([[np.cos(rotation_z), -np.sin(rotation_z), 0, 0], [np.sin(rotation_z), np.cos(rotation_z), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32)
        scale_matrix = np.array([[scale[0], 0, 0, 0], [0, scale[1], 0, 0], [0, 0, scale[2], 0], [0, 0, 0, 1]], dtype=np.float32)
        model_matrix = translation_matrix @ rotation_z_matrix @ scale_matrix

        # Bind the shader, set uniforms, bind vao (automatically binds vbo) and ibo
        self.shader.Use()
        modelMatrixLocation = glGetUniformLocation(self.shader.ID, "modelMatrix".encode('utf-8'))
        glUniformMatrix4fv(modelMatrixLocation, 1, GL_TRUE, model_matrix)

        useTextureLocation = glGetUniformLocation(self.shader.ID, "useTexture".encode('utf-8'))
        opacityLocation = glGetUniformLocation(self.shader.ID, "opacity".encode('utf-8'))
        glUniform1f(opacityLocation, self.opacity)

        if self.texture:
            glUniform1i(useTextureLocation, GL_TRUE)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            textureSamplerLocation = glGetUniformLocation(self.shader.ID, "textureSampler".encode('utf-8'))
            glUniform1i(textureSamplerLocation, GL_FALSE)            
        else:
            glUniform1i(useTextureLocation, GL_FALSE)

        self.vao.Use()
        self.ibo.Use()

        # Issue Draw call with primitive type
        glDrawElements(GL_TRIANGLES, self.ibo.count, GL_UNSIGNED_INT, None)
