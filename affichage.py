import tkinter as tk

class Vue:
    def __init__(self, title="Mon Jeu", width=400, height=300):
        self.root = tk.Tk()
        self.root.title(title)
        
        # Création du canvas
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack(padx=10, pady=10)
        
        # Bouton pour relancer le jeu
        self.restart_button = tk.Button(self.root, text="Recommencer", command=self.restart_game)
        self.restart_button.pack(pady=5)
        
        # Forcer la mise à jour des tâches en attente pour obtenir les dimensions correctes
        self.root.update_idletasks()
        
        # Initialisation de l'état du jeu
        self.game_running = True
        self.setup_game()
        self.refresh()  # Démarre la boucle de rafraîchissement
        
    def setup_game(self):
        """Initialise ou réinitialise l’état du jeu."""
        self.score = 0
        self.game_over = False
        self.state = "MENU"  # États possibles: MENU, PLAYING, PAUSE, GAME_OVER
        
    def refresh(self):
        """Met à jour l’affichage à chaque 'tick' du jeu."""
        if self.game_running:
            self.update_game_logic()
            self.update_display()
            self.root.after(50, self.refresh)  # 20 ticks/s approx.
        
    def update_game_logic(self):
        """Logique interne du jeu, à redéfinir dans les classes dérivées."""
        pass
        
    def update_display(self):
        """Met à jour l’affichage graphique à chaque tick, à redéfinir."""
        self.canvas.delete("all")
        # Affichage du score
        self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", font=("Arial", 12), fill="black", tags="score")
        
    def on_key_press(self, event):
        """Gère les entrées clavier du joueur, à redéfinir."""
        pass
    
    def game_over_sequence(self):
        """Affiche un message de fin et arrête la boucle de jeu."""
        self.game_over = True
        self.game_running = False
        self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                                text="Game Over", font=("Arial", 24), fill="red")
        
    def restart_game(self):
        """Permet de relancer la partie."""
        print("Recommencer le jeu")  # Debug
        self.game_running = True
        self.setup_game()
        self.refresh()
        
    def run(self):
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.mainloop()

if __name__ == "__main__":
    app = Vue("Base du Jeu")
    app.run()