from tkinter import *

from gameoflife import GameOfLife

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
        self.res = self.res_slider.get()
        # Pack.
        self.frame.pack(expand=YES)
        self.frame_sim.grid(pady=40, row=0, column=1, sticky=N)
        self.frame_time.pack(expand=YES)

        # Core
        self.cells_alive = set()

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
        # Slider.
        self.create_slider()
        # Canvas.
        self.create_canvas()
    
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
        self.next_button = Button(self.frame_time, text=">", command=self.cell)
        self.next_button.grid(padx=3, row=0, column=1)

    def create_quit_button(self):
        self.quit_button = Button(self.frame_sim, text="Quit", command=self.window.quit)
        self.quit_button.pack(side=BOTTOM)

    def create_check_grid(self):
        self.show_grid = Checkbutton(self.frame_sim, variable=self.check_value, command=self._draw_grid)
        self.show_grid.pack()

    def create_slider(self):
        self.res_slider = Scale(self.frame_sim ,label="Resolution", orient=HORIZONTAL, from_=58, to=2, resolution=4, command=self._draw_grid)
        self.res_slider.set(24)
        self.res_slider.pack()

    def create_canvas(self):
        self.canvas = Canvas(self.frame, bg='white', width=800, height=800)
        self.canvas.grid(row=0, column=0)

    def _draw_grid(self, slider_value=None):
        if slider_value == None:
            slider_value = int(self.res_slider.get())
        show_grid = self.check_value.get()
        # Clear canvas
        self.canvas.delete('all')

        if show_grid: self._draw_lines(slider_value)
        # Draw alive cells
        self.draw_cells_alive()
    
    def _draw_lines(self, slider_value):
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        centerX = int(width/2)
        centerY = int(height/2)

        stepX = centerX - (int(int(slider_value)/2))
        while stepX < width:
            self.canvas.create_line(stepX, 0, stepX, height, width=1, fill='black')
            self.canvas.create_line(width-stepX, 0, width-stepX, height, width=0.5, fill='black')
            stepX += int(slider_value)
        stepY = centerY - (int(int(slider_value)/2))
        while stepY < height:
            self.canvas.create_line(0, stepY, width, stepY, width=1, fill='black')
            self.canvas.create_line(0, height-stepY, width, height-stepY, width=0.5, fill='black')
            stepY += int(slider_value)
    
    def draw_cells_alive(self):
        for cell in self.cells_alive:
            self.cell(cell)

    def cell(self, pos=(10,10)):
        """how to draw a cell, it's juste a test"""
        size = self.res_slider.get()
        pos_x = (pos[0] * size) - int(size/2)
        pos_y = (pos[1] * size) - int(size/2)
        self.canvas.create_rectangle(pos_x, pos_y, pos_x+size, pos_y+size, fill='black')
        # add cell in list of alive cell
        self.cells_alive.add(pos)

class Cell():
    def __init__(self, position, size, stat=True):
        self.pos = position
        self.size = size
        self.stat = True
        self.color = 'black'

APP = Interface()
APP.window.mainloop()