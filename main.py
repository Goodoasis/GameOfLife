from tkinter import *

class Cellife():
    """[summary]
    """
    def __init__(self):
        """[summary]
        """
        self.window = Tk()
        self.window.title = "Cel*life"
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

    def create_widgets(self):
        # Labels.
        self.create_title()
        # Buttons.
        self.create_start_button()
        self.create_next_button()
        self.create_prev_button()
        self.create_quit_button()
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
        self.next_button = Button(self.frame_time, text=">")
        self.next_button.grid(padx=3, row=0, column=1)

    def create_quit_button(self):
        self.quit_button = Button(self.frame_sim, text="Quit", command=self.window.quit)
        self.quit_button.pack(side=BOTTOM)

    def create_slider(self):
        self.res_slider = Scale(self.frame_sim ,label="Resolution", orient=HORIZONTAL, from_=70, to=5, resolution=5, command=self._draw_grid)
        self.res_slider.set(25)
        self.res_slider.pack()

    def create_canvas(self):
        self.canvas = Canvas(self.frame, bg='white', width=900, height=900)
        self.canvas.grid(row=0, column=0)

    def _draw_grid(self, slider_value):
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        # Clear canvas
        self.canvas.delete('all')
        # Draw lines horizontals then verticals.
        step_x = 0
        while step_x < width:
            self.canvas.create_line(step_x, 0, step_x, height, width=1, fill='black')
            step_x += int(slider_value)
        step_y = 0
        while step_y < height:
            self.canvas.create_line(0, step_y, width, step_y, width=1, fill='black')
            step_y += int(slider_value)

if __name__ == "__main__":
    APP = Cellife()
    APP.window.mainloop()