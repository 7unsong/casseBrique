import tkinter as tk
import math, random

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
        self.id = screen.create_oval(self.x - rayon, self.y - rayon, self.x + rayon, self.y + rayon, fill="red", outline="white")

    def deplacement(self):
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
                bx1, by1, bx2, by2 = self.screen.coords(brique.rect)
                xb1 = self.x - self.rayon
                yb1 = self.y - self.rayon
                xb2 = self.x + self.rayon
                yb2 = self.y + self.rayon

                if xb2 >= bx1 and xb1 <= bx2 and yb2 >= by1 and yb1 <= by2:
                    # remove brick, update score, bounce
                    self.screen.delete(brique.rect)
                    self.screen.master.score += 100
                    if hasattr(self.screen.master, 'update_score'):
                        self.screen.master.update_score()
                    self.screen.master.Bricks.remove(brique)
                    self.dy *= -1
                    # check win
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

    def move(self):
        win_flag = getattr(self.screen.master, 'has_won', False)
        over_flag = getattr(self.screen.master, 'is_game_over', False)
        if not (self.moving or win_flag or over_flag):
            self.moving = True
            self.deplacement()


class Brick:
    def __init__(self, screen, x, y, width, height, color, ball):
        self.screen = screen
        self.rect = screen.create_rectangle(x, y, x+width, y+height, fill=color)
        self.object_ball = ball


class Paddle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen.bind_all("<Left>", self.gauche)
        self.screen.bind_all("<Right>", self.droite)
        self.paddle = screen.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="grey")

    def gauche(self, evt):
        if self.x > 0:
            self.x -= 50
            self.screen.coords(self.paddle, self.x, self.y, self.x + self.width, self.y + self.height)

    def droite(self, evt):
        if self.x + self.width < int(self.screen["width"]):
            self.x += 50
            self.screen.coords(self.paddle, self.x, self.y, self.x + self.width, self.y + self.height)

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

        self.object_ball = Ball(self.screen, x0, y0, r)
        self.object_paddle = Paddle(self.screen, x0 - 100, y0+35, 200, 15)

        self.score = 0
        self.labelScore = tk.Label(self, text=f"Score: {self.score}", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        self.labelScore.place(relx=0.90, rely=0.05)

        self.labelVie = tk.Label(self, text=f"Vies: {self.object_ball.vies}", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        self.labelVie.place(relx=0.02, rely=0.05)

        buttonQuit = tk.Button(self, text='Quitter', font=36, fg='red', command=self.destroy)
        buttonQuit.place(relx=0.08, rely=0.93)

        self.buttonPlay = tk.Button(self, text="Jouer", font=36, fg="green", command=self.object_ball.move)
        self.buttonPlay.place(relx=0.02, rely=0.93)

        self.Bricks = []
        self.showBrick()

    def update_lives(self):
        self.labelVie.config(text=f"Vies: {self.object_ball.vies}")

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