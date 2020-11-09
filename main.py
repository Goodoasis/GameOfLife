from tkinter import *
from tkinter import ttk
from time import sleep

from gameoflife import GameOfLife

SHAPES = {
    "clear": [],
    "blinker": [(10, 22), (10, 23), (10, 24)],
    "row10": [(10, 18), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23), (10, 24), (10, 25), (10, 26), (10, 27)],
    "ship": [(18, 3), (18, 4), (18, 5), (19,5), (20,4)]
}

class Interface():

    def __init__(self):
        self.window = Tk()
        self.window.title = "Game of Life"
        self.window.geometry("1100x950")
        self.window.config(background='brown')
        # Init frames.
        self.frame = Frame(self.window, bg='red')
        self.frame_sim = Frame(self.frame, bg='green', border=1)
        self.frame_time = Frame(self.frame_sim, bg="yellow", border=1)
        # Create all of widgets.
        self.create_widgets()
        # Class Variables.
        self.size = 8
        # Pack.
        self.frame.pack(expand=YES)
        self.frame_sim.grid(pady=40, row=0, column=1, sticky=N)
        self.frame_time.pack(expand=YES)
        # Core.
        self.core = GameOfLife(113, 113)
        self.cells = []

    def create_widgets(self):
        # Labels.
        self.create_title()
        # Buttons.
        self.create_start_button()
        self.create_next_button()
        self.create_prev_button()
        self.create_quit_button()
        # CheckButton
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
        self.start_button = Button(self.frame_sim, text="Start/Pause", command=self.printo)
        self.start_button.pack()

    def create_prev_button(self):
        self.prev_button = Button(self.frame_time, text="<")
        self.prev_button.grid(padx=3, row=0, column=0)

    def create_next_button(self):
        self.next_button = Button(self.frame_time, text=">")
        self.next_button.grid(padx=3, row=0, column=1)

    def create_quit_button(self):
        self.quit_button = Button(self.frame_sim, text="Quit", command=self.window.quit)
        self.quit_button.pack(side=BOTTOM)

    def create_check_grid(self):
        self.show_grid = Checkbutton(self.frame_sim, variable=self.check_value, command=self.update_canvas)
        self.show_grid.pack()

    def create_canvas(self):
        self.size = 8
        self.canvas = Canvas(self.frame, bg='white', width=(self.size*113+2), height=(self.size*113+2),  bd=1, highlightthickness=1)
        # self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.mouse_click)
        # self.canvas.bind("<Space>", self.startanim)

    def create_combobox(self):
        self.shapes = [i.capitalize() for i in list(SHAPES.keys())]
        self.combo = ttk.Combobox(self.frame_sim, state="readonly", values=self.shapes)
        self.combo.current(0)
        self.combo.pack()
        # Chaque choix de combobox met a jours le canvas.
        self.combo.bind("<<ComboboxSelected>>", self.update_canvas)

    def mouse_click(self, event):
        # Increment de 3px for increase accuracy.
        mouseX = event.x-3
        mouseY = event.y-3
        # Divid by size of cellule for translate in position in cellule case.
        cellX = int(mouseX / self.size)
        cellY = int(mouseY / self.size)
        click_pos = (cellY, cellX)
        # Si la position n'est pas dans la liste des cellules vivantes:
        if click_pos not in self.cells:
            self._draw_cell(click_pos)
        else:
            # Sinon on la redessine mais en blanc
            self._draw_cell(click_pos, False)
        # Puis on met a jours la liste des cellules vivante.
        self.update_cells()
    
    def _draw_grid(self):
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

    def draw_cells(self):
        # self.cells contient tout les vivantes a dessiner.
        self.cells = SHAPES[str(self.combo.get()).lower()]
        # Initalisation de deux lsite qui permette de mettre à jours self.cells.
        self.new_cells = []
        self.dead_cells = []
        # Dessine chaque cellule de self.cells
        for cell in self.cells:
           self._draw_cell(cell)
        # Apres avoir dessiné
        self.update_cells()
    
    def update_cells(self):
        # Supprime de self.cells toutes celle qui sont mortes
        for cell in self.dead_cells:
            self.cells.remove(cell)
        # On ajoute tout les nouvelles cellules.
        for cell in self.new_cells:
            if cell not in self.cells:
                self.cells.append(cell)
        self.new_cells.clear()
        self.dead_cells.clear()

    def _draw_cell(self, pos, alive=True):
        """Draw a square (self.size X self.size) with position in arg."""
        self.new_cells = []
        self.dead_cells = []
        pos_x = (pos[1] * self.size+2)
        pos_y = (pos[0] * self.size+2)
        # Si on dessine une cellule vivante:
        if alive:
            color = 'black'
            self.new_cells.append(pos)
        else: 
            # Sinon:
            color = 'white'
            self.dead_cells.append(pos)
        self.canvas.create_rectangle(pos_x, pos_y, pos_x+self.size, pos_y+self.size, fill=color)

    def update_canvas(self, event=None):
        # Clear canvas before.
        self.canvas.delete('all')
        # Draw grid if chech button is cheked.
        if self.check_value.get():
            self._draw_grid()
        choice = str(self.combo.get()).lower()
        # Definit la position de depart du jeu de la vie grave au combobox.
        self.draw_cells()
    
    def printo(self):
        print(f"cells = {self.cells}")

APP = Interface()
APP.window.mainloop()