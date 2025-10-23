import tkinter as tk
import math, random
from PIL import Image, ImageTk

width = 1500
height = 800

x0 = width / 2
y0 = 5/6 * height
r = 10

class Ball:
    def __init__(self, screen, x, y, rayon):
        self.screen = screen
        self.x = x
        self.y = y
        self.rayon = rayon
        vitesse = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        self.dx = vitesse * math.cos(angle)
        self.dy = vitesse * math.sin(angle)
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

        if self.y - self.rayon + self.dy < 0:
            self.y = self.rayon
            self.dy = -self.dy


        self.x += self.dx
        self.y += self.dy

        # brick collisions
        if hasattr(self.screen.master, "Bricks"):
            for brique in list(self.screen.master.Bricks):


                bx1 = brique.x
                by1 = brique.y
                bx2 = brique.x + brique.width
                by2 = brique.y + brique.height

                xb1 = self.x - self.rayon
                yb1 = self.y - self.rayon
                xb2 = self.x + self.rayon
                yb2 = self.y + self.rayon

                if xb2 >= bx1 and xb1 <= bx2 and yb2 >= by1 and yb1 <= by2:

                    # remove brick

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
                   
                


        # paddle collision
        paddle = getattr(self.screen.master, 'object_paddle', None)
        if paddle is not None:
            paddle_x = getattr(paddle, 'x', None)
            paddle_y = getattr(paddle, 'y', None)
            paddle_w = getattr(paddle, 'width', None)
            if paddle_x is None:
                try:
                    paddle_x, paddle_y, px2, py2 = self.screen.coords(paddle.paddle)
                    paddle_w = px2 - paddle_x
                except Exception:
                    paddle_x = 0
                    paddle_y = self.height
                    paddle_w = 0

            ball_left = self.x - self.rayon
            ball_right = self.x + self.rayon
            ball_bottom = self.y + self.rayon
            ball_top = self.y - self.rayon

            paddle_left = paddle_x
            paddle_right = paddle_x + paddle_w
            paddle_top = paddle_y

            if ball_right >= paddle_left and ball_left <= paddle_right and ball_bottom >= paddle_top and ball_top < paddle_top:
                self.y = paddle_top - self.rayon
                self.dy = -self.dy

        # fallen below bottom
        if self.y + self.rayon + 10 > self.height:
            self.vies -= 1
            # stop and reset
            self.moving = False
            self.x = x0
            self.y = y0
            # reset velocity
            vitesse = 10
            angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
            self.dx = vitesse * math.cos(angle)
            self.dy = vitesse * math.sin(angle)
            # reset paddle center if available
            paddle.set_x(x0 - paddle.width/2)
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


            # update lives and check game over
            if hasattr(self.screen.master, 'update_lives'):
                self.screen.master.update_lives()
            if self.vies <= 0 and hasattr(self.screen.master, 'game_over'):
                self.screen.master.game_over()


        # update ball canvas coords
        self.screen.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)

        # schedule next frame
        if self.moving:
            self.screen.after(20, self.deplacement)

    def move(self, evt=None):
        win_flag = getattr(self.screen.master, 'has_won', False)
        over_flag = getattr(self.screen.master, 'is_game_over', False)
        if not (self.moving or win_flag or over_flag):
            self.moving = True
            self.deplacement()


class Brick:
    
    def __init__(self, screen, x, y, width, height, color, ball, img=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.object_ball = ball

        if img:
            self.rect = screen.create_image(x, y, image=img, anchor='nw')
        else:
            self.rect = screen.create_rectangle(x, y, x + width, y + height, fill=color)



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

    def set_x(self, new_x):
        max_x = int(self.screen['width']) - self.width
        self.x = max(0, min(new_x, max_x))
        self.screen.coords(self.paddle, self.x, self.y, self.x + self.width, self.y + self.height)


class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1500x800")
        self.title("Casse Brique")

        self.has_won = False
        self.is_game_over = False

        self.screen = tk.Canvas(self, width=1500, height=800, bg="black")
        self.screen.pack()

        self.heartImg = Image.open("heart.png").resize((30,30))
        self.heartTkImg = ImageTk.PhotoImage(self.heartImg)
        self.hearts =[]

        self.dirtTexture = Image.open("dirtTexture.jpg").resize((72,30))
        self.dirtTkTexture = ImageTk.PhotoImage(self.dirtTexture)

        self.object_ball = Ball(self.screen, x0, y0, r)
        self.object_paddle = Paddle(self.screen, x0 - 100, y0+35, 200, 15)

        self.score = 0
        self.labelScore = tk.Label(self, text=f"Score: {self.score}", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        self.labelScore.place(relx=0.90, rely=0.05)

        self.object_ball.vies = 3
        self.showHP(20, 20)


        buttonQuit = tk.Button(self, text='Quitter', font=36, fg='red', command=self.destroy)
        buttonQuit.place(relx=0.08, rely=0.93)

        self.buttonPlay = tk.Button(self, text="Jouer", font=36, fg="green", command=self.object_ball.move)
        self.buttonPlay.place(relx=0.02, rely=0.93)
        # bind space key (lowercase 'space' keysym) — ignore event argument
        self.screen.bind_all("<space>", lambda e: self.object_ball.move())

        self.Bricks = []
        self.showBrick()

        


    def update_lives(self):
        self.showHP(20,20)

    def update_score(self):
        self.labelScore.config(text=f"Score: {self.score}")

    def win(self):
        self.object_ball.moving = False
        self.has_won = True
        self.buttonPlay.config(state='disabled')

        cx = int(self.screen['width'])//2
        cy = int(self.screen['height'])//2
        self.screen.create_text(cx, cy, text="YOU WIN!", fill="white", font=("Arial", 40, "bold"), tags=('overlay',))
        self.overlay_restart_btn = tk.Button(self, text='Restart', font=(None, 14), command=self.restart)
        self.screen.create_window(cx, cy + 60, window=self.overlay_restart_btn, tags=('overlay',))


    def game_over(self):
        self.object_ball.moving = False
        self.is_game_over = True
        self.buttonPlay.config(state='disabled')
        cx = int(self.screen['width'])//2
        cy = int(self.screen['height'])//2
        self.screen.create_text(cx, cy, text="GAME OVER", fill="red", font=("Arial", 40, "bold"), tags=('overlay',))
        self.overlay_restart_btn = tk.Button(self, text='Restart', font=(None, 14), command=self.restart)
        self.screen.create_window(cx, cy + 60, window=self.overlay_restart_btn, tags=('overlay',))

    def showBrick(self):
        height = 30
        width = 72
        space = 15
        lines = 5
        columns = 18


        for i in range(lines):
            for j in range(columns):
                x = j * (width + space) + 20
                y = i * (height + space) + 70
                self.Bricks.append(Brick(self.screen, x, y, width, height, 'black', self.object_ball, img = self.dirtTkTexture))

    def HP(self, x, y):
        return self.screen.create_image(x, y, image=self.heartTkImg, anchor='nw')

    def showHP(self, x, y):
        
        for heart in self.hearts:
            self.screen.delete(heart)
        self.hearts.clear()

        for i in range(self.object_ball.vies):
            heart = self.HP(x + i * 35, y)
            self.hearts.append(heart)

    def restart(self):
        # clear overlay elements (text and restart button)
        self.screen.delete('overlay')
        if hasattr(self, 'overlay_restart_btn'):
            self.overlay_restart_btn.destroy()
            del self.overlay_restart_btn

        # reset flags
        self.has_won = False
        self.is_game_over = False

        # reset score and lives and ball
        self.score = 0
        self.object_ball.vies = 3
        self.object_ball.x = x0
        self.object_ball.y = y0
        vitesse = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        self.object_ball.dx = vitesse * math.cos(angle)
        self.object_ball.dy = vitesse * math.sin(angle)
        self.object_ball.moving = False

        # rebuild bricks
        for b in list(self.Bricks):
            self.screen.delete(b.rect)
        self.Bricks = []
        self.showBrick()


        # update UI and re-enable play
        self.update_score()
        self.update_lives()
        self.buttonPlay.config(state='normal')

window = MyWindow()
window.mainloop()