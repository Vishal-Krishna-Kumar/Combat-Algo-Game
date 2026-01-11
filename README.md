# DOOM style 3d (raycasting) game in Python (based on Wolfenstein 3d)

Control: 'WASD' + mouse

![doom](/sreenshots/0.jpg)
# Combat — DOOM-Style 3D Raycasting FPS (Python + Pygame)

A DOOM/Wolfenstein-inspired first-person shooter built in **Python** using **Pygame**, featuring a real-time **raycasting engine**, **AI-controlled enemies**, shortest-path navigation (A*/grid pathfinding), and gameplay balancing (spawn control to avoid overwhelming the player).

🎮 **Play / Download (Windows build):** https://vishalkrishna.itch.io/combat

---

# Combat — DOOM-Style AI FPS Game (Python + Pygame)

A high-performance DOOM-style first-person shooter built in **Python** using **Pygame**, featuring **real-time ray-casting**, **AI-driven enemies**, **shortest-path navigation**, and **dynamic spawn balancing**.

🎮 **Play / Download (Windows Build):**  
https://vishalkrishna.itch.io/combat

---

## Features

### 🔫 Core FPS Gameplay
- DOOM-style first-person movement with smooth mouse-controlled camera rotation  
- Real-time ray-casting renderer for immersive 3D visuals  
- Weapon system with responsive shooting mechanics  
- Health, ammo, and pickups  
- Mini-map with player and enemy tracking  

### 🤖 Enemy AI & Game Balancing
- Enemies navigate the map using **shortest-path algorithms (A* pathfinding)**  
- AI enemies actively **hunt and engage** the player  
- Dynamic spawn balancing prevents too many enemies appearing at once  
- Real-time enemy movement and combat updates  

---

## Controls

| Action | Key |
|------|-----|
| Move Forward | **W** |
| Move Backward | **S** |
| Strafe Left | **A** |
| Strafe Right | **D** |
| Look / Aim | **Mouse** |
| Shoot | **Space** |
| Exit | **Esc** (if enabled) |

> Tip: You can play in fullscreen or windowed mode depending on your system.

---

## Requirements

- **Python 3.11+** (recommended)  
- Windows / macOS / Linux (Windows works best with Pygame)  

Dependencies are listed in `requirements.txt`.

---

## How to Run (Local Development)

### 1) Clone the repository
```bash
git clone https://github.com/Vishal-Krishna-Kumar/Combat-Algo-Game.git
cd Combat-Algo-Game

###2) Create and activate virtual environment

Windows (PowerShell):

py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1


macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3) Install dependencies
pip install -r requirements.txt

4) Run the game
python main.py

Build Windows EXE (Optional)

If you want to create a distributable Windows build:

1) Install PyInstaller
pip install pyinstaller

2) Build the game
pyinstaller --noconfirm --windowed --onedir main.py --add-data "resources;resources"


The executable will be created at:

dist/main/main.exe


If you have additional asset folders such as sounds/, textures/, or sprites/, include them using --add-data.

Project Structure (Typical)
Combat-Algo-Game/
  main.py
  requirements.txt
  resources/
    sounds/
    sprites/
    textures/
  screenshots/

Technical Notes
Raycasting Engine

The game renders a 3D-like world by casting rays from the player’s viewpoint and calculating wall intersections, similar to classic DOOM and Wolfenstein-3D. This approach gives a 3D illusion while remaining highly performant.

Pathfinding & Enemy AI

Enemies use grid-based shortest-path algorithms (A*) to:

Navigate around walls and obstacles

Chase the player intelligently

Avoid getting stuck

Spawn Balancing

The game limits how many enemies can appear at once to prevent unfair gameplay and performance drops.

Troubleshooting
pygame not found

Make sure your virtual environment is active and run:

pip install -r requirements.txt

Textures or sounds not loading

Ensure the resources/ folder exists in the project root.
If using a Windows EXE, include:

--add-data "resources;resources"


when building with PyInstaller.

PowerShell cannot activate venv

Run once:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned


Then:

.\venv\Scripts\Activate.ps1

Roadmap

More enemy types and behaviors

New levels and map editor support

Improved UI (health, ammo, settings)

Browser version (WebAssembly via pygbag)


