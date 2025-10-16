import tkinter as tk
import math, random

x0 = 775
y0 = 650
r = 10

vitesse = 10
angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)

dx = vitesse * math.cos(angle)
dy = vitesse * math.sin(angle)


class Ball:

    def __init__(self, canvas, x, y, rayon):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.rayon = rayon
        self.dx = dx
        self.dy = dy
        self.width = int(canvas["width"])
        self.height = int(canvas["height"])
        self.moving = False

        # Création de la balle
        self.id = canvas.create_oval(self.x - rayon, self.y - rayon, self.x + rayon, self.y + rayon, fill="red", outline="white")

    def deplacement(self):
        # Gestion des collisions
        if self.x + self.rayon + self.dx > self.width:
            self.x = self.width - self.rayon
            self.dx = -self.dx

        if self.x - self.rayon + self.dx < 0:
            self.x = self.rayon
            self.dx = -self.dx

        if self.y + self.rayon + self.dy > self.height:
            self.y = self.height - self.rayon
            self.dy = -self.dy

        if self.y - self.rayon + self.dy < 0:
            self.y = self.rayon
            self.dy = -self.dy
        
        self.x += self.dx
        self.y += self.dy

        if hasattr(self.canvas.master, "Bricks"):

            for brique in self.canvas.master.Bricks:
                bx1, by1, bx2, by2 = self.canvas.coords(brique.rect)
                xb1 = self.x - self.rayon
                yb1 = self.y - self.rayon
                xb2 = self.x + self.rayon
                yb2 = self.y + self.rayon

                if xb2 >= bx1 and xb1 <= bx2 and yb2 >= by1 and yb1 <= by2:
                    self.canvas.delete(brique.rect)
                    self.canvas.master.Bricks.remove(brique)
                    self.dy *= -1

        self.canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon,)

        self.canvas.after(20, self.deplacement)


    def move(self):
        if not self.moving:
            self.moving = True
            self.deplacement()


class Brick(tk.Tk):

    def __init__(self, screen, x, y, width, height, color, ball):

        
        self.screen = screen
        self.rect = screen.create_rectangle(x, y, x+width, y+height, fill = color)
        self.object_ball = ball
    


class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1500x800")
        self.title("Casse Brique")

        self.screen = tk.Canvas(self, width=1500, height=800, bg="black")
        self.screen.pack()

        self.object_ball = Ball(self.screen, x0, y0, r)

        labelScore = tk.Label(self, text="Score: ", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        labelScore.place(relx=0.90, rely=0.05)

        labelVie = tk.Label(self, text="Vies: ", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        labelVie.place(relx=0.02, rely=0.05)

        buttonQuit = tk.Button(self, text = 'Quitter' , font = 36, fg ='red', command = self.destroy )
        buttonQuit.place(relx = 0.08, rely = 0.93)

        buttonPlay = tk.Button(self, text = "Jouer", font = 36, fg = "green", command = self.object_ball.move)
        buttonPlay.place(relx = 0.02, rely = 0.93)
        
        self.Bricks = []
        self.showBrick()
    
    def showBrick(self):
        height = 36
        width = 100
        space = 20
        lines = 5
        columns = 10
        color_code = ["red", "orange", "yellow", "green", "cyan"]

        for i in range(lines):
            for j in range(columns):
                x = j * (width + space) + 150
                y = i * (height + space) + 110
                self.Bricks.append(Brick(self.screen, x, y, width, height, color_code[i], self.object_ball))
            


    
window = MyWindow()
window.mainloop()
