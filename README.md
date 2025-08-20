# Smart Parking System with A* Pathfinding

A Python GUI application that uses A* pathfinding to find optimal routes to available parking spots. Built with Tkinter and supports multiple vehicle types with dedicated parking zones.

## Features

- **A* Pathfinding**: Automatically finds shortest path to nearest parking spot
- **Multiple Vehicle Types**: Cars (cyan), EVs (blue), Trucks (brown)
- **Dedicated Zones**: Bottom-right for EVs, top-left for trucks
- **Interactive GUI**: Click to park vehicles or toggle slot availability
- **Visual Animation**: Shows pathfinding route in real-time

## Requirements

```
Python 3.6+
numpy
tkinter (included with Python)
```

## Installation & Usage

1. Clone and run:
```bash
git clone https://github.com/yourusername/smart-parking-system.git
cd smart-parking-system
pip install numpy
python parking_system.py
```

2. Use the GUI:
   - **Park Car/EV/Truck**: Automatically finds and parks vehicle with ID (c1, ev1, t1...)
   - **Remove Vehicle**: Enter vehicle ID to remove
   - **Click parking slots**: Toggle between available/blocked

## How it Works

- Grid layout with driving lanes (gray) and parking spots (blue)
- A* algorithm finds optimal path from entrance (green) to nearest spot
- Vehicle IDs are displayed on occupied spots
- Blocked slots (black) are not accessible

## Visual Guide

- 🟢 Green: Entrance
- 🔵 Light Blue: Available spots  
- 🔘 Gray: Driving lanes
- ⬛ Black: Blocked areas
- Vehicle colors show occupied spots with IDs

## Customization

Change lot size in `create_lot()`:
```python
rows = 6  # Default: 4
cols = 6  # Default: 4
```

## License

MIT License - Feel free to use and modify!
