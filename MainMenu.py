import imgui
import glfw

class MainMenu:
    def __init__(self):
        self.selected_index = 0  # 0 -> NEW GAME, 1 -> LOAD GAME

    def handle_input(self, window):
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            self.selected_index = (self.selected_index + 1) % 2  # Toggle between 0 and 1
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            self.selected_index = (self.selected_index - 1) % 2
        if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS:
            if self.selected_index == 0:
                print("Starting New Game...")
                return "new_game"
            elif self.selected_index == 1:
                print("Loading Game...")
                return "load_game"
        return None  # No selection made yet

    def draw(self):
        imgui.begin("Main Menu")
        
        # Draw menu options
        if self.selected_index == 0:
            imgui.text_colored("-> NEW GAME", 1, 1, 0, 1)  # Highlighted in yellow
        else:
            imgui.text("   NEW GAME")

        if self.selected_index == 1:
            imgui.text_colored("-> LOAD GAME", 1, 1, 0, 1)  # Highlighted in yellow
        else:
            imgui.text("   LOAD GAME")
        
        imgui.end()
