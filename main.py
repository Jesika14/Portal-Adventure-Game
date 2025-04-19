from OpenGL.GL import *
from utils.window_manager import Window
from game import Game
import OpenGL.GL as gl
import glfw
import imgui
import random
from assets.objects.objects import *
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image

class App:
    def __init__(self, width, height):
        self.window = Window(height, width)
        self.game = Game(height, width)
    def RenderLoop(self):

        while self.window.IsOpen():
            inputs, time = self.window.StartFrame(0.0, 0.0, 0.0, 1.0)
            self.game.ProcessFrame(self.window, inputs, time)
            self.window.EndFrame()

if __name__ == "__main__":
    app = App(1000, 1000)
    app.RenderLoop()