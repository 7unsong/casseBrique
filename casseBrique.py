import tkinter as tk
import math, random

width = 1600
height = 800

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

        self.canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon,)

        self.canvas.after(20, self.deplacement)

    def move(self):
        if not self.moving:
            self.moving = True
            self.deplacement()




class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1600x900")
        self.title("Casse Brique")

        self.screen = tk.Canvas(self, width=1600, height=900, bg="black")
        self.screen.pack()

        self.object_ball = Ball(self.screen, x0, y0, r)

        labelScore = tk.Label(self, text="Score: ", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        labelScore.place(relx=0.90, rely=0.05)

        labelVie = tk.Label(self, text="Vies: ", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        labelVie.place(relx=0.02, rely=0.05)

        buttonQuit = tk.Button(self, text="Quitter", font=36, fg="red", command=self.destroy)
        buttonQuit.place(relx=0.08, rely=0.93)

        buttonPlay = tk.Button(self, text="Jouer", font=36, fg="green", command=self.object_ball.move)
        buttonPlay.place(relx=0.02, rely=0.93)


window = MyWindow()
window.mainloop()
