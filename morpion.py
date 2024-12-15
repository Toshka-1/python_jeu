import tkinter as tk

class JeuMorpion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Morpion")
        self.joueur_courant = "X"
        self.grille = [["" for _ in range(3)] for _ in range(3)]
        self.boutons = []

        self.creer_interface()
        self.root.mainloop()

    def creer_interface(self):
        cadre = tk.Frame(self.root)
        cadre.pack()
        for i in range(3):
            ligne_boutons = []
            for j in range(3):
                btn = tk.Button(cadre, text="", width=5, height=2, font=("Arial", 24),
                                command=lambda x=i, y=j: self.clic_case(x, y))
                btn.grid(row=i, column=j)
                ligne_boutons.append(btn)
            self.boutons.append(ligne_boutons)
        self.label_info = tk.Label(self.root, text="Joueur X, à toi de jouer!")
        self.label_info.pack()

    def clic_case(self, i, j):
        if self.grille[i][j] == "" and not self.verifier_vainqueur():
            self.grille[i][j] = self.joueur_courant
            self.boutons[i][j].configure(text=self.joueur_courant)
            if self.verifier_vainqueur():
                self.label_info.config(text=f"Le joueur {self.joueur_courant} a gagné!")
            elif self.partie_nulle():
                self.label_info.config(text="Match nul!")
            else:
                self.joueur_courant = "O" if self.joueur_courant == "X" else "X"
                self.label_info.config(text=f"Joueur {self.joueur_courant}, à toi de jouer!")

    def verifier_vainqueur(self):
        # Vérifier les lignes
        for i in range(3):
            if self.grille[i][0] == self.grille[i][1] == self.grille[i][2] != "":
                return True
        # Vérifier les colonnes
        for j in range(3):
            if self.grille[0][j] == self.grille[1][j] == self.grille[2][j] != "":
                return True
        # Vérifier diagonales
        if self.grille[0][0] == self.grille[1][1] == self.grille[2][2] != "":
            return True
        if self.grille[0][2] == self.grille[1][1] == self.grille[2][0] != "":
            return True
        return False

    def partie_nulle(self):
        for i in range(3):
            for j in range(3):
                if self.grille[i][j] == "":
                    return False
        return True
    
JeuMorpion()