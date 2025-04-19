## Overview

This project is a game developed using Python, OpenGL, and ImGui. The game consists of multiple screens and levels, including a main menu, gameplay scenes, and a game over screen. The player can move, jump, and interact with various objects in the game world.

## Project Structure
- **assets/objects/objects.py**: Contains definitions for various game objects like the player, enemies, platforms, etc.
- **utils/window_manager.py**: Manages the game window and handles input events.
- **MainMenu.py**: Implements the main menu of the game.
- **game.py**: Contains the main game logic, including different game screens and their updates.
- **main.py**: Entry point of the game, initializes the game and starts the render loop.

## Requirements

- Python 3.x
- GLFW
- PyOpenGL
- ImGui
- Pillow (PIL)
- JSON

## Installation

1. Install the required Python packages:
    sh
    pip install glfw PyOpenGL imgui Pillow
    

## Running the Game

To run the game, execute the `main.py` file:
sh
python main.py

## The Three Levels

The game has three levels.

1. The biome of 1st level is river biome. The enemies are fishes and the platforms are stones on which player has to jump.
2. The biome of 2nd level is space biome. The enemies are aliens, our player is an astronaut, and the platforms are asteroids. There is a unique mechanic of anti-gravity as well which makes this level slightly harder.
3. Th biome of 3rd level is mystic biome. The enemies are wizards, our player is a mystic, and the platforms are magical mats/carpets. This level is hard due to the large size of the enemies which are hard to escape.

## Controls

- **Arrow Keys**: Navigate the main menu.
- **Enter**: Select menu option.
- **W, A, S, D**: Move the player.
- **Space**: Jump.
- **Mouse Click**: To select "Sace Game" or "Load Game".

## Saving and Loading

- **Save Game**: Click the "Save Game" button in the in-game menu to save the current game state.
- **Load Game**: Select "LOAD GAME" from the main menu to load the previously saved game state.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenGL for rendering graphics.
- ImGui for the graphical user interface.
- GLFW for window management and input handling.

```
