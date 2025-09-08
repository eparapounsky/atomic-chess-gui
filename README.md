# Atomic Chess Game
A graphical interface for playing Atomic Chess, written in Python with Tkinter.

## Download Available
Download the game [here](https://github.com/eparapounsky/atomic-chess-gui/releases) (Windows and Mac only)

## Features
- Play Atomic Chess with an intuitive and interactive GUI
- Rule enforcement with instant feedback
- Displays current player and game state
- No installation required for Windows executable

## Rules
- Atomic chess follows standard chess rules with one major exception: captures cause explosions
- When a piece captures another piece, both pieces are destroyed along with all pieces in the 8 adjacent squares
- Pawns are immune to explosions unless they are directly captured or make the capturing move themselves
- Kings cannot make captures because they would explode themselves
- A move that would result in both kings being destroyed is not allowed
- The game ends immediately when a king is destroyed; this counts as a capture

## Preview
<img width="500" height="1615" alt="Screenshot 2025-07-30 125200" src="https://github.com/user-attachments/assets/c1cb015d-17fc-4b02-a5ba-ac4a2168e4ed" />
