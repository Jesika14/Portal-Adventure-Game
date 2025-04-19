import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import *
from MainMenu import *
import time
from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import json

GRAVITY = -500
JUMP_STRENGTH = 500
PLAYER_SPEED = 250

class Game:
    def __init__(self, height, width):
        self.won = False
        self.height = height
        self.width = width
        self.screen = -2
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.objects = []
        self.lives = 3
        self.health = 100
        self.playerStop = True
        self.gravity = GRAVITY
        self.menu = MainMenu()
        self.last_hit_time = 0
        self.cool_down_time = 3.0
        self.keys_collected = 0
        self.total_keys = 3
        self.keys = []

    def InitScreen(self):
        if self.screen == -1:
            pass
        if self.screen == 0:
            self.screen0()
        if self.screen == 1:
            self.screen1()
        if self.screen == 2:
            self.screen2()

    def screen0(self):
        background = Object(self.shaders[0], backgroundProps)
        self.player = Object(self.shaders[0], playerProps)
        self.player.properties['position'] = np.array([-self.width//2 + 50, -self.height//2 + 50, 0], dtype=np.float32)
        fishes = []
        asteroids = []
        self.objects.append(background)
        self.objects.append(self.player)
        for i in range (10):
            fishes.append(Object(self.shaders[0], fishProps))
            fishes[i].properties['position'] = np.array([np.random.randint(self.objects[0].properties['river_banks'][0], self.objects[0].properties['river_banks'][1]-100), np.random.randint(-self.height//2, self.height//2), 3], dtype=np.float32)
            fishes[i].properties['velocity'] = np.array([np.random.randint(-100, 100), np.random.randint(-100, -60), 0], dtype=np.float32)
            asteroids.append(Object(self.shaders[0], stoneProps))
            asteroids[i].properties['position'] = np.array([-300 + i*60, np.random.randint(-self.height//2, self.height//2), 0], dtype=np.float32)
            asteroids[i].properties['velocity'][1] = np.random.choice(np.concatenate((np.random.uniform((-100, -80), 1), np.random.uniform((80, 100), 1))), 1)
            self.objects.append(fishes[i])
            self.objects.append(asteroids[i])

        for i in range(self.total_keys):
            key = Object(self.shaders[0], keyProps)
            platform = asteroids[np.random.randint(0, len(asteroids))]  # Choose a random platform
            key.properties['position'] = np.array([platform.properties['position'][0], platform.properties['position'][1] + 20, 20], dtype=np.float32)
            key.properties['platform'] = platform  # Link key to platform
            self.keys.append(key)
            self.objects.append(key)

    def ProcessFrame(self, window, inputs, time):
        self.window = window
        if self.screen == -2:
            self.screen = -1
        if self.screen == -1:
            self.DrawText()
            self.UpdateScene(inputs, time)
        if self.screen == 0:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
        if self.screen == 1:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
        if self.screen == 2:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
        
    def DrawText(self):
        imgui.new_frame()
        if self.screen == -1:
            x = self.menu.handle_input(self.window.window)
            self.menu.draw()
            if self.won:
                imgui.set_next_window_position(10, self.height//2)
                imgui.set_next_window_size(100, -100)
                imgui.begin("Win Message", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
                
                imgui.text_colored("YOU WON!", 0, 0.8, 0, 1)  # Green text
                imgui.set_window_font_scale(1.5)  # Slightly larger font
                
                imgui.end()
            if(x == "new_game"):
                self.screen = 0
                self.InitScreen()
            elif (x=="load_game"):
                self.load_game()
        imgui.render()

    def screen0_text(self):
        imgui.new_frame()
        # imgui.set_next_window_size(500, 500)
        # imgui.begin("Welcome to the Game")
        # imgui.text("Press Enter to start the game")
        # self.InitScreen()
        # print('I am hereeeee')
        # imgui.end()
        imgui.render()
        # imgui.impl_glfw_NewFrame()
        # imgui.impl_opengl3_NewFrame()
        # imgui.impl_opengl3_RenderDrawData(imgui.get_draw_data())


    def UpdateScene(self, inputs, time):
        if self.screen == 0:
            self.Scene0Update(inputs, time)
        if self.screen == 1:
            self.Scene1Update(inputs, time)
        if self.screen == 2:
            self.Scene2Update(inputs, time)

    def Scene0Update(self, inputs, time):
        dt = time["deltaTime"]
        # print("Velocity_start: ", self.player.properties["velocity"])
        # Collision with asteroids (platforms)
        for obj in self.objects:
            # print(obj.properties)
            if "platform" in obj.properties["type"]:
                player_x, player_y, _ = self.player.properties["position"]
                asteroid_x, asteroid_y, _ = obj.properties["position"]
                
                if abs(player_x - asteroid_x) < 40 and abs(player_y - asteroid_y) < 40:
                    self.playerStop = True
                    self.player.properties["velocity"][1] = obj.properties["velocity"][1]  # Move with the platform
                    self.player.properties["velocity"][0] = obj.properties["velocity"][0]  # Move with the platform
                    # self.player.properties["position"][1] = asteroid_y + 10  # Place self.player on top
                    # self.player.properties['position'][1] += self.player.properties['velocity'][1] * dt
                    # print("Player: ", self.player.properties["position"])
        
        # Collision with aliens (enemies)
        for obj in self.objects:
            if "enemy" in obj.properties["type"]:
                player_x, player_y, _ = self.player.properties["position"]
                alien_x, alien_y, _ = obj.properties["position"]

                if abs(player_x - alien_x) < 20 and abs(player_y - alien_y) < 20:
                    # Only reduce health if cooldown has passed
                    if time["currentTime"] - self.last_hit_time > self.cool_down_time:
                        self.health -= 25  # Reduce health on collision
                        self.last_hit_time = time["currentTime"]  # Update last hit time
                        print(f"Health: {self.health}")

                        if self.health <= 0:
                            print("Game Over!")
                            self.screen = 3  # Move to Game Over screen

        # Platform movement
        for obj in self.objects:
            if obj.properties['type'] == 'platform':
                # obj.properties['velocity'][1] = random.randint(0, 100)  # Randomize platform speed
                obj.properties['position'][1] += obj.properties['velocity'][1] * time['deltaTime']  # Move left continuously

                # Reset asteroid position when it moves out of bounds
                if obj.properties['position'][1] <= -self.height//2 or obj.properties['position'][1] >= self.height//2:
                    obj.properties['velocity'][1] *= -1
                    # obj.properties['position'][1] = self.height//2

        # Enenmy movement
        for obj in self.objects:
            if obj.properties['type'] == 'enemy':

                obj.properties['position'][0] += obj.properties['velocity'][0] * dt
                obj.properties['position'][1] += obj.properties['velocity'][1] * dt

                # Bounce fish off screen edges
                if obj.properties['position'][0] < -self.width//2 + 160 or obj.properties['position'][0] > self.width//2 - 160:
                    obj.properties['velocity'][0] *= -1  # Reverse x direction
                if obj.properties['position'][1] < -self.height//2 or obj.properties['position'][1] > self.height//2:
                    obj.properties['velocity'][1] *= -1  # Reverse y direction

        if "D" in inputs:  # Move right
            self.player.properties["position"][0] += PLAYER_SPEED * dt
            if self.playerStop:
                self.playerStop = False
        if "A" in inputs:  # Move left
            self.player.properties["position"][0] -= PLAYER_SPEED * dt
            if self.playerStop:
                self.playerStop = False
        # Jump logic
        if "SPACE" in inputs and self.playerStop:
            print(self.player.properties["velocity"][1])
            self.player.properties["velocity"][1] += JUMP_STRENGTH
            print(self.player.properties["velocity"][1])
            self.playerStop = False
            print("hell")
            self.player.properties["position"][1] += self.player.properties["velocity"][1] * dt
            # self.player.properties["on_ground"] = False

        if -self.width//2<self.player.properties["position"][0] <self.objects[0].properties["river_banks"][0] or self.objects[0].properties["river_banks"][1]<self.player.properties["position"][0]<self.width//2:
            self.gravity = 0
            self.playerStop = True
            # print('1st true')
            self.player.properties["velocity"][1] = 0
            self.player.properties["velocity"][0] = 0
        # print("Velocity_collison: ", self.player.properties["velocity"])
        # Check if player reached the right side
        if not self.playerStop:
            self.gravity = GRAVITY
            self.player.properties["velocity"][1] += self.gravity*dt    
        
        self.player.properties['position'] += self.player.properties['velocity'] * dt
        # print("Velocity_end: ", self.player.properties["velocity"])
        # print("Position", self.player.properties["position"])

        if self.player.properties["position"][1]<-self.height//2 and not self.playerStop:
            self.lives -= 1
            self.player.properties['position'] = np.array([-self.width//2 + 50, -self.height//2 + 50, 0], dtype=np.float32)

        if self.lives == 0:
            print("Game Over!")
            self.screen = 3

        for key in self.keys:
            platform = key.properties['platform']
            key.properties['position'][1] = platform.properties['position'][1] + 20  # Keep key moving with platform

        for obj in self.objects:
            if obj.properties["type"] == "key":
                player_x, player_y, _ = self.player.properties["position"]
                key_x, key_y, _ = obj.properties["position"]
                
                if abs(player_x - key_x) < 20 and abs(player_y - key_y) < 20:
                    self.objects.remove(obj)
                    self.keys.remove(obj)
                    self.keys_collected += 1
                    print(f"Keys Collected: {self.keys_collected}/{self.total_keys}")

        if self.keys_collected == self.total_keys and self.player.properties["position"][0] > self.objects[0].properties["river_banks"][1]+50:
            print("Level Complete!")
            self.screen = 1
            self.objects.clear()
            self.keys.clear()
            self.screen1()


    def screen1(self):
        # self.objects = []
        background = Object(self.shaders[0], backgroundSpaceProps)
        self.player = Object(self.shaders[0], astronautProps)
        self.player.properties['position'] = np.array([-self.width//2 + 50, -self.height//2 + 50, 0], dtype=np.float32)
        aliens = []
        asteroids = []
        self.objects.append(background)
        self.objects.append(self.player)
        for i in range (7):
            aliens.append(Object(self.shaders[0], alienProps))
            aliens[i].properties['position'] = np.array([np.random.randint(-self.width//2 + 100, self.width//2 - 100), np.random.randint(0, self.height), 3], dtype=np.float32)
            aliens[i].properties['velocity'] = np.array([np.random.randint(-100, 100), np.random.randint(-100, 100), 0], dtype=np.float32)
            asteroids.append(Object(self.shaders[0], asteroidProps))
            asteroids[i].properties['position'] = np.array([-300 + i*100, np.random.randint(-self.height//2, self.height//2), 0], dtype=np.float32)
            asteroids[i].properties['velocity'][0] = np.random.randint(-100, 100)
            asteroids[i].properties['velocity'][1] = np.random.randint(-100, 100)

            self.objects.append(aliens[i])
            self.objects.append(asteroids[i])

    def Scene1Update(self, inputs, time):
        dt = time["deltaTime"]
        # print("Velocity_start: ", self.player.properties["velocity"])
        # Collision with asteroids (platforms)
        for obj in self.objects:
            # print(obj.properties)
            if "platform" in obj.properties["type"]:
                player_x, player_y, _ = self.player.properties["position"]
                asteroid_x, asteroid_y, _ = obj.properties["position"]
                
                if abs(player_x - asteroid_x) < 40 and abs(player_y - asteroid_y) < 40:
                    print("collided")
                    self.playerStop = True
                    self.player.properties["velocity"][1] = obj.properties["velocity"][1]  # Move with the platform
                    self.player.properties["velocity"][0] = obj.properties["velocity"][0]  # Move with the platform
                    # self.player.properties["position"][1] = asteroid_y + 10  # Place self.player on top
                    # self.player.properties['position'][1] += self.player.properties['velocity'][1] * dt
                    # print("Player: ", self.player.properties["position"])
        
        # Collision with aliens (enemies)
        for obj in self.objects:
            if "enemy" in obj.properties["type"]:
                player_x, player_y, _ = self.player.properties["position"]
                alien_x, alien_y, _ = obj.properties["position"]

                if abs(player_x - alien_x) < 20 and abs(player_y - alien_y) < 20:
                    # Only reduce health if cooldown has passed
                    if time["currentTime"] - self.last_hit_time > self.cool_down_time:
                        self.health -= 25  # Reduce health on collision
                        self.last_hit_time = time["currentTime"]  # Update last hit time
                        print(f"Health: {self.health}")

                        if self.health <= 0:
                            print("Game Over!")
                            self.screen = 3  # Move to Game Over screen

        # Platform movement
        for obj in self.objects:
            if obj.properties['type'] == 'platform':
                # obj.properties['velocity'][1] = random.randint(0, 100)  # Randomize platform speed
                obj.properties['position'][1] += obj.properties['velocity'][1] * time['deltaTime']  # Move left continuously

                # Reset asteroid position when it moves out of bounds
                if obj.properties['position'][1] <= -self.height//2 or obj.properties['position'][1] >= self.height//2:
                    obj.properties['velocity'][1] *= -1

                if obj.properties['position'][0] <= -self.width//2 + 100 or obj.properties['position'][0] >= self.width//2 - 100:
                    obj.properties['velocity'][0] *= -1
                    # obj.properties['position'][1] = self.height//2

        # Enenmy movement
        for obj in self.objects:
            if obj.properties['type'] == 'enemy':

                obj.properties['position'][0] += obj.properties['velocity'][0] * dt
                obj.properties['position'][1] += obj.properties['velocity'][1] * dt

                # Bounce fish off screen edges
                if obj.properties['position'][0] < -self.width//2 + 160 or obj.properties['position'][0] > self.width//2 - 160:
                    obj.properties['velocity'][0] *= -1  # Reverse x direction
                if obj.properties['position'][1] < -self.height//2 or obj.properties['position'][1] > self.height//2:
                    obj.properties['velocity'][1] *= -1  # Reverse y direction

        if "D" in inputs:  # Move right
            self.player.properties["position"][0] += PLAYER_SPEED * dt
            if self.playerStop:
                self.playerStop = False
        if "A" in inputs:  # Move left
            self.player.properties["position"][0] -= PLAYER_SPEED * dt
            if self.playerStop:
                self.playerStop = False
        # Jump logic
        if "SPACE" in inputs and self.playerStop:
            print(self.player.properties["velocity"][1])
            self.player.properties["velocity"][1] += JUMP_STRENGTH
            print(self.player.properties["velocity"][1])
            self.playerStop = False
            print("hell")
            self.player.properties["position"][1] += self.player.properties["velocity"][1] * dt
            # self.player.properties["on_ground"] = False

        if -self.width//2<self.player.properties["position"][0] <self.objects[0].properties["river_banks"][0]:
            self.gravity = 0
            self.playerStop = True
            # print('1st true')
            self.player.properties["velocity"][1] = 0
            self.player.properties["velocity"][0] = 0

        # Check if player reached the right side
        if not self.playerStop:
            self.gravity = GRAVITY
            self.player.properties["velocity"][1] += self.gravity*dt    
        
        self.player.properties['position'] += self.player.properties['velocity'] * dt

        if self.player.properties["position"][1]<-self.height//2 and not self.playerStop:
            self.lives -= 1
            self.player.properties['position'] = np.array([-self.width//2 + 50, -self.height//2 + 50, 0], dtype=np.float32)

        if self.lives == 0:
            print("Game Over!")
            self.screen = 3

        if self.player.properties["position"][0] > self.objects[0].properties["river_banks"][1]+50:
            print("Level Complete!")
            self.screen = 2
            # self.ProcessFrame(self.window, inputs, time)
            self.objects.clear()
            self.screen2()

    def screen2(self):
        background = Object(self.shaders[0], backgroundMysticProps)
        self.player = Object(self.shaders[0], mysticPlayerProps)
        self.player.properties['position'] = np.array([-self.width//2 + 50, -self.height//2 + 50, 0], dtype=np.float32)
        wizards = []
        mats = []
        self.objects.append(background)
        self.objects.append(self.player)
        for i in range (10):
            wizards.append(Object(self.shaders[0], wizardProps))
            wizards[i].properties['position'] = np.array([np.random.randint(self.objects[0].properties['river_banks'][0], self.objects[0].properties['river_banks'][1]-100), np.random.randint(-self.height//2, self.height//2), 3], dtype=np.float32)
            wizards[i].properties['velocity'] = np.array([np.random.randint(-100, 100), np.random.randint(-100, -60), 0], dtype=np.float32)
            mats.append(Object(self.shaders[0], magicalMatProps))
            mats[i].properties['position'] = np.array([-300 + i*60, np.random.randint(-self.height//2, self.height//2), 0], dtype=np.float32)
            mats[i].properties['velocity'][1] = np.random.choice(np.concatenate((np.random.uniform((-100, -80), 1), np.random.uniform((80, 100), 1))), 1)
            self.objects.append(wizards[i])
            self.objects.append(mats[i])

        for i in range(self.total_keys):
            key = Object(self.shaders[0], keyProps)
            platform = mats[np.random.randint(0, len(mats))]  # Choose a random platform
            key.properties['position'] = np.array([platform.properties['position'][0], platform.properties['position'][1] + 20, 20], dtype=np.float32)
            key.properties['platform'] = platform  # Link key to platform
            self.keys.append(key)
            self.objects.append(key)
        

    def Scene2Update(self, inputs, time):
        dt = time["deltaTime"]
        # print("Velocity_start: ", self.player.properties["velocity"])
        # Collision with asteroids (platforms)
        for obj in self.objects:
            # print(obj.properties)
            if "platform" in obj.properties["type"]:
                player_x, player_y, _ = self.player.properties["position"]
                asteroid_x, asteroid_y, _ = obj.properties["position"]
                
                if abs(player_x - asteroid_x) < 40 and abs(player_y - asteroid_y) < 40:
                    self.playerStop = True
                    self.player.properties["velocity"][1] = obj.properties["velocity"][1]  # Move with the platform
                    self.player.properties["velocity"][0] = obj.properties["velocity"][0]  # Move with the platform
                    # self.player.properties["position"][1] = asteroid_y + 10  # Place self.player on top
                    # self.player.properties['position'][1] += self.player.properties['velocity'][1] * dt
                    # print("Player: ", self.player.properties["position"])
        
        # Collision with aliens (enemies)
        for obj in self.objects:
            if "enemy" in obj.properties["type"]:
                player_x, player_y, _ = self.player.properties["position"]
                alien_x, alien_y, _ = obj.properties["position"]

                if abs(player_x - alien_x) < 20 and abs(player_y - alien_y) < 20:
                    # Only reduce health if cooldown has passed
                    if time["currentTime"] - self.last_hit_time > self.cool_down_time:
                        self.health -= 25  # Reduce health on collision
                        self.last_hit_time = time["currentTime"]  # Update last hit time
                        print(f"Health: {self.health}")

                        if self.health <= 0:
                            print("Game Over!")
                            self.screen = 3  # Move to Game Over screen

        # Platform movement
        for obj in self.objects:
            if obj.properties['type'] == 'platform':
                # obj.properties['velocity'][1] = random.randint(0, 100)  # Randomize platform speed
                obj.properties['position'][1] += obj.properties['velocity'][1] * time['deltaTime']  # Move left continuously

                # Reset asteroid position when it moves out of bounds
                if obj.properties['position'][1] <= -self.height//2 or obj.properties['position'][1] >= self.height//2:
                    obj.properties['velocity'][1] *= -1
                    # obj.properties['position'][1] = self.height//2

        # Enenmy movement
        for obj in self.objects:
            if obj.properties['type'] == 'enemy':

                obj.properties['position'][0] += obj.properties['velocity'][0] * dt
                obj.properties['position'][1] += obj.properties['velocity'][1] * dt

                # Bounce fish off screen edges
                if obj.properties['position'][0] < -self.width//2 + 160 or obj.properties['position'][0] > self.width//2 - 160:
                    obj.properties['velocity'][0] *= -1  # Reverse x direction
                if obj.properties['position'][1] < -self.height//2 or obj.properties['position'][1] > self.height//2:
                    obj.properties['velocity'][1] *= -1  # Reverse y direction

        if "D" in inputs:  # Move right
            self.player.properties["position"][0] += PLAYER_SPEED * dt
            if self.playerStop:
                self.playerStop = False
        if "A" in inputs:  # Move left
            self.player.properties["position"][0] -= PLAYER_SPEED * dt
            if self.playerStop:
                self.playerStop = False
        # Jump logic
        if "SPACE" in inputs and self.playerStop:
            print(self.player.properties["velocity"][1])
            self.player.properties["velocity"][1] += JUMP_STRENGTH
            print(self.player.properties["velocity"][1])
            self.playerStop = False
            print("hell")
            self.player.properties["position"][1] += self.player.properties["velocity"][1] * dt
            # self.player.properties["on_ground"] = False

        if -self.width//2<self.player.properties["position"][0] <self.objects[0].properties["river_banks"][0] or self.objects[0].properties["river_banks"][1]<self.player.properties["position"][0]<self.width//2:
            self.gravity = 0
            self.playerStop = True
            # print('1st true')
            self.player.properties["velocity"][1] = 0
            self.player.properties["velocity"][0] = 0
        # print("Velocity_collison: ", self.player.properties["velocity"])
        # Check if player reached the right side
        if not self.playerStop:
            self.gravity = GRAVITY
            self.player.properties["velocity"][1] += self.gravity*dt    
        
        self.player.properties['position'] += self.player.properties['velocity'] * dt
        # print("Velocity_end: ", self.player.properties["velocity"])
        # print("Position", self.player.properties["position"])

        if self.player.properties["position"][1]<-self.height//2 and not self.playerStop:
            self.lives -= 1
            self.player.properties['position'] = np.array([-self.width//2 + 50, -self.height//2 + 50, 0], dtype=np.float32)

        if self.lives == 0:
            print("Game Over!")
            self.screen = 3

        for key in self.keys:
            platform = key.properties['platform']
            key.properties['position'][1] = platform.properties['position'][1] + 20  # Keep key moving with platform

        for obj in self.objects:
            if obj.properties["type"] == "key":
                player_x, player_y, _ = self.player.properties["position"]
                key_x, key_y, _ = obj.properties["position"]
                
                if abs(player_x - key_x) < 20 and abs(player_y - key_y) < 20:
                    self.objects.remove(obj)
                    self.keys.remove(obj)
                    self.keys_collected += 1
                    print(f"Keys Collected: {self.keys_collected}/{self.total_keys}")

        if self.keys_collected == self.total_keys and self.player.properties["position"][0] > self.objects[0].properties["river_banks"][1]:
            print("Game Complete!")
            self.won = True
            

    def DrawScene(self):
        if self.screen == 0:
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()

        elif self.screen == 1:
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()

        elif self.screen == 2:
            for shader in self.shaders:
                self.camera.Update(shader)

            for obj in self.objects:
                obj.Draw()

        elif self.screen == 3:
            self.game_over()
            # return

         # Draw Health Bar and Lives
        imgui.new_frame()
        
        imgui.set_next_window_position(10, 10)
        imgui.set_next_window_size(200, 50)
        imgui.begin("HUD", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        
        # Health Bar
        # imgui.text("Health")
        imgui.text(f"Health: {self.health}")
        
        # Lives
        imgui.separator()
        imgui.text(f"Lives: {self.lives}")
        
        imgui.end()
        imgui.set_next_window_position(self.width - 220, 10)
        imgui.set_next_window_size(200, 80)
        imgui.begin("Options", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        
        if imgui.button("Save Game"):
            print("Game saved.")
            self.save_game()
        
        if imgui.button("Quit Game"):
            self.screen = -1  # Return to main menu
            print("Game quit.")
            self.objects.clear()
        
        imgui.end()
        imgui.render()

    def save_game(self):
        game_data = {
            "screen": self.screen,
            "player": {
                "health": self.health,
                "lives": self.lives,
            }
        }
        with open("save_game.json", "w") as f:
            json.dump(game_data, f)

    def load_game(self, filename="save_game.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            # Restore player attributes
            self.health = data["player"]["health"]
            self.lives = data["player"]["lives"]

            # Restore game level
            self.screen = data["screen"]

            if self.screen == 0:
                self.screen0()
            elif self.screen == 1:
                self.screen1()
            elif self.screen == 2:
                self.screen2()

            print("Game loaded successfully.")
        except FileNotFoundError:
            print("Save file not found. Starting a new game.")
        except Exception as e:
            print(f"Error loading game: {e}")

    def game_over(self):
        """Displays the game over screen before returning to the main menu."""
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        imgui.new_frame()

        # Center the Game Over message
        imgui.set_next_window_position(self.width // 2 - 100, self.height // 2 - 50)
        imgui.set_next_window_size(200, 100)
        imgui.begin("Game Over", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        imgui.text("GAME OVER")
        imgui.text("Press any key to continue...")

        imgui.end()
        imgui.render()  
        # self.objects.clear()
        # Wait for user input instead of using time.sleep()
        # if self.any_key_pressed():
        self.objects.clear()
        self.screen = -1  # Return to the main menu
        self.DrawText()
        self.health = 100
        self.lives = 3

    def any_key_pressed(self):
        for key in range(32, 349):  # Checks all GLFW key codes
            if glfw.get_key(self.window.window, key) == glfw.PRESS:
                return True
        return False

    def game_end(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        imgui.new_frame()
        imgui.set_next_window_position(self.width / 2 - 150, self.height / 2 - 50)
        imgui.set_next_window_size(300, 100)
        imgui.begin("Game Won", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        
        imgui.set_window_font_scale(2.5)  # Increase font size for emphasis
        imgui.text_colored("YOU WON!", 0, 0.5, 0, 1)  # Green text on white screen
        
        if imgui.button("Return to Main Menu"):
            self.screen = 0  # Return to main menu
        
        imgui.end()
        imgui.render()
