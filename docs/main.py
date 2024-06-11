import tkinter as tk
import random
#from config.shapes import COLORS, SHAPES

import json

with open('config\config.json', 'r') as file:
    data = json.load(file)
    COLORS = data['COLORS']
    SHAPES = data['SHAPES']

class Tetris:
    def __init__(self, canvas):
        self.score = 0
        self.canvas = canvas
        self.game_board = [[0] * 10 for _ in range(20)]
        self.current_piece = None
        self.game_over = False
        self.game_running = True
        self.spawn_new_piece()

    def spawn_new_piece(self):
        self.current_piece = Piece()
        self.current_piece.color = random.choice(COLORS)
        if self.check_collision():
            self.game_running = False
            self.game_over = True

    def move_piece_down(self):
        self.current_piece.y += 1
        if self.check_collision():
            self.current_piece.y -= 1
            self.lock_piece()
            self.clear_lines()
            self.spawn_new_piece()
            if self.check_collision():
                self.game_running = False
                self.game_over = True 

    def check_collision(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = x + self.current_piece.x
                    board_y = y + self.current_piece.y
                    if (board_x < 0 or board_x >= 10 or 
                        board_y < 0 or board_y >= 20 or 
                        self.game_board[board_y][board_x]):
                        return True
        return False

    def lock_piece(self):
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.game_board[y + self.current_piece.y][x + self.current_piece.x] = self.current_piece.color

    def clear_lines(self):
        lines_cleared = 0
        new_board = [row for row in self.game_board if any(cell == 0 for cell in row)]
        lines_cleared = 20 - len(new_board)
        new_board = [[0] * 10 for _ in range(lines_cleared)] + new_board
        self.game_board = new_board
        
        self.score += lines_cleared * 30 

    def draw_game_board(self):
        self.canvas.delete("all")
        
        for y in range(20):
            self.canvas.create_line(0, y * 30, 300, y * 30, fill="wheat")
        for x in range(10):
            self.canvas.create_line(x * 30, 0, x * 30, 600, fill="wheat")

        for y in range(len(self.game_board)):
            for x in range(len(self.game_board[y])):
                color = self.game_board[y][x]
                if color:
                    self.canvas.create_rectangle(
                        x * 30, y * 30, (x + 1) * 30, (y + 1) * 30,
                        fill=color, outline="white"
                    )
        if self.current_piece:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.canvas.create_rectangle(
                            (self.current_piece.x + x) * 30,
                            (self.current_piece.y + y) * 30,
                            (self.current_piece.x + x + 1) * 30,
                            (self.current_piece.y + y + 1) * 30,
                            fill=self.current_piece.color, outline="white"
                        )


    def move_piece_right(self):
        self.current_piece.x += 1
        if self.check_collision():
            self.current_piece.x -= 1

    def move_piece_left(self):
        self.current_piece.x -= 1
        if self.check_collision():
            self.current_piece.x += 1

    def rotate_piece(self):
        rotated_shape = self.current_piece.rotate()
        if not self.check_collision_with_rotation(rotated_shape):
            self.current_piece.shape = rotated_shape

    def check_collision_with_rotation(self, rotated_shape):
        for y, row in enumerate(rotated_shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = x + self.current_piece.x
                    board_y = y + self.current_piece.y
                    if (board_x < 0 or board_x >= 10 or 
                        board_y < 0 or board_y >= 20 or 
                        self.game_board[board_y][board_x]):
                        return True
        return False
    
    def stop_game(self):
        self.game_over = True
        self.game_running = False

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.x = 3
        self.y = 0
        self.color = random.choice(COLORS)

    def rotate(self):
        rotated_shape = []
        for i in range(len(self.shape[0])):
            new_row = [self.shape[j][i] for j in range(len(self.shape))]
            rotated_shape.append(new_row[::-1])
        return rotated_shape

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris")
        
        self.info_frame = tk.Frame(self, width=300, height=600, bg="blanchedalmond")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_frame.propagate(False)
        
        self.info_frame.config(highlightbackground="burlywood",highlightthickness=2)
        
        self.game_frame = tk.Frame(self, width=300, height=600)
        self.game_frame.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self.game_frame, width=300, height=600, bg="oldlace")
        self.canvas.pack()
        self.game_frame.propagate(False)

        self.game_frame.config(highlightbackground="burlywood",highlightthickness=2)
        
        self.score_label = tk.Label(self.info_frame, text="TETRIS\n\n\n\nGame Statistics:\nScore: 0", font=("Arial", 20), bd=0, relief="flat", fg='#a36940')
        self.score_label.configure(bg="blanchedalmond")
        self.score_label.pack(pady=20)
        
        self.game_over_label = tk.Label(self.info_frame, text="", font=("Arial", 20), bg="blanchedalmond", fg="red")
        self.game_over_label.pack(pady=20)
        
        self.start_label = tk.Label(self.info_frame, text="Press Up arrow\n to start the game\n\n And press Enter\n to end the game", font=("Arial", 16), bg="blanchedalmond", fg="#5b7528")
        self.start_label.pack()
        
        self.tetris = Tetris(self.canvas)
        self.bind("<KeyPress>", self.on_key_press)
        self.game_started = False
        

    def on_key_press(self, event):
        if event.keysym == "Up":
            if not self.game_started:
                self.start_game()
            elif self.tetris.game_over:
                self.restart_game()
        elif event.keysym == "Return":
            if self.game_started and not self.tetris.game_over:
                self.stop_game()

        if self.game_started:  
            if self.tetris.game_running:
                if event.keysym == "Left":
                    self.tetris.move_piece_left()
                elif event.keysym == "Right":
                    self.tetris.move_piece_right()
                elif event.keysym == "Down":
                    self.tetris.move_piece_down()
                elif event.keysym == "Up":
                    self.tetris.rotate_piece()

                self.tetris.draw_game_board()
                self.update_score_label()

    def start_game(self):
        self.game_started = True
        self.start_label.config(text="")
        self.update_game()

    def restart_game(self):
        self.tetris = Tetris(self.canvas)
        self.game_over_label.config(text="")
        self.start_game()

    def stop_game(self):
        self.tetris.stop_game()
        self.display_game_over()

    def update_game(self):
        if self.tetris.game_running:
            self.tetris.move_piece_down()
            self.tetris.draw_game_board()
            self.after(600, self.update_game)
        else:
            self.display_game_over()

    def update_score_label(self):
        self.score_label.config(text="TETRIS\n\n\n\nGame Statistics:\nScore: {}".format(self.tetris.score))

    def display_game_over(self):
        self.game_over_label.config(text="Game Over!\n\n Press Up arrow\n to play again.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
