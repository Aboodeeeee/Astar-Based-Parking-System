import tkinter as tk
from tkinter import messagebox
import numpy as np
import heapq

# [Previous imports and ParkingSystem class code remains the same until park_vehicle method]
class ParkingSystem:
    def __init__(self, rows=4, cols=4):
        self.rows = max(5, rows) * 2 + 1
        self.cols = max(4, cols) * 2 + 1
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.vehicles = {}  # {(row, col): vehicle_type}
        self.dedicated_slots = {
            'ev': [],      # Will store coordinates of EV slots
            'truck': []    # Will store coordinates of truck slots
        }
        self.setup_layout()
        self.setup_dedicated_slots()

    def setup_layout(self):
        self.entrance = (0, self.cols // 2)
        self.grid[0, self.cols // 2] = 2

        for row in range(1, self.rows):
            for col in range(self.cols):
                if row == 1:
                    self.grid[row, col] = 0
                elif row > 1:
                    if row % 2 == 0 and col % 2 == 0:
                        self.grid[row, col] = 3
                    else:
                        self.grid[row, col] = 0

    def setup_dedicated_slots(self):
        # Find all parking slots
        parking_slots = [(r, c) for r in range(self.rows) for c in range(self.cols) 
                        if self.grid[r, c] == 3]
        
        # Updated positions for EV slots
        ev_positions = [(10, 6), (10, 8), (8, 8)]  # Updated EV positions
        for pos in ev_positions:
            if pos[0] < self.rows and pos[1] < self.cols:
                self.dedicated_slots['ev'].append(pos)
                self.grid[pos[0], pos[1]] = 3
        
        # Positions for truck slots remain the same
        truck_positions = [(2, 0), (2, 2)]
        for pos in truck_positions:
            if pos[0] < self.rows and pos[1] < self.cols:
                self.dedicated_slots['truck'].append(pos)
                self.grid[pos[0], pos[1]] = 3

    def is_valid_slot(self, pos, vehicle_type):
        if vehicle_type == 'ev':
            return pos in self.dedicated_slots['ev'] and self.grid[pos[0], pos[1]] == 3
        elif vehicle_type == 'truck':
            return pos in self.dedicated_slots['truck'] and self.grid[pos[0], pos[1]] == 3
        else:  # Regular car can park in non-dedicated slots
            return (pos not in self.dedicated_slots['ev'] and 
                   pos not in self.dedicated_slots['truck'] and 
                   self.grid[pos[0], pos[1]] == 3)

    def toggle_slot(self, row, col):
        pos = (row, col)
        
        # If the slot is occupied by a vehicle
        if pos in self.vehicles:
            self.grid[row, col] = 3  # Change back to empty parking slot
            del self.vehicles[pos]    # Remove the vehicle
            return
            
        # For dedicated EV slots
        if pos in self.dedicated_slots['ev']:
            if self.grid[row, col] == 3:
                self.grid[row, col] = -1  # Block the slot
            elif self.grid[row, col] == -1:
                self.grid[row, col] = 3   # Unblock the slot
            return
            
        # For dedicated truck slots
        if pos in self.dedicated_slots['truck']:
            if self.grid[row, col] == 3:
                self.grid[row, col] = -1  # Block the slot
            elif self.grid[row, col] == -1:
                self.grid[row, col] = 3   # Unblock the slot
            return
            
        # For regular parking slots
        if self.grid[row, col] == 3:
            self.grid[row, col] = -1  # Block the slot
        elif self.grid[row, col] == -1:
            self.grid[row, col] = 3   # Unblock the slot

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        row, col = pos
        neighbors = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r, c] in [0, 3]:
                neighbors.append((r, c))
        return neighbors

    def a_star(self, start, target=None, vehicle_type=None):
        empty_spots = [(r, c) for r in range(self.rows) for c in range(self.cols) 
                      if self.grid[r, c] == 3 and self.is_valid_slot((r, c), vehicle_type)]
        
        if not empty_spots:
            return None
            
        if target is None:
            target = min(empty_spots, key=lambda pos: self.heuristic(pos, start))

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]
            if current == target:
                break
            for next_pos in self.get_neighbors(current):
                new_cost = cost_so_far[current] + (2 if self.grid[next_pos] == 3 else 1)
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(target, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        if target not in came_from:
            return None

        path = []
        current = target
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def park_vehicle(self, start, vehicle_type):
        path = self.a_star(start, vehicle_type=vehicle_type)
        if not path:
            return None, 0
        final_pos = path[-1]
        self.grid[final_pos[0], final_pos[1]] = 1
        self.vehicles[final_pos] = vehicle_type
        return final_pos, len(path) - 1  # Subtract 1 to exclude the starting position

class ParkingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Parking System (A* Pathfinding)")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Park Car 🚗", command=lambda: self.park_vehicle('car')).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Park EV ⚡", command=lambda: self.park_vehicle('ev')).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Park Truck 🚛", command=lambda: self.park_vehicle('truck')).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Reset (C)", command=self.reset_map).pack(side=tk.LEFT, padx=5)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.buttons = []
        self.parking = None
        self.create_lot()
        
        # Bind 'C' key to reset functionality
        self.root.bind('c', lambda event: self.reset_map())
        self.root.bind('C', lambda event: self.reset_map())
    def create_lot(self):
        rows, cols = 4, 4
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons.clear()
        self.parking = ParkingSystem(rows, cols)

        for i in range(self.parking.rows):
            button_row = []
            for j in range(self.parking.cols):
                btn = tk.Button(self.grid_frame, width=3, height=1, command=lambda r=i, c=j: self.toggle_slot(r, c))
                btn.grid(row=i, column=j, padx=1, pady=1)
                button_row.append(btn)
            self.buttons.append(button_row)

        self.update_display()

    def toggle_slot(self, row, col):
        self.parking.toggle_slot(row, col)
        self.update_display()

    def reset_map(self):
        self.create_lot()
        messagebox.showinfo("Reset", "Parking lot has been reset to default state!")

    def park_vehicle(self, vehicle_type):
        if not self.parking:
            messagebox.showerror("Error", "Create parking lot first")
            return

        path = self.parking.a_star(self.parking.entrance, vehicle_type=vehicle_type)
        if not path:
            messagebox.showerror("Error", f"No available {vehicle_type.upper()} parking spaces")
            return

        final_pos, travel_cost = self.parking.park_vehicle(self.parking.entrance, vehicle_type)
        self.animate_path(path)

        messagebox.showinfo("Success", 
                          f"{vehicle_type.upper()} parked!\n" +
                          f"Travel distance: {travel_cost} cells")
    def animate_path(self, path):
        original_colors = {}
        for pos in path:
            original_colors[pos] = self.buttons[pos[0]][pos[1]].cget('bg')

        for pos in path:
            self.buttons[pos[0]][pos[1]].configure(bg='yellow')
            self.root.update()
            self.root.after(200)
            if pos != path[-1]:
                self.buttons[pos[0]][pos[1]].configure(bg=original_colors[pos])

        self.update_display()

    def update_display(self):
        colors = {
            -1: ('black', 'X'),
            0: ('#d3d3d3', ''),
            2: ('#008000', 'E'),
            3: ('#90EE90', 'P'),
        }

        for i in range(self.parking.rows):
            for j in range(self.parking.cols):
                pos = (i, j)
                value = self.parking.grid[i, j]
                
                if pos in self.parking.vehicles:
                    vehicle_type = self.parking.vehicles[pos]
                    if vehicle_type == 'truck':
                        color, text = '#C4A484', '🚛'
                    elif vehicle_type == 'ev':
                        color, text = '#ADD8E6', '⚡'
                    else:
                        color, text = '#FF6961', '🚗'
                elif pos in self.parking.dedicated_slots['ev']:
                    if value == -1:
                        color, text = 'black', 'X'
                    else:
                        color, text = '#E6E6FA', 'P⚡'  # Light purple for EV slots
                elif pos in self.parking.dedicated_slots['truck']:
                    if value == -1:
                        color, text = 'black', 'X'
                    else:
                        color, text = '#FFE4C4', 'P🚛'  # Light orange for truck slots
                else:
                    color, text = colors[value]
                
                self.buttons[i][j].configure(bg=color, text=text)

    def run(self):
        self.root.mainloop()

    # [Rest of the ParkingGUI class remains the same]

if __name__ == "__main__":
    app = ParkingGUI()
    app.run()