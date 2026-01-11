# DOOM style 3d (raycasting) game in Python (based on Wolfenstein 3d)

Control: 'WASD' + mouse

![doom](/sreenshots/0.jpg)
# Combat — DOOM-Style 3D Raycasting FPS (Python + Pygame)

A DOOM/Wolfenstein-inspired first-person shooter built in **Python** using **Pygame**, featuring a real-time **raycasting engine**, **AI-controlled enemies**, shortest-path navigation (A*/grid pathfinding), and gameplay balancing (spawn control to avoid overwhelming the player).

🎮 **Play / Download (Windows build):** https://vishalkrishna.itch.io/combat

---

## Demo / Screenshots

> Add screenshots here (recommended)

```md

Features
Core FPS Gameplay
Algo Combat -style first-person movement with smooth camera rotation

Real-time raycasting renderer for 3D illusion

Weapon system + shooting mechanics

Health / ammo / pickups (if included in your build)

Mini-map with player + enemy tracking (if enabled)

Enemy AI & Game Balancing
Enemies navigate the map using shortest-path logic (grid-based pathfinding such as A*)

AI behavior designed to chase/engage the player intelligently

Spawn balancing logic prevents too many enemies spawning at once

Real-time updates for enemy movement and combat interaction

Controls
Action	Key
Move Forward	W
Move Backward	S
Strafe Left	A
Strafe Right	D
Look / Aim	Mouse
Shoot	Space
Exit	Esc (if enabled)

Tip: Run the game in fullscreen/windowed depending on your project settings.

Requirements
Python 3.11+ recommended

Windows/macOS/Linux (Windows easiest for Pygame)

Install dependencies from requirements.txt.

How to Run (Local Development)
1) Clone the repository
bash
Copy code
git clone https://github.com/Vishal-Krishna-Kumar/Combat-Algo-Game.git
cd Combat-Algo-Game
2) Create and activate virtual environment
Windows (PowerShell):

powershell
Copy code
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3) Install dependencies
bash
Copy code
pip install -r requirements.txt
4) Run the game
bash
Copy code
python main.py
Build Windows EXE (Optional)
If you want to create a distributable build:

1) Install PyInstaller
bash
Copy code
pip install pyinstaller
2) Build (recommended: folder-based build)
powershell
Copy code
pyinstaller --noconfirm --windowed --onedir main.py --add-data "resources;resources"
The output will be in:

css
Copy code
dist/main/main.exe
If you have other asset folders like sounds/, textures/, sprites/, include them using --add-data.

Project Structure (Typical)
This may vary depending on your files. Update names if needed.

css
Copy code
Combat-Algo-Game/
  main.py
  requirements.txt
  resources/
    sounds/
    sprites/
    textures/
  screenshots/
  ...
Technical Notes (How It Works)
Raycasting Engine
The game renders a 3D-like world by casting rays from the player’s viewpoint across the screen and computing wall intersections. This allows DOOM/Wolfenstein-style visuals while remaining computationally efficient.

Pathfinding / Enemy AI
Enemies move using shortest-path logic over a grid-based representation of the map. This helps them:

Navigate around walls/obstacles

Approach the player strategically

Avoid getting stuck

Spawn Balancing
To keep gameplay fair and performant, spawn logic caps how many enemies can appear in a region at once. This avoids “enemy flooding” while maintaining challenge.

Troubleshooting
1) pygame not found
Make sure venv is activated and dependencies installed:

bash
Copy code
pip install -r requirements.txt
2) Game runs but textures/sounds missing
Make sure resources/ exists in the project root and paths are correct.
If using a PyInstaller EXE, include --add-data "resources;resources" in the build command.

3) PowerShell can’t activate venv
Run once:

powershell
Copy code
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
Then:

powershell
Copy code
.\venv\Scripts\Activate.ps1
Roadmap (Optional)
More enemy types / behaviors

New levels and map editor support

Improved UI (health/ammo, settings)

Browser build (WASM) via pygbag (experimental)
