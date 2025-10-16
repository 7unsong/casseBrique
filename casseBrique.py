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

class Brick(tk.Tk):

    

    def __init__(self, screen, x, y, width, height, color):

        self.screen = screen
        self.rect = screen.create_rectangle(x, y, x+width, y+height, fill = color)
    
        if 
        



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
        
        self.Bricks = []
        self.showBrick()




    def showBrick(self):
        height = 35
        width = 100
        space = 20
        lines = 5
        columns = 10
        color_code = ["red", "orange", "yellow", "green", "cyan"]

        for i in range(lines):
            for j in range(columns):
                x = j * (width + space) + 150
                y = i * (height + space) + 110
                self.Bricks.append(Brick(self.screen, x, y, width, height, color_code[i]))
            
    


    
window = MyWindow()
window.mainloop()