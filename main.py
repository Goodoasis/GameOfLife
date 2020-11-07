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
        self.size = 8
        # self.res = self.res_slider.get()
        # Pack.
        self.frame.pack(expand=YES)
        self.frame_sim.grid(pady=40, row=0, column=1, sticky=N)
        self.frame_time.pack(expand=YES)

        # Core
        self.cells_alive = set()
        self.window.bind("<MouseWheel>",self.zoom)

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
        # self.create_slider()
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

    # def create_slider(self):
    #     """ DEactivate for a time"""
    #     self.res_slider = Scale(self.frame_sim ,label="Resolution", orient=HORIZONTAL, from_=58, to=2, resolution=4, command=self._draw_grid)
    #     self.res_slider.set(24)
    #     self.res_slider.pack()

    def create_canvas(self):
        self.canvas = Canvas(self.frame, bg='white', width=900, height=900, xscrollincrement=10, yscrollincrement=10)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.grid(row=0, column=0)
        self.sub_canvas = Canvas(self.canvas, bg='grey', width=800, height=800)
        self.sub_canvas.place(relx=.5, rely=.5, anchor=CENTER)

    def zoom(self, event):
        if event.delta>0:
            print("ZOOM IN!")
            print(self.canvas.children)
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta<0:
            print("ZOOM OUT!")
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _draw_grid(self):
        show_grid = self.check_value.get()
        # Clear canvas
        self.sub_canvas.delete('all')

        if show_grid: self._draw_lines(self.size)
        # Draw alive cells
        self.draw_cells_alive()
    
    def _draw_lines(self, size):
        width = int(self.sub_canvas['width'])
        height = int(self.sub_canvas['height'])
        centerX = int(width/2)
        centerY = int(height/2)

        stepX = centerX - 4
        while stepX < width*4:
            self.sub_canvas.create_line(stepX, -(height*4), stepX, height*4, width=1, fill='black')
            self.sub_canvas.create_line(width-stepX, -(height*4), width-stepX, height*4, width=1, fill='black')
            stepX += self.size
        stepY = centerY - self.size
        while stepY < height*4:
            self.sub_canvas.create_line(-(width*4), stepY, width*4, stepY, width=1, fill='black')
            self.sub_canvas.create_line(-(width*4), height-stepY, width*4, height-stepY, width=1, fill='black')
            stepY += self.size
    
    def draw_cells_alive(self):
        for cell in self.cells_alive:
            self.cell(cell)

    def cell(self, pos=(10,10)):
        """how to draw a cell, it's juste a test"""
        self.size = 8
        pos_x = (pos[0] * self.size)
        pos_y = (pos[1] * self.size)
        self.sub_canvas.create_rectangle(pos_x, pos_y, pos_x+self.size, pos_y+self.size, fill='black')
        # add cell in list of alive cell
        self.cells_alive.add(pos)

class Cell():
    def __init__(self, position, stat=True):
        self.pos = position
        self.stat = True
        self.color = 'black'

APP = Interface()
APP.window.mainloop()