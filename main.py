from tkinter import *

class Cellife():
    def __init__(self):
        self.window = Tk()
        self.window.title = "Cel*life"
        self.window.geometry("1100x950")
        self.window.config(background='brown')

        self.frame = Frame(self.window, bg='red')
        self.frame_sim = Frame(self.frame, bg='green', border=1)
        self.frame_time = Frame(self.frame_sim, bg="yellow", border=2)

        # Create all of widgets
        self.create_widgets()

        # pack
        self.frame.pack(expand=YES)
        self.frame_sim.grid(pady=40, row=0, column=1, sticky=N)
        self.frame_time.pack(expand=YES)

    def create_widgets(self):
        # Buttons
        self.create_start_button()
        self.create_next_button()
        self.create_prev_button()
        self.create_quit_button()
        # Labels
        self.create_title()
        # Canvas
        self.create_canvas()
    
    def create_title(self):
        self.title = Label(self.frame, text="Welcome to cell life")
        self.title.grid(row=0, column=1, sticky=N)

    def create_canvas(self):
        self.canvas = Canvas(self.frame, bg='gray', width=900, height=900)
        self.canvas.grid(row=0, column=0)
    
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

if __name__ == "__main__":
    APP = Cellife()
    APP.window.mainloop()