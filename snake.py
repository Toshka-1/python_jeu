import tkinter as tk
import random

class Nourriture:
    def __init__(self, canvas, taille_case, width, height):
        self.canvas = canvas
        self.taille_case = taille_case
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.obj = None
        self.generer()

    def generer(self):
        if self.obj is not None:
            self.canvas.delete(self.obj)
        max_x = self.width // self.taille_case - 1
        max_y = self.height // self.taille_case - 1
        self.x = random.randint(0, max_x)
        self.y = random.randint(0, max_y)
        x1 = self.x * self.taille_case
        y1 = self.y * self.taille_case
        x2 = x1 + self.taille_case
        y2 = y1 + self.taille_case
        self.obj = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

class Serpent:
    def __init__(self, canvas, x, y, taille_case):
        self.canvas = canvas
        self.taille_case = taille_case
        self.corps = [(x, y), (x-1, y), (x-2, y)]
        self.direction = "droite"
        self.objets = []
        self.dessiner()

    def dessiner(self):
        for obj in self.objets:
            self.canvas.delete(obj)
        self.objets = []
        for (x, y) in self.corps:
            x1 = x * self.taille_case
            y1 = y * self.taille_case
            x2 = x1 + self.taille_case
            y2 = y1 + self.taille_case
            self.objets.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="green"))

    def changer_direction(self, nouvelle_dir):
        directions_opposees = {("haut","bas"), ("bas","haut"), ("gauche","droite"), ("droite","gauche")}
        if (self.direction, nouvelle_dir) not in directions_opposees and (nouvelle_dir, self.direction) not in directions_opposees:
            self.direction = nouvelle_dir

    def avancer(self):
        (x, y) = self.corps[0]
        if self.direction == "haut":
            y -= 1
        elif self.direction == "bas":
            y += 1
        elif self.direction == "gauche":
            x -= 1
        elif self.direction == "droite":
            x += 1
        self.corps.insert(0, (x, y))

    def grandir(self):
        # On n'enlève pas la dernière case pour grandir
        pass

    def bouger(self):
        self.avancer()
        self.corps.pop()

class JeuSerpent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jeu du Serpent")
        self.taille_case = 20
        self.width = 400
        self.height = 400

        # Créer un cadre principal
        self.cadre_principal = tk.Frame(self.root)
        self.cadre_principal.pack()

        # Écran de démarrage
        self.creer_ecran_demarrage()

        self.root.mainloop()

    def creer_ecran_demarrage(self):
        # Créer un cadre pour l'écran de démarrage
        self.cadre_demarrage = tk.Frame(self.cadre_principal)
        self.cadre_demarrage.pack(expand=True)

        # Titre
        titre = tk.Label(self.cadre_demarrage, text="Bienvenue dans le Jeu du Serpent!", font=("Arial", 24))
        titre.pack(pady=20)

        # Bouton Démarrer
        bouton_demarrer = tk.Button(self.cadre_demarrage, text="Démarrer", font=("Arial", 16), command=self.demarrer_jeu)
        bouton_demarrer.pack(pady=10)

        # Bouton Quitter
        bouton_quitter = tk.Button(self.cadre_demarrage, text="Quitter", font=("Arial", 16), command=self.root.quit)
        bouton_quitter.pack(pady=10)

    def demarrer_jeu(self):
        # Détruire l'écran de démarrage
        self.cadre_demarrage.destroy()

        # Créer le canvas pour le jeu
        self.canvas = tk.Canvas(self.cadre_principal, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Initialiser le serpent
        self.serpent = Serpent(self.canvas, 5, 5, self.taille_case)

        # Initialiser la nourriture
        self.nourriture = Nourriture(self.canvas, self.taille_case, self.width, self.height)
        self.game_over = False

        # Configurer les contrôles
        self.root.bind("<Up>", lambda e: self.serpent.changer_direction("haut"))
        self.root.bind("<Down>", lambda e: self.serpent.changer_direction("bas"))
        self.root.bind("<Left>", lambda e: self.serpent.changer_direction("gauche"))
        self.root.bind("<Right>", lambda e: self.serpent.changer_direction("droite"))

        # Démarrer la boucle de mise à jour
        self.mettre_a_jour()

    def mettre_a_jour(self):
        if not self.game_over:
            self.serpent.bouger()
            # Vérifier les collisions
            x, y = self.serpent.corps[0]
            # Bordures
            if x < 0 or x * self.taille_case >= self.width or y < 0 or y * self.taille_case >= self.height:
                self.game_over = True
            # Queue
            if (x, y) in self.serpent.corps[1:]:
                self.game_over = True
            # Nourriture
            if x == self.nourriture.x and y == self.nourriture.y:
                self.serpent.grandir()
                self.serpent.corps.append(self.serpent.corps[-1])
                self.nourriture.generer()

            self.serpent.dessiner()
            if self.game_over:
                self.canvas.create_text(self.width / 2, self.height / 2, text="GAME OVER", fill="white", font=("Arial", 20))
                # Optionnel : Ajouter un bouton pour revenir à l'écran de démarrage ou quitter
                bouton_rejouer = tk.Button(self.cadre_principal, text="Rejouer", font=("Arial", 16), command=self.rejouer)
                bouton_rejouer.place(x=self.width/2 - 50, y=self.height/2 + 30)
            else:
                self.root.after(100, self.mettre_a_jour)

    def rejouer(self):
        # Détruire le canvas de jeu
        self.canvas.destroy()
        # Détruire le bouton "Rejouer" s'il existe
        for widget in self.cadre_principal.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] == "Rejouer":
                widget.destroy()
        # Recréer l'écran de démarrage
        self.creer_ecran_demarrage()

# Pour lancer le jeu du serpent, décommentez la ligne suivante :
JeuSerpent()