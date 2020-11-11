import os
import pprint
import json
from tkinter import *
from tkinter import ttk
from time import sleep

from gameoflife import GameOfLife

class Interface():

    def __init__(self):
        self.window = Tk()
        self.window.title = "Game of Life"
        self.window.geometry("1100x950")
        self.window.config(background='brown')
        # Init variables.
        self.variables()
        # Init frames.

        self.frame = Frame(self.window, bg='red')
        self.frame_sim = Frame(self.frame, bg='green', border=1)
        self.frame_time = Frame(self.frame_sim, bg="yellow", border=1)
        # Create all of widgets.
        self.create_widgets()
        # Pack.
        self.frame.pack(expand=YES)
        self.frame_sim.grid(pady=40, row=0, column=1, sticky=N)
        self.frame_time.pack(expand=YES)
        # Core.
        self.core = GameOfLife(113, 113)
        # Save shape

    def quit(self):
        self._save_shapes()
        self.window.quit()

    def load_shapes(self):
        _json = "shapes.json"
        with open(_json, "r") as f:
            json_content = json.load(f)
        for key, v in json_content.items():
            self.SHAPES[key] = [tuple(i) for i in v]

    def _save_shapes(self):
        _json = "shapes.json"
        with open(_json, "w") as f:
            json.dump(self.SHAPES, f, indent=4)
    
    def variables(self):
        self.SHAPES = {}
        self.load_shapes()
        self.size = 8
        self.cellule_canvas = 904 / self.size
        # Main liste of alive cells. 
        self.cells = []
        # Sub-lists for born and dead cell for update self.cells.
        self.dead_cells = []
        self.new_cells = []

    def create_widgets(self):
        # Labels.
        self.create_title()
        # Buttons.
        self.create_start_button()
        self.create_next_button()
        self.create_prev_button()
        self.create_add_custom_button()
        self.create_remove_custom_button()
        self.create_quit_button()
        # CheckButton.
        self.check_value = BooleanVar()
        self.create_check_grid()
        # Canvas.
        self.create_canvas()
        # ComboBox.
        self.create_combobox()
    
    def create_title(self):
        self.title = Label(self.frame, text="Welcome to cell life")
        self.title.grid(row=0, column=1, sticky=N)

    def create_start_button(self):
        self.start_button = Button(self.frame_sim, text="Start/Pause", command=self.startEvolution)
        self.start_button.pack()

    def create_prev_button(self):
        self.prev_button = Button(self.frame_time, text="<")
        self.prev_button.grid(padx=3, row=0, column=0)

    def create_next_button(self):
        self.next_button = Button(self.frame_time, text=">")
        self.next_button.grid(padx=3, row=0, column=1)

    def create_add_custom_button(self):
        self.start_button = Button(self.frame_sim, text="Add this shape", command=self.add_custom)
        self.start_button.pack()

    def create_remove_custom_button(self):
        self.start_button = Button(self.frame_sim, text="Remove selected shape", command=self.remove_custom)
        self.start_button.pack()
    
    def add_custom(self):
        new_shape = self.cells[:]
        shape_index = len(self.SHAPES) - 4
        if shape_index < 9:
            name = f"Custom n°{shape_index+1}"
            self.SHAPES[name] = new_shape
            self.update_combobox()

    def remove_custom(self):
        selected = self.combo.get()
        if "Custom" in selected:
            self.SHAPES.pop(selected)
            self.update_combobox()
            
    def create_quit_button(self):
        self.quit_button = Button(self.frame_sim, text="Quit", command=self.quit)
        self.quit_button.pack(side=BOTTOM)

    def create_check_grid(self):
        self.show_grid = Checkbutton(self.frame_sim, variable=self.check_value, command=self.update_canvas)
        self.show_grid.pack()

    def create_canvas(self):
        self.canvas = Canvas(self.frame, width=(self.size*self.cellule_canvas+2), height=(self.size*self.cellule_canvas+2))
        self.canvas.config(bg='white', bd=1, highlightthickness=1)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.mouse_click)

    def create_combobox(self):
        combo_shapes = list(self.SHAPES.keys())
        self.combo = ttk.Combobox(self.frame_sim, state="readonly", values=combo_shapes)
        self.combo.current(0)
        self.combo.pack()
        # Each combobox event update self.cells.
        self.combo.bind("<<ComboboxSelected>>", self.set_combo)
    
    def update_combobox(self):
        combo_shapes = list(self.SHAPES.keys())
        self.combo.config(values=combo_shapes)
        self.combo.pack()
    
    def set_combo(self, event):
        """ Methode called by a change on ComboBox.
        self.cell is clear for set this choice. """
        # et current ComboBox value.
        choice = self.combo.get()
        self.cells.clear()
        # Update self.cells
        for pos in self.SHAPES[choice]:
            self.manage_cells(pos)
        self.update_canvas()

    def _draw_grid(self):
        """ Methode who draw lines and rows in accordance to self.size. """
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        # Increment 2px for see the first line on canvas limits.
        stepX = 2
        while stepX < width + self.size :
            self.canvas.create_line(stepX, 0, stepX, height, width=1, fill='grey')
            stepX += self.size
        stepY = 2
        while stepY < height + self.size:
            self.canvas.create_line(0, stepY, width, stepY, width=1, fill='grey')
            stepY += self.size

    def mouse_click(self, event):
        """ Methode for add ou remove a cell directly by a mouse click in canvas. """
        # Increment de 3px for increase accuracy.
        mouseX = event.x-3
        mouseY = event.y-3
        # Divid by size of cellule for translate in position in cellule case.
        cellX = int(mouseX / self.size)
        cellY = int(mouseY / self.size)
        click_pos = (cellY, cellX)
        self.manage_cells(click_pos)

    def manage_cells(self, pos):
        """ Check if cell in arg already exists for sort cell. """
        if pos not in self.cells:
            self.new_cells.append(pos)
        else:
            self.dead_cells.append(pos)
        self.update_cells()
    
    def update_cells(self):
        # On ajoute toutes les nouvelles cellules.
        for cell in self.new_cells:
            if cell not in self.cells:
                self.cells.append(cell)
        # Supprime de self.cells toutes celles qui sont mortes.
        for cell in self.dead_cells:
            self.cells.remove(cell)
        self.new_cells.clear()
        self.dead_cells.clear()
        # Met a jours le canvas.
        self.update_canvas()

    def update_canvas(self, event=None):
        """
        Methode who erase canvas.
        Draw grid if CheckButton is True.
        Then draw all cell in self.cells.
        """
        # Clear canvas before.
        self.canvas.delete('all')
        # Draw grid if check button is checked.
        if self.check_value.get():
            self._draw_grid()
        self.draw_cells()

    def draw_cells(self):
        """ Itere self.cells for draw each cell. """
        # Dessine chaque cellule de self.cells.
        for cell in self.cells:
           self.draw_cell(cell)

    def draw_cell(self, pos):
        """ Draw a square with self.size and position in arg tuple(y, x)."""
        pos_x = (pos[1] * self.size+2)
        pos_y = (pos[0] * self.size+2)
        self.canvas.create_rectangle(pos_x, pos_y, pos_x+self.size, pos_y+self.size, fill='black')

    def startEvolution(self, event=None):
        self.core._start_pos(self.cells)
        for i in range(100):
            self.cells = self.core.evolution(self.cells)
            self.update_cells()
            if len(self.cells) == 0:
                break
            self.canvas.update()
            sleep(0.09)


APP = Interface()
APP.window.mainloop()