"Créé le 9 Octobre 2025 par SONG Yun et DURAND Guillian"
"Ce fichier contient les classes principales du jeu Casse-Brique ainsi que les fonctions de gestion du jeu."
"Modifié le 5 mars 2026 par DURAND Guillian : ajout du mode Endless, mode Survie et de plusieurs effets/bonus des briques"

import tkinter as tk
import math, random
from PIL import Image, ImageTk
from collections import deque

width = 1500
height = 800

x0 = width / 2
y0 = 5/6 * height
r = 10

# Constantes du Mode Survie
SURVIVAL_ACCEL_INTERVAL = 5000   # ms entre chaque accélération
SURVIVAL_ACCEL_FACTOR   = 1.08   # multiplicateur par palier
SURVIVAL_MAX_SPEED      = 35     # vitesse max de la balle (px/frame)
SURVIVAL_PADDLE_SPEED_RATIO = 1.4  # vitesse paddle = vitesse_balle * ratio


class LifeStack:
    
    def __init__(self, n):
        """Initialise une pile de vies avec n vies."""
        self.stack = ['life'] * n

    def lose_life(self):
        """Retire une vie de la pile."""
        if not self.is_empty():
            return self.stack.pop()

    def add_life(self):
        """Ajoute une vie à la pile."""
        self.stack.append('life')

    def is_empty(self):
        """Vérifie si la pile de vies est vide."""
        return len(self.stack) == 0

    def count(self):
        """Retourne le nombre de vies restantes."""
        return len(self.stack)


class BonusQueue:
    """Gestion d'une file de bonus."""
    def __init__(self):
        """Initialise une file vide."""
        self.queue = deque()

    def add_bonus(self, bonus):
        """Ajoute un bonus à la file."""
        self.queue.append(bonus)

    def use_bonus(self):
        """Retire et retourne le bonus en tête de la file."""
        if self.queue:
            return self.queue.popleft()

    def is_empty(self):
        """Vérifie si la file de bonus est vide."""
        return len(self.queue) == 0


class Ball:
    def __init__(self, screen, x, y, rayon, lives_ref=None, is_extra=False):
        """
        lives_ref : LifeStack partagée (seule la balle principale l'utilise).
        is_extra  : True = balle bonus (sa perte ne coûte pas de vie).
        """
        self.screen   = screen
        self.x        = x
        self.y        = y
        self.rayon    = rayon
        self.is_extra = is_extra
        self.moving   = False

        speed = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)

        self.width  = int(screen["width"])
        self.height = int(screen["height"])

        if lives_ref is not None:
            self.lives = lives_ref
        elif not is_extra:
            self.lives = LifeStack(3)
        else:
            self.lives = None

        color = "orange" if is_extra else "red"
        self.id = screen.create_oval(
            self.x - self.rayon, self.y - self.rayon,
            self.x + self.rayon, self.y + self.rayon,
            fill=color
        )

    def deplacement(self):
        """Gère le déplacement de la balle et les collisions."""

        # Collisions avec les bords
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

        # Collisions avec les briques
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

                    brique.hp -= 1
                    if brique.hp > 0:
                        # Brique multi-vie : rebond sans destruction
                        dist_top    = abs(yb2 - by1)
                        dist_bottom = abs(yb1 - by2)
                        dist_left   = abs(xb2 - bx1)
                        dist_right  = abs(xb1 - bx2)
                        min_dist    = min(dist_top, dist_bottom, dist_left, dist_right)
                        if min_dist == dist_top or min_dist == dist_bottom:
                            self.dy *= -1
                        else:
                            self.dx *= -1
                        continue

                    # Destruction de la brique
                    self.screen.delete(brique.rect)
                    self.screen.master.Bricks.remove(brique)

                    dist_top    = abs(yb2 - by1)
                    dist_bottom = abs(yb1 - by2)
                    dist_left   = abs(xb2 - bx1)
                    dist_right  = abs(xb1 - bx2)
                    min_dist    = min(dist_top, dist_bottom, dist_left, dist_right)

                    if min_dist == dist_top or min_dist == dist_bottom:
                        self.dy *= -1
                    else:
                        self.dx *= -1

                    self.screen.master.score += 100 * brique.max_hp
                    if hasattr(self.screen.master, 'update_score'):
                        self.screen.master.update_score()

                    if getattr(brique, 'is_bonus', False) and hasattr(self.screen.master, 'bonus_queue'):
                        self.screen.master.bonus_queue.add_bonus(brique.bonus_type)

            # Vérification victoire / nouvelle vague
            if hasattr(self.screen.master, "Bricks") and len(self.screen.master.Bricks) == 0:
                if hasattr(self.screen.master, 'win'):
                    self.screen.master.after(0, self.screen.master.win)

        # Collision avec la raquette
        paddle = getattr(self.screen.master, 'object_paddle', None)
        if paddle is not None:
            paddle_x = getattr(paddle, 'x', None)
            paddle_y = getattr(paddle, 'y', None)
            paddle_w = getattr(paddle, 'width', None)
            if paddle_x is None:
                paddle_x, paddle_y, px2, py2 = self.screen.coords(paddle.paddle)
                paddle_w = px2 - paddle_x
                paddle_x = 0
                paddle_y = self.height
                paddle_w = 0

            ball_left   = self.x - self.rayon
            ball_right  = self.x + self.rayon
            ball_bottom = self.y + self.rayon
            ball_top    = self.y - self.rayon

            if (ball_right >= paddle_x and ball_left <= paddle_x + paddle_w
                    and ball_bottom >= paddle_y and ball_top < paddle_y):
                self.y  = paddle_y - self.rayon
                self.dy = -self.dy

        # Balle tombée
        if self.y + self.rayon + 10 > self.height:
            win   = self.screen.master
            balls = getattr(win, 'extra_balls', [])

            if self.is_extra:
                # Balle bonus perdue : suppression silencieuse
                self.moving = False
                self.screen.delete(self.id)
                if self in balls:
                    balls.remove(self)
                return

            else:
                if balls:
                    # Une balle extra prend la place de la principale (pas de perte de vie)
                    heir = balls.pop(0)
                    heir.is_extra = False
                    heir.lives    = self.lives
                    heir.screen.itemconfig(heir.id, fill="red")
                    win.object_ball = heir
                    self.moving = False
                    self.screen.delete(self.id)
                    return

                else:
                    # Vraie perte de vie
                    self.lives.lose_life()
                    self.moving = False
                    self.x = x0
                    self.y = y0

                    if getattr(win, 'game_mode', None) and win.game_mode.get() == "survival":
                        win.current_speed = 10
                        win._stop_survival_acceleration()
                        win.object_paddle.speed = 20
                        win.labelSpeed.config(text="Vitesse : 10.0")
                        win._bind_survival_start()

                    speed = getattr(win, 'current_speed', 10)
                    angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
                    self.dx = speed * math.cos(angle)
                    self.dy = speed * math.sin(angle)

                    paddle.set_x(x0 - paddle.width / 2)
                    self.moving = False
                    self.x = x0
                    self.y = y0

                    if hasattr(win, 'update_lives'):
                        win.update_lives()
                    if self.lives.is_empty() and hasattr(win, 'game_over'):
                        win.game_over()

        # Mise à jour position canvas
        self.screen.coords(
            self.id,
            self.x - self.rayon, self.y - self.rayon,
            self.x + self.rayon, self.y + self.rayon
        )

        if self.moving:
            self.screen.after(20, self.deplacement)

    def move(self, evt=None):
        """Démarre le mouvement de la balle si elle n'est pas déjà en mouvement."""
        win_flag  = getattr(self.screen.master, 'has_won', False)
        over_flag = getattr(self.screen.master, 'is_game_over', False)
        if not (self.moving or win_flag or over_flag):
            self.moving = True
            self.deplacement()


class Brick:
    def __init__(self, screen, x, y, width, height, color, ball,
                 img=None, is_bonus=False, bonus_type="paddle_size_up", hp=1):
        self.screen      = screen
        self.x           = x
        self.y           = y
        self.width       = width
        self.height      = height
        self.object_ball = ball
        self.is_bonus    = bool(is_bonus)
        self.bonus_type  = bonus_type
        self.hp          = hp
        self.max_hp      = hp

        if img:
            self.rect = screen.create_image(x, y, image=img, anchor='nw')
        else:
            self.rect = screen.create_rectangle(x, y, x + width, y + height, fill=color)


class Paddle:

    def __init__(self, screen, x, y, width, height):
        self.screen        = screen
        self.x             = x
        self.y             = y
        self.width         = width
        self.default_width = width
        self.height        = height
        self.speed         = 20
        self.boosted       = False
        self.boost_timer   = None
        self.moving_left   = False
        self.moving_right  = False

        self.paddle = screen.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill="grey"
        )

        screen.bind_all("<KeyPress-Left>",    self.start_left)
        screen.bind_all("<KeyRelease-Left>",  self.stop_left)
        screen.bind_all("<KeyPress-Right>",   self.start_right)
        screen.bind_all("<KeyRelease-Right>", self.stop_right)

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

        self.screen.coords(self.paddle, self.x, self.y, self.x + self.width, self.y + self.height)
        self.screen.after(20, self.move_continuously)

    def set_x(self, new_x):
        max_x  = int(self.screen['width']) - self.width
        self.x = max(0, min(new_x, max_x))
        self.screen.coords(self.paddle, self.x, self.y, self.x + self.width, self.y + self.height)


class MyWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry("1500x800")
        self.title("Casse Brique")

        self.has_won      = False
        self.is_game_over = False

        self.game_mode         = tk.StringVar(value="classic")
        self.survival_timer_id = None
        self.current_speed     = 10
        self.endless_wave      = 0

        self.screen = tk.Canvas(self, width=1500, height=800, bg="black")
        self.screen.pack()

        self.heartImg    = Image.open("heart.png").resize((30, 30))
        self.heartTkImg  = ImageTk.PhotoImage(self.heartImg)
        self.hearts      = []

        self.brickTexture   = Image.open("brickTexture.jpg").resize((72, 30))
        self.brickTkTexture = ImageTk.PhotoImage(self.brickTexture)

        try:
            self.diamondTexture   = Image.open("Diamond_Ore.png").resize((72, 30))
            self.diamondTkTexture = ImageTk.PhotoImage(self.diamondTexture)
        except Exception:
            self.diamondTkTexture = self.brickTkTexture

        try:
            self.goldTexture   = Image.open("Gold_Ore.jpg").resize((72, 30))
            self.goldTkTexture = ImageTk.PhotoImage(self.goldTexture)
        except Exception:
            self.goldTkTexture = self.brickTkTexture

        try:
            self.netherbricksTexture   = Image.open("netherbricks_texture.png").resize((72, 30))
            self.netherbricksTkTexture = ImageTk.PhotoImage(self.netherbricksTexture)
        except Exception:
            self.netherbricksTkTexture = self.brickTkTexture

        self.object_ball   = Ball(self.screen, x0, y0, r)
        self.object_paddle = Paddle(self.screen, x0 - 125, y0 + 35, 250, 15)
        self.extra_balls   = []

        self.score      = 0
        self.labelScore = tk.Label(
            self, text=f"Score: {self.score}",
            bg="black", font=("Arial", 15, "bold"), fg="yellow"
        )
        self.labelScore.place(relx=0.90, rely=0.05)

        self.labelSpeed = tk.Label(
            self, text="", bg="black", font=("Arial", 12, "bold"), fg="orange"
        )
        self.labelSpeed.place(relx=0.90, rely=0.10)

        self.bonus_queue = BonusQueue()
        self.after(200, self.update_game)

        self.showHP(20, 20)

        buttonQuit = tk.Button(self, text='Quitter', font=36, fg='red', command=self.destroy)
        buttonQuit.place(relx=0.08, rely=0.93)

        self.buttonPlay = tk.Button(self, text="Jouer", font=36, fg="green", command=self.object_ball.move)
        self.buttonPlay.place(relx=0.02, rely=0.93)

        modeFrame = tk.Frame(self, bg="black")
        modeFrame.place(relx=0.14, rely=0.94)

        tk.Label(modeFrame, text="Mode :", bg="black", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=(0, 6))

        tk.Radiobutton(
            modeFrame, text="Classique", variable=self.game_mode, value="classic",
            bg="black", fg="white", selectcolor="black", activebackground="black",
            activeforeground="cyan", font=("Arial", 11), command=self._on_mode_change
        ).pack(side="left", padx=4)

        tk.Radiobutton(
            modeFrame, text="Survie", variable=self.game_mode, value="survival",
            bg="black", fg="orange", selectcolor="black", activebackground="black",
            activeforeground="orange", font=("Arial", 11, "bold"), command=self._on_mode_change
        ).pack(side="left", padx=4)

        tk.Radiobutton(
            modeFrame, text="Endless", variable=self.game_mode, value="endless",
            bg="black", fg="cyan", selectcolor="black", activebackground="black",
            activeforeground="cyan", font=("Arial", 11, "bold"), command=self._on_mode_change
        ).pack(side="left", padx=4)

        self.screen.bind_all("<space>", lambda e: self.object_ball.move())

        self.Bricks = []
        self.showBrick()

    def _on_mode_change(self):
        """Relance une partie propre quand le joueur change de mode."""
        self.restart()

    def update_lives(self):
        self.showHP(20, 20)

    def update_score(self):
        self.labelScore.config(text=f"Score: {self.score}")
        if len(self.Bricks) == 0 and not self.has_won and self.game_mode.get() != "endless":
            self.win()

    def update_game(self):
        try:
            if not self.bonus_queue.is_empty():
                bonus = self.bonus_queue.use_bonus()
                if bonus:
                    self.apply_bonus(bonus)
        except Exception:
            pass
        self.after(200, self.update_game)

    def apply_bonus(self, bonus):
        """Applique le bonus spécifié."""
        if bonus == "paddle_size_up":
            p = self.object_paddle
            if getattr(p, 'boosted', False):
                return
            p.boosted = True
            p.width  += 50
            p.set_x(p.x)
            self.screen.itemconfig(p.paddle, fill="cyan")

            def revert():
                try:
                    p.width   = getattr(p, 'default_width', p.width - 50)
                    p.boosted = False
                    p.set_x(p.x)
                    p.boost_timer = None
                    self.screen.itemconfig(p.paddle, fill="grey")
                except Exception:
                    pass

            p.boost_timer = self.after(15000, revert)

        elif bonus == "multi_ball":
            main  = self.object_ball
            speed = getattr(self, 'current_speed', 10)
            angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)

            new_ball = Ball(
                self.screen,
                main.x + random.randint(-30, 30),
                main.y,
                r,
                lives_ref=None,
                is_extra=True
            )
            new_ball.dx = speed * math.cos(angle)
            new_ball.dy = speed * math.sin(angle)
            new_ball.moving = True
            self.extra_balls.append(new_ball)
            new_ball.deplacement()

    def start_survival_acceleration(self):
        self._survival_accelerate()

    def _survival_accelerate(self):
        """Accélère progressivement la balle et le paddle en mode survie."""
        if self.has_won or self.is_game_over:
            return

        ball = self.object_ball
        spd  = math.hypot(ball.dx, ball.dy)
        if spd < SURVIVAL_MAX_SPEED:
            new_spd = min(spd * SURVIVAL_ACCEL_FACTOR, SURVIVAL_MAX_SPEED)
            ratio   = new_spd / spd if spd > 0 else 1
            ball.dx *= ratio
            ball.dy *= ratio
            self.current_speed = new_spd

            for eb in self.extra_balls:
                eb.dx *= ratio
                eb.dy *= ratio

            self.object_paddle.speed = int(new_spd * SURVIVAL_PADDLE_SPEED_RATIO)
            self.labelSpeed.config(text=f"Vitesse : {new_spd:.1f}")

        self.survival_timer_id = self.after(SURVIVAL_ACCEL_INTERVAL, self._survival_accelerate)

    def _stop_survival_acceleration(self):
        if self.survival_timer_id:
            try:
                self.after_cancel(self.survival_timer_id)
            except Exception:
                pass
            self.survival_timer_id = None

    def win(self):
        """Victoire : affiche l'écran de fin, sauf en mode Endless où on génère de nouvelles briques."""
        if self.game_mode.get() == "endless":
            self._endless_next_wave()
            return

        self._stop_survival_acceleration()
        self.object_ball.moving = False
        for eb in self.extra_balls:
            eb.moving = False
        self.has_won = True
        self.buttonPlay.config(state='disabled')

        cx = int(self.screen['width']) // 2
        cy = int(self.screen['height']) // 2
        self.screen.create_text(cx, cy, text="YOU WIN!", fill="white",
                                font=("Arial", 40, "bold"), tags=('overlay',))
        self.screen.create_text(cx, cy - 50, text=f"Score final : {self.score}",
                                fill="yellow", font=("Arial", 20), tags=('overlay',))
        self.overlay_restart_btn = tk.Button(self, text='Restart', font=(None, 14), command=self.restart)
        self.screen.create_window(cx, cy + 60, window=self.overlay_restart_btn, tags=('overlay',))

    def _endless_next_wave(self):
        """Mode Endless : génère une nouvelle vague de briques sans interrompre la balle."""
        self.endless_wave += 1
        self.showBrick()
        cx = int(self.screen['width']) // 2
        self.screen.create_text(
            cx, int(self.screen['height']) // 2,
            text=f"Vague {self.endless_wave} !",
            fill="white", font=("Arial", 30, "bold"), tags=('wave_notif',)
        )
        self.after(1500, lambda: self.screen.delete('wave_notif'))

    def game_over(self):
        self._stop_survival_acceleration()
        self.object_ball.moving = False
        for eb in self.extra_balls:
            eb.moving = False
        self.is_game_over = True
        self.buttonPlay.config(state='disabled')

        cx = int(self.screen['width']) // 2
        cy = int(self.screen['height']) // 2
        self.screen.create_text(cx, cy, text="GAME OVER", fill="red",
                                font=("Arial", 40, "bold"), tags=('overlay',))
        self.screen.create_text(cx, cy - 50, text=f"Score : {self.score}",
                                fill="yellow", font=("Arial", 20), tags=('overlay',))
        self.overlay_restart_btn = tk.Button(self, text='Restart', font=(None, 14), command=self.restart)
        self.screen.create_window(cx, cy + 60, window=self.overlay_restart_btn, tags=('overlay',))

    def showBrick(self):
        """Affiche une grille de briques."""
        brick_height = 30
        brick_width  = 72
        space        = 15
        lines        = 4
        columns      = 17

        for i in range(lines):
            for j in range(columns):
                x = j * (brick_width + space) + 20
                y = i * (brick_height + space) + 70

                roll = random.random()

                if roll < 0.10:
                    img        = self.goldTkTexture
                    is_bonus   = True
                    bonus_type = "multi_ball"
                    hp         = 1

                elif roll < 0.20:
                    img        = self.diamondTkTexture
                    is_bonus   = True
                    bonus_type = "paddle_size_up"
                    hp         = 1

                elif roll < 0.35:
                    img        = self.netherbricksTkTexture
                    is_bonus   = False
                    bonus_type = "none"
                    hp         = 2

                else:
                    img        = self.brickTkTexture
                    is_bonus   = False
                    bonus_type = "none"
                    hp         = 1

                self.Bricks.append(Brick(
                    self.screen, x, y, brick_width, brick_height, 'black',
                    self.object_ball,
                    img=img, is_bonus=is_bonus, bonus_type=bonus_type, hp=hp
                ))

    def HP(self, x, y):
        return self.screen.create_image(x, y, image=self.heartTkImg, anchor='nw')

    def showHP(self, x, y):
        for heart in self.hearts:
            self.screen.delete(heart)
        self.hearts.clear()
        for i in range(self.object_ball.lives.count()):
            heart = self.HP(x + i * 35, y)
            self.hearts.append(heart)

    def restart(self):
        """Redémarre le jeu."""
        self._stop_survival_acceleration()

        self.screen.delete('overlay')
        if hasattr(self, 'overlay_restart_btn'):
            self.overlay_restart_btn.destroy()
            del self.overlay_restart_btn

        self.has_won       = False
        self.is_game_over  = False
        self.score         = 0
        self.current_speed = 10
        self.endless_wave  = 0
        self.labelSpeed.config(text="")

        for eb in self.extra_balls:
            eb.moving = False
            self.screen.delete(eb.id)
        self.extra_balls = []

        self.object_ball.lives    = LifeStack(3)
        self.object_ball.x        = x0
        self.object_ball.y        = y0
        speed = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        self.object_ball.dx       = speed * math.cos(angle)
        self.object_ball.dy       = speed * math.sin(angle)
        self.object_ball.moving   = False
        self.object_ball.is_extra = False

        p = self.object_paddle
        if getattr(p, 'boost_timer', None):
            try:
                self.after_cancel(p.boost_timer)
            except Exception:
                pass
            p.boost_timer = None

        if getattr(p, 'default_width', None) is not None:
            p.width   = p.default_width
            p.boosted = False
            p.set_x(x0 - p.width / 2)
            self.screen.itemconfig(p.paddle, fill="grey")

        p.speed = 20

        for b in list(self.Bricks):
            self.screen.delete(b.rect)
        self.Bricks = []
        self.showBrick()

        self.update_score()
        self.update_lives()
        self.buttonPlay.config(state='normal')

        self.screen.bind_all("<space>", lambda e: self.object_ball.move())

        if self.game_mode.get() == "survival":
            self._bind_survival_start()

    def _bind_survival_start(self):
        """Démarre l'accélération dès que la balle part (première pression espace)."""
        def space_handler(e):
            self.object_ball.move()
            self.after(150, lambda: (
                self.start_survival_acceleration()
                if self.object_ball.moving else None
            ))

        self.screen.bind_all("<space>", space_handler)


window = MyWindow()

if window.game_mode.get() == "survival":
    window._bind_survival_start()

window.mainloop()