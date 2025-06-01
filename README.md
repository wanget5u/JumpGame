# Jump Game

A game that bears resemblence to the popular game <b>"Geometry Dash"</b>. Made entirely from scratch by using <b>pygame</b> library. Project serves as a <b>PPY</b> class final assignment at my university.

![screenshot](assets/screenshot5.PNG)

## About 
    
### How to Play
- **Left mouse click/Up Arrow**: Jump
- **Hold**: Continuous jumping
- **Escape**: Returns you to the previous window state
- Navigate through obstacles and reach the end of each level
- Avoid spikes and other hazards
- Time your jumps carefully to maintain momentum

## Features: </h4>

    - Custom Physics Engine: Built from scratch using pygame
    - Multiple Levels: Various challenging levels with increasing difficulty
    - Collision Detection: Precise collision system for blocks and spikes
    - Smooth Gameplay: Optimized performance for responsive controls
    - Asset Management: Organized sprite and sound assets
    - Level Editor: For level edition (loading and saving available)

## Project Structure

```
JumpGame/
├── .idea/          # IDE configuration files
├── assets/         # Game sprites, sounds, and other media
├── config/         # Game configuration files
├── game/           # Core game logic and mechanics
├── levels/         # Level definitions and layouts
├── objects/        # Game objects (player, obstacles, etc.)
├── ui/             # User interface components
├── main.py         # Main game entry point
├── requirements.txt # Python dependencies
└── Dockerfile      # Docker configuration
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/wanget5u/JumpGame.git
   cd JumpGame
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

### Docker Setup

Alternatively, you can run the game using Docker:

```bash
  docker build -t jump-game .
  docker run -it jump-game
```

### WebApp Setup

You can also run the game with <b>pygbag</b> by running. Game should be available on http://localhost:8000/
```bash
  cd .
  pygbag JumpGame
```

# In-game screenshots

### Title menu:

![screenshot](assets/screenshot1.PNG)

### Level editor:

![screenshot](assets/screenshot2.PNG)

### Level loader:

![screenshot](assets/screenshot3.PNG)

### Level save:

![screenshot](assets/screenshot4.PNG)
