# Clash City

A simple tower-defense–like prototype built with **Pygame**.
The player builds up a base, places buildings, and defends the **Town Hall** against waves of incoming enemies.

This project is experimental and was mainly created for testing game mechanics in Python.

---

## Features

* Fullscreen Pygame window
* Placeable buildings and walls with resource costs
* Upgradable Town Hall unlocking more defenses
* Enemies spawn in two modes:

  * **Progressive Mode** – enemies get faster and stronger over time
  * **Wave Mode** – enemies spawn in structured waves
* Health bars and money/resource system
* Basic UI with stats, resources, and a quit button
* End-game screen when the Town Hall is destroyed

---

## Controls

* **Arrow Up / Down** – Change terrain
* **F1** – Toggle HP display
* **Backspace** – Sell/remove a building
* **Space** – Upgrade Town Hall (if enough resources)
* **Q / W / E** – Select building type (Barrack, Wall, Mine)
* **0 / D / Escape** – Deselect building
* **Delete / End** – Quit the game
* **Mouse Left-Click** – Place building / interact
* **Top-right X button** – Quit

---

## Requirements

* [Python 3.x](https://www.python.org/downloads/)
* [Pygame](https://www.pygame.org/download.shtml)

Install dependencies via pip:

```bash
pip install pygame
```

---

## Running the Game

Run the main script:

```bash
python main.py
```

At startup you’ll be asked:

* Press **Enter** → Progressive mode
* Type `wave` + Enter → Wave mode

---

## Notes

* This is a **prototype** project and not a finished game.
* Some building/unit types are commented out in the code.
* No menus, audio, or save/load support.

---
