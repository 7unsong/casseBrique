import tkinter as tk




class Interface(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        Canevas = tk.Canvas(self, width = 1920, height = 1080, bg = "black", )
        Canevas.pack(padx=5, pady=5)

        labelScore = tk.Label(self, text = "Score: ", bg = "black", font = ("Arial", 15, "bold"), fg = "yellow")
        labelScore.place(relx = 0.90, rely = 0.05)

        labelVie = tk.Label(self, text = "Vies: ", bg = "black", font = ("Arial", 15, "bold"), fg ="yellow")
        labelVie.place(relx = 0.02, rely = 0.05)

        buttonQuit = tk.Button(self, text = "Quitter", font = 36, fg = "red", command = parent.destroy)
        buttonQuit.place(relx = 0.02, rely = 0.93)

        buttonPlay = tk.Button(self, text = "Jouer", font = 36, fg = "green", command = ) ##reprends la
        buttonPlay.place(relx = 0.05, rely = 0.93)

    def jouer():
        print("lance")


class MyWindow(tk.Tk):


    def __init__(self):

        super().__init__()

        self.geometry("1920x1080")

        self.title("Casse Brique")

        self.interface = Interface(self)
        self.interface.pack()


window = MyWindow()
window.mainloop()