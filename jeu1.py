import tkinter as tk
from affichage import Vue

class DeplacementGame(Vue):
    def __init__(self, title="Jeu de Déplacement", width=400, height=300):
        super().__init__(title, width, height)
        
    def setup_game(self):
        super().setup_game()
        self.player_size = 20
        self.player_x = self.canvas.winfo_reqwidth() // 2
        self.player_y = self.canvas.winfo_reqheight() // 2
        self.player_speed = 10  # Pixels par déplacement
        
    def on_key_press(self, event):
        if self.state == "MENU":
            if event.keysym == "Return":  # Appuyer sur Entrée pour démarrer
                self.state = "PLAYING"
        elif self.state == "PLAYING":
            if event.keysym == "p":
                self.state = "PAUSE"
            else:
                self.move_player(event.keysym)
        elif self.state == "PAUSE":
            if event.keysym == "p":
                self.state = "PLAYING"
                
    def move_player(self, direction):
        if direction == "Up":
            self.player_y -= self.player_speed
        elif direction == "Down":
            self.player_y += self.player_speed
        elif direction == "Left":
            self.player_x -= self.player_speed
        elif direction == "Right":
            self.player_x += self.player_speed
        
        # Vérifier les limites du canvas
        self.player_x = max(0, min(self.player_x, self.canvas.winfo_width() - self.player_size))
        self.player_y = max(0, min(self.player_y, self.canvas.winfo_height() - self.player_size))
        
    def update_game_logic(self):
        if self.state == "PLAYING":
            # Logique du jeu en cours
            pass
        elif self.state == "GAME_OVER":
            self.game_over_sequence()
        
    def update_display(self):
        self.canvas.delete("all")
        if self.state == "MENU":
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                                    text="Appuyez sur Entrée pour commencer", font=("Arial", 16), fill="black")
        elif self.state == "PLAYING":
            # Afficher le score
            self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", font=("Arial", 12))
            # Dessiner le joueur
            self.canvas.create_rectangle(self.player_x, self.player_y, 
                                         self.player_x + self.player_size, self.player_y + self.player_size, 
                                         fill="blue")
        elif self.state == "PAUSE":
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                                    text="Jeu en pause\nAppuyez sur 'p' pour reprendre", 
                                    font=("Arial", 16), fill="grey")

if __name__ == "__main__":
    app = DeplacementGame()
    app.run()