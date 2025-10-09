import tkinter as tk






    


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

        buttonPlay = tk.Button(self, text = "Jouer", font = 36, fg = "green", command = self.jouer)
        buttonPlay.place(relx = 0.02, rely = 0.93)


    def jouer(self):
        self.screen.create_oval(350, 250, 450, 350, fill = "red")
        


    
window = MyWindow()
window.mainloop()