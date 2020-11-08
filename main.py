from tkinter import *
from tkinter import ttk
from time import sleep

from gameoflife import GameOfLife, SHAPES

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
        # self.res = self.res_slider.get()
        # Pack.
        self.frame.pack(expand=YES)
        self.frame_sim.grid(pady=40, row=0, column=1, sticky=N)
        self.frame_time.pack(expand=YES)
        # self.window.bind("<MouseWheel>",self.zoom).

        # Core.
        self.core = GameOfLife(113, 113)

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
        # # Slider.
        # self.create_slider()
    
    def create_title(self):
        self.title = Label(self.frame, text="Welcome to cell life")
        self.title.grid(row=0, column=1, sticky=N)

    def create_start_button(self):
        self.start_button = Button(self.frame_sim, text="Start/Stop")
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
        self.show_grid = Checkbutton(self.frame_sim, variable=self.check_value, command=self._draw_grid)
        self.show_grid.pack()

    # def create_slider(self):
    #     """ Deactivate for a time"""
    #     self.res_slider = Scale(self.frame_sim ,label="Resolution", orient=HORIZONTAL, from_=58, to=2, resolution=4, command=self._draw_grid)
    #     self.res_slider.set(24)
    #     self.res_slider.pack()

    def create_canvas(self):
        self.size = 8
        self.canvas = Canvas(self.frame, bg='white', width=(self.size*113+2), height=(self.size*113+2),  bd=0, highlightthickness=0)
        # self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        # self.front_canvas = Canvas(self.canvas)
        # self.front_canvas.pack(expand=YES)
        self.canvas.grid(row=0, column=0)
    
    def create_combobox(self):
        self.shapes = sorted(list(SHAPES.keys()))
        self.combo = ttk.Combobox(self.frame_sim, state="readonly", values=self.shapes)
        self.combo.current(1)
        self.combo.pack()
        # Chaque choix de combobox appel la methode sombo_selected.
        self.combo.bind("<<ComboboxSelected>>", self.combo_selected)

    def combo_selected(self, event):
        # recupere le choix de l'utilisateur.
        choice = str(self.combo.get())
        print(f"choice= {choice}")
        print(SHAPES[choice])
        # Definit la position de depart du jeu de la vie grave au combobox.
        self.init_simulation(SHAPES[choice])
    
    def init_simulation(self, shape):
        self.core._start_pos(shape)
        self.cells = shape
        self.draw_cells()

    # def zoom(self, event):
    #     if event.delta>0:
    #         print("ZOOM IN!")
    #         print(self.canvas.children)
    #         self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
    #     elif event.delta<0:
    #         print("ZOOM OUT!")
    #         self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
    #     self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _draw_grid(self):
        show_grid = self.check_value.get()
        # Clear canvas
        self.canvas.delete('all')
        self.draw_cells()

        if show_grid:
            self._draw_lines(self.size)
    
    def _draw_lines(self, size):
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        stepX = 2
        while stepX < width + self.size :
            self.canvas.create_line(stepX, 0, stepX, height, width=1, fill='black')
            stepX += self.size
        stepY = 2
        while stepY < height + self.size:
            self.canvas.create_line(0, stepY, width, stepY, width=1, fill='black')
            stepY += self.size
        # centerX = int(width/2)
        # centerY = int(height/2)
        # stepX = centerX - (self.size/2)
        # while stepX < width*4:
        #     self.canvas.create_line(stepX, -(height*4), stepX, height*4, width=1, fill='black')
        #     self.canvas.create_line(width-stepX, -(height*4), width-stepX, height*4, width=1, fill='black')
        #     stepX += self.size
        # stepY = centerY - (self.size/2)
        # while stepY < height*4:
        #     self.canvas.create_line(-(width*4), stepY, width*4, stepY, width=1, fill='black')
        #     self.canvas.create_line(-(width*4), height-stepY, width*4, height-stepY, width=1, fill='black')
        #     stepY += self.size

    def draw_cells(self):
        self.cells = SHAPES[str(self.combo.get())]
        print(f"cells = {self.cells}")
        for cell in self.cells:
            self._draw_cell(cell)

    def _draw_cell(self, pos):
        """how to draw a cell, it's juste a test"""
        pos_x = (pos[1] * self.size+2)
        pos_y = (pos[0] * self.size+2)
        self.canvas.create_rectangle(pos_x, pos_y, pos_x+self.size, pos_y+self.size, fill='black')
    
    def update_canvas(self, *args):
        print(args)

APP = Interface()
APP.window.mainloop()