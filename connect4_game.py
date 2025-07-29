import tkinter as tk
from tkinter import messagebox
import numpy as np
import platform

class Connect4Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 - Modern Edition")
        self.root.configure(bg='#1a1a2e')
        
        # Game constants
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        
        # Game state
        self.board = self.create_board()
        self.game_over = False
        self.turn = 0  # 0 for Player 1 (Red), 1 for Player 2 (Yellow)
        
        # Colors
        self.colors = {
            'blue': '#003f88',
            'red': '#d00000',
            'yellow': '#ffd60a',
            'empty': '#2c3e50',
            'hover': '#34495e',
            'text': '#ecf0f1'
        }
        
        self.is_macos = platform.system() == 'Darwin'
        
        self.setup_ui()
        
    def create_board(self):
        return np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
    
    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece
    
    def is_valid_location(self, board, col):
        return board[self.ROW_COUNT - 1][col] == 0
    
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r
        return None
    
    def winning_move(self, board, piece):
        # Horizontal
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if (board[r][c] == piece and board[r][c+1] == piece and 
                    board[r][c+2] == piece and board[r][c+3] == piece):
                    return True
        # Vertical
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT):
                if (board[r][c] == piece and board[r+1][c] == piece and 
                    board[r+2][c] == piece and board[r+3][c] == piece):
                    return True
        # Positive diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                if (board[r][c] == piece and board[r+1][c+1] == piece and 
                    board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                    return True
        # Negative diagonal
        for r in range(3, self.ROW_COUNT):
            for c in range(self.COLUMN_COUNT - 3):
                if (board[r][c] == piece and board[r-1][c+1] == piece and 
                    board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                    return True
        return False
    
    def is_board_full(self):
        return all(self.board[self.ROW_COUNT - 1][col] != 0 for col in range(self.COLUMN_COUNT))
    
    def update_button_color(self, button, color):
        button.configure(bg=color)
        if self.is_macos:
            button.update_idletasks()
            self.root.update_idletasks()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#1a1a2e', padx=15, pady=15)
        main_frame.pack(expand=True, fill='both')
        
        header_frame = tk.Frame(main_frame, bg='#1a1a2e')
        header_frame.pack(fill='x', pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="CONNECT 4",
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Modern Edition",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#1a1a2e'
        )
        subtitle_label.pack()
        
        info_frame = tk.Frame(main_frame, bg='#1a1a2e')
        info_frame.pack(pady=(15, 20))
        
        self.player_label = tk.Label(
            info_frame,
            text="🎮 Player 1's Turn (Red)",
            font=('Arial', 14, 'bold'),
            fg='#e74c3c',
            bg='#1a1a2e'
        )
        self.player_label.pack()
        
        board_frame = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=3)
        board_frame.pack()
        
        self.buttons = []
        for row in range(self.ROW_COUNT):
            button_row = []
            for col in range(self.COLUMN_COUNT):
                label = tk.Label(
                    board_frame,
                    width=4,
                    height=2,
                    bg=self.colors['empty'],
                    relief='raised',
                    bd=1,
                )
                label.grid(row=row, column=col, padx=1, pady=1)
                
                label.bind('<Button-1>', lambda e, c=col: self.make_move(c))
                label.bind('<Enter>', lambda e, b=label: self.on_hover(b, True))
                label.bind('<Leave>', lambda e, b=label: self.on_hover(b, False))
                
                button_row.append(label)
            self.buttons.append(button_row)
        
        control_frame = tk.Frame(main_frame, bg='#1a1a2e')
        control_frame.pack(pady=(20, 0))
        
        reset_button = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=2,
            padx=15,
            pady=5,
            command=self.reset_game
        )
        reset_button.pack(side='left', padx=(0, 15))
        
        instructions = tk.Label(
            control_frame,
            text="Click any column to drop your piece",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#1a1a2e'
        )
        instructions.pack(side='left')
    
    def on_hover(self, button, entering):
        if self.game_over:
            return

        info = button.grid_info()
        row = int(info['row'])
        col = int(info['column'])

        board_row = self.ROW_COUNT - 1 - row

        if entering:
            if self.board[board_row][col] == 0:
                self.update_button_color(button, self.colors['hover'])
        else:
            piece = self.board[board_row][col]
            if piece == 1:
                self.update_button_color(button, self.colors['red'])
            elif piece == 2:
                self.update_button_color(button, self.colors['yellow'])
            else:
                self.update_button_color(button, self.colors['empty'])
    
    def make_move(self, col):
        if self.game_over:
            return
        
        if not self.is_valid_location(self.board, col):
            return
        
        row = self.get_next_open_row(self.board, col)
        if row is None:
            return
        
        piece = 1 if self.turn == 0 else 2
        self.drop_piece(self.board, row, col, piece)
        
        color = self.colors['red'] if piece == 1 else self.colors['yellow']
        ui_row = self.ROW_COUNT - 1 - row
        self.update_button_color(self.buttons[ui_row][col], color)
        
        self.root.update_idletasks()
        
        if self.winning_move(self.board, piece):
            self.game_over = True
            winner = "Player 1 (Red)" if piece == 1 else "Player 2 (Yellow)"
            messagebox.showinfo("Game Over!", f"{winner} wins!")
            return
        
        if self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Game Over!", "It's a draw!")
            return
        
        self.turn = (self.turn + 1) % 2
        
        if self.turn == 0:
            self.player_label.configure(text="Player 1's Turn (Red)", fg='#e74c3c')
        else:
            self.player_label.configure(text="Player 2's Turn (Yellow)", fg='#f1c40f')
    
    def reset_game(self):
        self.board = self.create_board()
        
        for row in range(self.ROW_COUNT):
            for col in range(self.COLUMN_COUNT):
                self.update_button_color(self.buttons[row][col], self.colors['empty'])
        
        self.root.update_idletasks()
        
        self.game_over = False
        self.turn = 0
        self.player_label.configure(text="Player 1's Turn (Red)", fg='#e74c3c')

def main():
    root = tk.Tk()
    root.geometry("500x600")
    root.resizable(False, False)
    
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"500x600+{x}+{y}")
    
    game = Connect4Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
