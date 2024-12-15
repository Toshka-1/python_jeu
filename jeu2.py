import tkinter as tk
import random
from affichage import Vue

class CollecteGame(Vue):
    def __init__(self, title="Jeu de Collecte", width=400, height=300):
        super().__init__(title, width, height)
        
    def setup_game(self):
        super().setup_game()
        self.player_size = 20
        self.player_x = (self.canvas.winfo_width() - self.player_size) // 2
        self.player_y = (self.canvas.winfo_height() - self.player_size) // 2
        self.player_speed = 10  # Pixels par déplacement
        
        # Position de l'objet à collecter
        self.objet_size = 15
        self.place_objet()
        
    def place_objet(self):
        # Utiliser les dimensions connues du canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Debugging
        print(f"Placing object: Canvas Width = {canvas_width}, Canvas Height = {canvas_height}")
        
        # Assurez-vous que l'objet peut être placé dans le canvas
        if canvas_width < self.objet_size or canvas_height < self.objet_size:
            raise ValueError("Le canvas est trop petit pour placer l'objet.")
        
        self.objet_x = random.randint(0, canvas_width - self.objet_size)
        self.objet_y = random.randint(0, canvas_height - self.objet_size)
        
        print(f"Objet placé à ({self.objet_x}, {self.objet_y})")  # Debug
        
    def on_key_press(self, event):
        print(f"Key pressed: {event.keysym}")  # Debug
        if self.state == "MENU":
            if event.keysym == "Return":  # Appuyer sur Entrée pour démarrer
                print("Passage à l'état PLAYING")  # Debug
                self.state = "PLAYING"
        elif self.state == "PLAYING":
            if event.keysym == "p":
                print("Passage à l'état PAUSE")  # Debug
                self.state = "PAUSE"
            else:
                self.move_player(event.keysym)
        elif self.state == "PAUSE":
            if event.keysym == "p":
                print("Reprise de l'état PLAYING")  # Debug
                self.state = "PLAYING"
                
    def move_player(self, direction):
        print(f"Moving player: {direction}")  # Debug
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
        
        print(f"Nouvelle position du joueur: ({self.player_x}, {self.player_y})")  # Debug
        
        # Vérifier la collecte de l'objet
        if (self.player_x < self.objet_x + self.objet_size and
            self.player_x + self.player_size > self.objet_x and
            self.player_y < self.objet_y + self.objet_size and
            self.player_y + self.player_size > self.objet_y):
            self.score += 1
            print(f"Objet collecté! Score: {self.score}")  # Debug
            self.place_objet()
        
    def update_game_logic(self):
        if self.state == "PLAYING":
            # Par exemple, ajouter un temps limite ou d'autres logiques
            if self.score >= 10:
                self.state = "GAME_OVER"
                print("Score atteint 10, passage à GAME_OVER")  # Debug
        
    def update_display(self):
        self.canvas.delete("all")
        if self.state == "MENU":
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                                    text="Appuyez sur Entrée pour commencer", font=("Arial", 16), fill="black")
        elif self.state == "PLAYING":
            # Afficher le score
            self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", font=("Arial", 12), fill="black")
            # Dessiner le joueur
            self.canvas.create_rectangle(self.player_x, self.player_y, 
                                         self.player_x + self.player_size, self.player_y + self.player_size, 
                                         fill="blue")
            # Dessiner l'objet à collecter
            self.canvas.create_oval(self.objet_x, self.objet_y, 
                                    self.objet_x + self.objet_size, self.objet_y + self.objet_size, 
                                    fill="red")
        elif self.state == "PAUSE":
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                                    text="Jeu en pause\nAppuyez sur 'p' pour reprendre", 
                                    font=("Arial", 16), fill="grey")
        elif self.state == "GAME_OVER":
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, 
                                    text=f"Game Over\nScore final: {self.score}", 
                                    font=("Arial", 16), fill="red")

if __name__ == "__main__":
    app = CollecteGame()
    app.run()