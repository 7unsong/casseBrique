import tkinter as tk
import math, random

width = 1600
height = 720

x0 = width / 2
y0 = 5/6 *  height
r = 10




class Ball:


    def __init__(self, screen, x, y, rayon):

        vitesse = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        dx = vitesse * math.cos(angle)
        dy = vitesse * math.sin(angle)
        

        self.screen = screen
        self.x = x
        self.y = y
        self.rayon = rayon
        self.dx = dx
        self.dy = dy
        self.width = int(screen["width"])
        self.height = int(screen["height"])
        self.vies = 3
        self.moving = False

        


        # Création de la balles
        self.id = screen.create_oval(self.x - rayon, self.y - rayon, self.x + rayon, self.y + rayon, fill="red", outline="white")

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

        if hasattr(self.screen.master, "Bricks"):

            for brique in self.screen.master.Bricks:
                bx1, by1, bx2, by2 = self.screen.coords(brique.rect)
                xb1 = self.x - self.rayon
                yb1 = self.y - self.rayon
                xb2 = self.x + self.rayon
                yb2 = self.y + self.rayon

                if xb1 <= bx2 and xb2 >= bx1 and yb1 <= by2 and yb2 >= by1:

                    self.screen.delete(brique.rect)
                    self.screen.master.Bricks.remove(brique)


                # Détermine le côté de l'impact

                    dist_top = abs(yb2 - by1)
                    dist_bottom = abs(yb1 - by2)
                    dist_left = abs(xb2 - bx1)
                    dist_right = abs(xb1 - bx2)
                    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

                # Inversion selon le côté de contact

                    if min_dist == dist_top or min_dist == dist_bottom:
                        self.dy *= -1
                    else:
                        self.dx *= -1
                    
                    # increment score on main window

                    self.screen.master.score += 100
                    if hasattr(self.screen.master, 'update_score'):
                        self.screen.master.update_score()
                   
                    
                    if len(self.screen.master.Bricks) == 0 and hasattr(self.screen.master, 'win'):
                        self.screen.master.win()
                   
                


        raquette = self.screen.master.object_paddle
        try:
            paddle_x = raquette.x
            paddle_y = raquette.y
            paddle_w = raquette.width
        except AttributeError:
            paddle_x, paddle_y, paddle_x2, paddle_y2 = self.screen.coords(raquette.rect)
            paddle_w = paddle_x2 - paddle_x

        ball_left  = self.x - self.rayon
        ball_right = self.x + self.rayon
        ball_bottom = self.y + self.rayon
        ball_top = self.y - self.rayon

        paddle_left = paddle_x
        paddle_right = paddle_x + paddle_w
        paddle_top = paddle_y

        if ball_right >= paddle_left and ball_left <= paddle_right and ball_bottom >= paddle_top and ball_top < paddle_top:
            self.y = paddle_top - self.rayon 
            self.dy = -self.dy

        if self.y + self.rayon + 10 > self.height:
            self.vies -= 1
            try:
                self.moving = False
                self.x = x0
                self.y = y0
                if hasattr(self.screen.master, 'update_lives'):
                    self.screen.master.update_lives()
                try:
                    if self.vies <= 0 and hasattr(self.screen.master, 'game_over'):
                        self.screen.master.game_over()
                except Exception:
                    pass
            except Exception:
                pass


        self.screen.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon,)

        if self.moving:
            self.screen.after(20, self.deplacement)

    def move(self):
        if not self.moving:
            self.moving = True
            self.deplacement()


class Brick:

    def __init__(self, screen, x, y, width, height, color, ball):
        self.screen = screen
        self.rect = screen.create_rectangle(x, y, x+width, y+height, fill = color)
        self.object_ball = ball
    
class Paddle:

    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 20  # vitesse du déplacement

        # États des touches
        self.moving_left = False
        self.moving_right = False

        # Création de la raquette
        self.paddle = screen.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="grey")

        # Écoute des événements clavier
        self.screen.bind_all("<KeyPress-Left>", self.start_left)
        self.screen.bind_all("<KeyRelease-Left>", self.stop_left)
        self.screen.bind_all("<KeyPress-Right>", self.start_right)
        self.screen.bind_all("<KeyRelease-Right>", self.stop_right)

        # Démarre le déplacement continu
        self.move_continuously()

    def start_left(self, evt):
        self.moving_left = True

    def stop_left(self, evt):
        self.moving_left = False

    def start_right(self, evt):
        self.moving_right = True

    def stop_right(self, evt):
        self.moving_right = False

    def move_continuously(self):

        """Déplacement fluide et continu de la raquette."""
        if self.moving_left and self.x > 0:
            self.x -= self.speed
        if self.moving_right and self.x + self.width < int(self.screen["width"]):
            self.x += self.speed

        # Met à jour la position sur le canvas
        self.screen.coords(self.paddle, self.x, self.y, self.x + self.width, self.y + self.height)

        # Rappelle cette fonction toutes les 20 ms
        self.screen.after(20, self.move_continuously)


class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1500x800")
        self.title("Casse Brique")

        self.screen = tk.Canvas(self, width=1500, height=800, bg="black")
        self.screen.pack()

        self.object_ball = Ball(self.screen, x0, y0, r)
        self.object_paddle = Paddle(self.screen, x0 - 100, y0+35, 200, 15)
        # score
        self.score = 0
        self.labelScore = tk.Label(self, text=f"Score: {self.score}", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        self.labelScore.place(relx=0.90, rely=0.05)

        self.labelVie = tk.Label(self, text=f"Vies: {self.object_ball.vies}", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        self.labelVie.place(relx=0.02, rely=0.05)

        buttonQuit = tk.Button(self, text='Quitter', font=36, fg='red', command=self.destroy)
        buttonQuit.place(relx=0.08, rely=0.93)

        buttonPlay = tk.Button(self, text="Jouer", font=36, fg="green", command=self.object_ball.move)
        buttonPlay.place(relx=0.02, rely=0.93)
        
        self.Bricks = []
        self.showBrick()

    def update_lives(self):
        try:
            self.labelVie.config(text=f"Vies: {self.object_ball.vies}")
        except Exception:
            pass
    
    def update_score(self):
        try:
            self.labelScore.config(text=f"Score: {self.score}")
        except Exception:
            pass

    def win(self):
        try:
            self.object_ball.moving = False
        except Exception:
            pass
        self.screen.create_text(int(self.screen['width'])//2, int(self.screen['height'])//2, text="YOU WIN!", fill="white", font=("Arial", 40, "bold"))

    def game_over(self):
        try:
            self.object_ball.moving = False
        except Exception:
            pass
        self.screen.create_text(int(self.screen['width'])//2, int(self.screen['height'])//2, text="GAME OVER", fill="red", font=("Arial", 40, "bold"))
    
    def showBrick(self):
        height = 30
        width = 72
        space = 5
        lines = 5
        columns = 19
        color_code = ["white", "white", "white", "white", "white"]

        for i in range(lines):
            for j in range(columns):
                x = j * (width + space) + 20
                y = i * (height + space) + 70
                self.Bricks.append(Brick(self.screen, x, y, width, height, color_code[i], self.object_ball))
            

window = MyWindow()
window.mainloop()