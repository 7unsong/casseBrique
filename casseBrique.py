import tkinter as tk
import math, random

width = 1920
height = 1080

x0 = 775
y0 = 650
r = 10

vitesse = 1
angle = random.uniform(0,2*math.pi)

dx = vitesse*math.cos(angle)
dy = vitesse*math.sin(angle)



class MyWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        self.geometry("1920x1080")

        self.title("Casse Brique")

        self.screen = tk.Canvas(self, width = 1920, height = 1080, bg = "black")
        self.screen.pack()

        labelScore = tk.Label(self, text = "Score: ", bg = "black", font = ("Arial", 15, "bold"), fg = "yellow")
        labelScore.place(relx = 0.90, rely = 0.05)

        labelVie = tk.Label(self, text = "Vies: ", bg = "black", font = ("Arial", 15, "bold"), fg ="yellow")
        labelVie.place(relx = 0.02, rely = 0.05)

        buttonQuit = tk.Button(self, text = "Quitter", font = 36, fg = "red", command = self.destroy)
        buttonQuit.place(relx = 0.08, rely = 0.93)

        buttonPlay = tk.Button(self, text = "Jouer", font = 36, fg = "green", command = self.spawn)
        buttonPlay.place(relx = 0.02, rely = 0.93)


    def spawn(self):
        r = 10
        x = 775
        y = 650
        self.screen.create_oval(x-r, y-r, x+r, y+r, fill = "red", outline = "white")
        self.deplacement
    
    def deplacement(self):
        global x0, y0, dx, dy

        if x0 + r + dx > width:
            x0 = 2*(width - r) - x0
            dx = -dx

        if x0 - r + dx < 0:
            x0 = 2*r - x0
            dx = -dx
    
        if y0 + r + dy > height:
            y0 = 2*(height - r) - y0
            dy = - dy
    
        if y0 - r + dy < 0:
            y0 = 2*r - y0
            dy = -dy
    
        self.screen.coords(self.spawn, x0-r, y0-r , x0+r, y0+r)
        

        self.after(20, self.deplacement)

    
window = MyWindow()
window.mainloop()