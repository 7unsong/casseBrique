"Créé le 9 Octobre 2025 par SONG Yun et DURAND Guillian"
"Ce fichier contient les classes principales du jeu Casse-Brique ainsi que les fonctions de gestion du jeu."

import tkinter as tk
import math, random
from PIL import Image, ImageTk
from collections import deque

width = 1500
height = 800

x0 = width / 2
y0 = 5/6 * height
r = 10

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
    def __init__(self, screen, x, y, rayon):
        
        # Initialisation des variables

        self.screen = screen
        self.x = x
        self.y = y
        self.rayon = rayon
        speed = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)
        self.width = int(screen["width"])
        self.height = int(screen["height"])
        self.lives = LifeStack(3)
        self.moving = False

        # Création de la balle
        self.id = screen.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon, fill="red")

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
            # parcours sur une copie pour pouvoir modifier l'originale
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
                
                    # Suppression de brique

                    self.screen.delete(brique.rect)
                    self.screen.master.Bricks.remove(brique)

                    # Détermine le côté de l'impact pour inverser la vélocité
                    dist_top = abs(yb2 - by1)
                    dist_bottom = abs(yb1 - by2)
                    dist_left = abs(xb2 - bx1)
                    dist_right = abs(xb1 - bx2)
                    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

                    if min_dist == dist_top or min_dist == dist_bottom:
                        self.dy *= -1
                    else:
                        self.dx *= -1
                    
                    # Mise a jour du score

                    self.screen.master.score += 100
                    if hasattr(self.screen.master, 'update_score'):
                        self.screen.master.update_score()

                    try:
                        if hasattr(self.screen.master, "Bricks") and len(self.screen.master.Bricks) == 0:
                            # schedule win() on la boucle principale Tk pour éviter tout problème d'appel direct
                            if hasattr(self.screen.master, 'win'):
                                self.screen.master.after(0, self.screen.master.win)
                    except Exception:
                        pass

        # Collision avec la raquette
                    # increment score
                
                    self.screen.master.score += 100
                    if hasattr(self.screen.master, 'update_score'):
                        self.screen.master.update_score()

                    # enqueue bonus if this brick is a bonus brick
                    
                    if getattr(brique, 'is_bonus', False) and hasattr(self.screen.master, 'bonus_queue'):
                        self.screen.master.bonus_queue.add_bonus("paddle_size_up")
                
            # FIN DE BOUCLE: vérification de victoire (fait en dehors de la boucle)
        
            if hasattr(self.screen.master, "Bricks") and len(self.screen.master.Bricks) == 0:
                # schedule win() on la boucle principale Tk pour éviter tout problème d'appel direct
                if hasattr(self.screen.master, 'win'):
                    self.screen.master.after(0, self.screen.master.win)
                
        # paddle collision
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

        # Traitement du cas où la balle tombe (en bas)

        # fallen below bottom
        if self.y + self.rayon + 10 > self.height:
            # lose one life from the stack
            self.lives.lose_life()
            # stop and reset
            self.moving = False
            self.x = x0
            self.y = y0

            # Réinitialisation des valeurs (angle et vitesse)

            speed = 10
            angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
            self.dx = speed * math.cos(angle)
            self.dy = speed * math.sin(angle)

            # Repositionnement de la raquette

            paddle.set_x(x0 - paddle.width/2)
            self.moving = False
            self.x = x0
            self.y = y0
            if hasattr(self.screen.master, 'update_lives'):
                self.screen.master.update_lives()
                
                if self.lives.is_empty() and hasattr(self.screen.master, 'game_over'):
                    self.screen.master.game_over()



            # Mise a jour du nombre de vies et vérification si "Game Over"

            if hasattr(self.screen.master, 'update_lives'):
                self.screen.master.update_lives()
            if self.lives.is_empty() and hasattr(self.screen.master, 'game_over'):
                self.screen.master.game_over()


        # mise a jour de la position de la balle
        self.screen.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)

        # Rappelle la fonction après un court délai si la balle est en mouvement
        if self.moving:
            self.screen.after(20, self.deplacement)

    def move(self, evt=None):

        """Démarre le mouvement de la balle si elle n'est pas déjà en mouvement.""" 

        win_flag = getattr(self.screen.master, 'has_won', False)
        over_flag = getattr(self.screen.master, 'is_game_over', False)
        if not (self.moving or win_flag or over_flag):
            self.moving = True
            self.deplacement()


class Brick:
    def __init__(self, screen, x, y, width, height, color, ball, img=None, is_bonus = False):
        #Initialisation des variables
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.object_ball = ball
        self.is_bonus = bool(is_bonus)

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
        self.default_width = width
        self.height = height
        self.speed = 20  # vitesse du déplacement
        # boost state (non-stacking)
        self.boosted = False
        self.boost_timer = None

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
        """Commence le déplacement vers la gauche."""
        self.moving_left = True

    def stop_left(self, evt):
        """Arrête le déplacement vers la gauche."""
        self.moving_left = False

    def start_right(self, evt):
        """Commence le déplacement vers la droite."""
        self.moving_right = True

    def stop_right(self, evt):
        """Arrête le déplacement vers la droite."""
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
        """Met à jour la position x de la raquette en respectant les limites de l'écran."""
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

        self.brickTexture = Image.open("brickTexture.jpg").resize((72,30))
        self.brickTkTexture = ImageTk.PhotoImage(self.brickTexture)
        # texture diamant
        try:
            self.diamondTexture = Image.open("Diamond_Ore.png").resize((72,30))
            self.diamondTkTexture = ImageTk.PhotoImage(self.diamondTexture)
        except Exception:
            # fall back to brick texture if diamond not found
            self.diamondTkTexture = self.brickTkTexture

        self.object_ball = Ball(self.screen, x0, y0, r)
        self.object_paddle = Paddle(self.screen, x0 - 125, y0+35, 250, 15)

        self.score = 0
        self.labelScore = tk.Label(self, text=f"Score: {self.score}", bg="black", font=("Arial", 15, "bold"), fg="yellow")
        self.labelScore.place(relx=0.90, rely=0.05)

        # initialize bonus queue
        self.bonus_queue = BonusQueue()
        # start periodic game update (process pending bonuses)
        self.after(200, self.update_game)
        self.showHP(20, 20)

        buttonQuit = tk.Button(self, text='Quitter', font=36, fg='red', command=self.destroy)
        buttonQuit.place(relx=0.08, rely=0.93)

        self.buttonPlay = tk.Button(self, text="Jouer", font=36, fg="green", command=self.object_ball.move)
        self.buttonPlay.place(relx=0.02, rely=0.93)

        # Lancer le jeu lors de l'appui de la touche espace

        self.screen.bind_all("<space>", lambda e: self.object_ball.move())

        self.Bricks = []
        self.showBrick()

    def update_lives(self):
        self.showHP(20,20)

    def update_score(self):
        """Met à jour l'affichage du score."""
        self.labelScore.config(text=f"Score: {self.score}")
        if len(self.Bricks) == 0 and not self.has_won:
            self.win()

    def update_game(self):
        """"Met à jour l'état du jeu périodiquement."""
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
            try:
                p = self.object_paddle
                # do not stack boosts
                if getattr(p, 'boosted', False):
                    return
                p.boosted = True
                # increase width and update coords
                p.width += 50
                p.set_x(p.x)

                # schedule revert after 15 seconds
                def revert():
                    try:
                        p.width = getattr(p, 'default_width', p.width - 50)
                        p.boosted = False
                        p.set_x(p.x)
                        p.boost_timer = None
                    except Exception:
                        pass

                # store timer id so we can cancel on restart
                try:
                    p.boost_timer = self.after(15000, revert)
                except Exception:
                    # fallback: try without storing timer
                    self.after(15000, revert)
            except Exception:
                pass

    def win(self):
        """Gère la victoire du joueur."""
        self.object_ball.moving = False
        self.has_won = True
        self.buttonPlay.config(state='disabled')

        cx = int(self.screen['width'])//2
        cy = int(self.screen['height'])//2
        self.screen.create_text(cx, cy, text="YOU WIN!", fill="white", font=("Arial", 40, "bold"), tags=('overlay',))
        self.overlay_restart_btn = tk.Button(self, text='Restart', font=(None, 14), command=self.restart)
        self.screen.create_window(cx, cy + 60, window=self.overlay_restart_btn, tags=('overlay',))

    def game_over(self):
        """Gère la fin de partie du joueur."""
        self.object_ball.moving = False
        self.is_game_over = True
        self.buttonPlay.config(state='disabled')
        cx = int(self.screen['width'])//2
        cy = int(self.screen['height'])//2
        self.screen.create_text(cx, cy, text="GAME OVER", fill="red", font=("Arial", 40, "bold"), tags=('overlay',))
        self.overlay_restart_btn = tk.Button(self, text='Restart', font=(None, 14), command=self.restart)
        self.screen.create_window(cx, cy + 60, window=self.overlay_restart_btn, tags=('overlay',))

    def showBrick(self):
        """Affiche les briques à l'écran."""
        height = 30
        width = 72
        space = 15
        lines = 5
        columns = 18

        for i in range(lines):
            for j in range(columns):
                x = j * (width + space) + 20
                y = i * (height + space) + 70
                """ Il y a une chance que le bloque soit un bonus, on utilise la texture diamant si c'est le cas """
                is_bonus = (random.random() < 0.2)
                img = self.diamondTkTexture if is_bonus else self.brickTkTexture
                self.Bricks.append(Brick(self.screen, x, y, width, height, 'black', self.object_ball, img=img, is_bonus=is_bonus))

    def HP(self, x, y):
        """Affiche une icône de cœur représentant une vie."""
        return self.screen.create_image(x, y, image=self.heartTkImg, anchor='nw')

    def showHP(self, x, y):
        """Met à jour l'affichage des vies restantes."""
        for heart in self.hearts:
            self.screen.delete(heart)
        self.hearts.clear()

        for i in range(self.object_ball.lives.count()):
            heart = self.HP(x + i * 35, y)
            self.hearts.append(heart)

    def restart(self):
        """Redémarre le jeu."""
        self.screen.delete('overlay')
        if hasattr(self, 'overlay_restart_btn'):
            self.overlay_restart_btn.destroy()
            del self.overlay_restart_btn

        self.has_won = False
        self.is_game_over = False

        self.score = 0
        self.object_ball.lives = LifeStack(3)
        self.object_ball.x = x0
        self.object_ball.y = y0
        speed = 10
        angle = random.uniform(11/6 * math.pi, 7/6 * math.pi)
        self.object_ball.dx = speed * math.cos(angle)
        self.object_ball.dy = speed * math.sin(angle)
        self.object_ball.moving = False

        try:
            p = self.object_paddle
            if getattr(p, 'boost_timer', None):
                try:
                    self.after_cancel(p.boost_timer)
                except Exception:
                    pass
                p.boost_timer = None

            if getattr(p, 'default_width', None) is not None:
                p.width = p.default_width
                p.boosted = False
                p.set_x(p.x)
        except Exception:
            pass

        for b in list(self.Bricks):
            self.screen.delete(b.rect)
        self.Bricks = []
        self.showBrick()

        self.update_score()
        self.update_lives()
        self.buttonPlay.config(state='normal')


window = MyWindow()
window.mainloop()