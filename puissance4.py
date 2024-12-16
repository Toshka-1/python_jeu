import tkinter as tk
from tkinter import messagebox

class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        # 0 = case vide, 1 = pion joueur 1, 2 = pion joueur 2
        self.grid = [[0]*cols for _ in range(rows)]
        
    def is_valid_move(self, col):
        # Un coup est valide si la colonne n'est pas pleine
        return self.grid[0][col] == 0
    
    def place_token(self, col, player):
        # Place le pion du joueur dans la colonne donnée, à la première ligne disponible
        for row in range(self.rows-1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                return row, col
        return None
        
    def check_winner(self, player):
        # Vérifie si le joueur 'player' a gagné.
        # On vérifie les alignements horizontaux, verticaux et diagonaux.
        
        # Check horizontal
        for r in range(self.rows):
            for c in range(self.cols-3):
                if (self.grid[r][c] == player and
                    self.grid[r][c+1] == player and
                    self.grid[r][c+2] == player and
                    self.grid[r][c+3] == player):
                    return True
                    
        # Check vertical
        for c in range(self.cols):
            for r in range(self.rows-3):
                if (self.grid[r][c] == player and
                    self.grid[r+1][c] == player and
                    self.grid[r+2][c] == player and
                    self.grid[r+3][c] == player):
                    return True
        
        # Check diagonale descendante
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                if (self.grid[r][c] == player and
                    self.grid[r+1][c+1] == player and
                    self.grid[r+2][c+2] == player and
                    self.grid[r+3][c+3] == player):
                    return True

        # Check diagonale montante
        for r in range(3, self.rows):
            for c in range(self.cols-3):
                if (self.grid[r][c] == player and
                    self.grid[r-1][c+1] == player and
                    self.grid[r-2][c+2] == player and
                    self.grid[r-3][c+3] == player):
                    return True

        return False
    
    def is_full(self):
        return all(self.grid[0][c] != 0 for c in range(self.cols))


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.game_over = False

    def reset(self):
        self.board = Board()
        self.current_player = 1
        self.game_over = False

    def play_turn(self, col):
        if self.game_over:
            return None
        
        if self.board.is_valid_move(col):
            pos = self.board.place_token(col, self.current_player)
            if pos:
                # Vérifie si le joueur courant gagne
                if self.board.check_winner(self.current_player):
                    self.game_over = True
                    return self.current_player, pos
                elif self.board.is_full():
                    # Match nul
                    self.game_over = True
                    return 0, pos
                else:
                    # Changement de joueur
                    self.current_player = 2 if self.current_player == 1 else 1
                    return None, pos
        return None


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Puissance 4")
        
        self.game = Game()
        
        self.cell_size = 60
        self.rows = self.game.board.rows
        self.cols = self.game.board.cols
        
        self.canvas = tk.Canvas(self.master, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="blue")
        self.canvas.pack(side=tk.TOP)
        
        # Dessin initial du plateau (cases vides)
        self.tokens = [[None for _ in range(self.cols)] for __ in range(self.rows)]
        self.draw_board()
        
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Bouton de reset
        self.reset_button = tk.Button(self.master, text="Recommencer", command=self.reset_game)
        self.reset_button.pack(side=tk.BOTTOM)

    def draw_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c*self.cell_size
                y1 = r*self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.tokens[r][c] = self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white", outline="black")
        
    def handle_click(self, event):
        if self.game.game_over:
            return
        
        col = event.x // self.cell_size
        result = self.game.play_turn(col)
        
        if result is not None:
            # Soit un vainqueur, soit un match nul
            winner, pos = result
            if winner == 1:
                self.update_token(pos[0], pos[1], "red")
                messagebox.showinfo("Fin de la partie", "Le Joueur 1 a gagné!")
            elif winner == 2:
                self.update_token(pos[0], pos[1], "yellow")
                messagebox.showinfo("Fin de la partie", "Le Joueur 2 a gagné!")
            elif winner == 0:
                # Egalité
                self.update_token(pos[0], pos[1], "red" if self.game.current_player == 1 else "yellow")
                messagebox.showinfo("Fin de la partie", "Match nul!")
        else:
            # Aucun gagnant pour l'instant, juste actualiser l'affichage du dernier coup
            last_pos = self.get_last_move_position()
            if last_pos:
                r, c = last_pos
                color = "red" if self.game.current_player == 2 else "yellow"  # le pion vient d'être placé par le joueur précédent
                self.update_token(r, c, color)
    
    def get_last_move_position(self):
        # On retrouve la dernière position jouée en comparant l'état du board
        # Mais le résultat a déjà été donné par game.play_turn normalement
        # Ici, on parcourt le board pour trouver une case sans affichage ?
        # Pour simplifier, on peut récupérer la dernière case jouée à partir du board actuel.
        # Comme on place un pion par tour, on regarde la couleur dans le board.
        
        # Cependant, on a déjà ce pos dans play_turn (renvoie None, pos)
        # On l'a utilisé uniquement si c'était un coup gagnant.
        # Pour le coup normal, on a "None, pos". On pourrait stocker pos dans une variable globale
        # Mais pour aller plus vite : ajoutons une variable "last_pos" dans play_turn :
        
        # Pour éviter de tout changer, on va faire un petit bricolage :
        # On va lire le dernier coup par rapport au joueur courant (inversé)
        # Ce n'est pas très optimal, mais comme on sait qu'un pion a été posé si on est ici...
        
        # En réalité, notre code a un petit souci : lorsqu'il n'y a pas de gagnant, on n'enregistre pas la position
        # dans result. Corrigeons cela.
        pass

    # Modification du code pour mémoriser le dernier coup joué :
    def handle_click(self, event):
        if self.game.game_over:
            return
        
        col = event.x // self.cell_size
        old_player = self.game.current_player
        result = self.game.play_turn(col)

        # result peut être:
        # - (None, (row,col)) si pas de gagnant
        # - (1 ou 2, (row,col)) si gagnant
        # - (0, (row,col)) si nul
        # ou None si coup invalide

        if result is None:
            # Coup invalide ou pas de changement d'état
            return
        
        winner, pos = result
        if winner is None:
            # Pas de gagnant, juste un coup normal
            # pos = (r, c)
            # Le pion qui vient d'être posé appartient à old_player
            color = "red" if old_player == 1 else "yellow"
            self.update_token(pos[0], pos[1], color)
        else:
            # Soit gagnant, soit nul
            color = "red" if old_player == 1 else "yellow"
            self.update_token(pos[0], pos[1], color)

            if winner == 1:
                messagebox.showinfo("Fin de la partie", "Le Joueur 1 a gagné!")
            elif winner == 2:
                messagebox.showinfo("Fin de la partie", "Le Joueur 2 a gagné!")
            elif winner == 0:
                messagebox.showinfo("Fin de la partie", "Match nul!")
            
    def update_token(self, r, c, color):
        self.canvas.itemconfig(self.tokens[r][c], fill=color)
        
    def reset_game(self):
        self.game.reset()
        for r in range(self.rows):
            for c in range(self.cols):
                self.canvas.itemconfig(self.tokens[r][c], fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()