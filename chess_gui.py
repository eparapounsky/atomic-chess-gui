import tkinter as tk
from tkinter import messagebox, font
from ChessVar import ChessVar, Piece

# This module creates a window with a GUI for the game


class ChessGUI:
    def __init__(self):
        self.root = tk.Tk()  # create the main window
        self.root.title("Atomic Chess")
        self.root.geometry("800x1200")  # set the window size
        self.root.configure(bg="#2b2b2b")

        # initialize game
        self.game = ChessVar()
        self.selected_square = None  # currently selected square (row, col)
        self.board_buttons = []  # list to hold button references for the chess board

        # use unicode symbols for pieces
        # 1-6: black pieces, 10-60: white pieces
        self.piece_symbols = {
            0: "",  # empty
            1: "♜",  # black rook
            2: "♞",  # black knight
            3: "♝",  # black bishop
            4: "♛",  # black queen
            5: "♚",  # black king
            6: "♟",  # black pawn
            10: "♖",  # white rook
            20: "♘",  # white knight
            30: "♗",  # white bishop
            40: "♕",  # white queen
            50: "♔",  # white king
            60: "♙",  # white pawn
        }

        self.setup_ui()
        self.update_board()  # initialize the board display

    def setup_ui(self):
        """Set up the main UI components: title, game info, chess board, and control buttons."""
        # Title
        title_label = tk.Label(
            self.root,
            text="Atomic Chess",
            font=("Arial", 30, "bold"),
            bg="#2b2b2b",
            fg="white",
        )
        title_label.pack(pady=15)  # add title to top of window

        # Game info bar
        info_bar = tk.Frame(self.root, bg="#2b2b2b")
        info_bar.pack(pady=5)

        self.game_state_label = tk.Label(
            info_bar,
            text="Game State: UNFINISHED",
            font=("Arial", 12, "bold"),
            bg="#2b2b2b",
            fg="white",
        )
        self.game_state_label.pack(side=tk.LEFT, padx=20)

        self.current_player_label = tk.Label(
            info_bar,
            text="Current Player: WHITE",
            font=("Arial", 12, "bold"),
            bg="#2b2b2b",
            fg="white",
        )
        self.current_player_label.pack(side=tk.LEFT, padx=20)

        # Chess board frame
        board_frame = tk.Frame(self.root, bg="#2b2b2b")
        board_frame.pack(pady=20)

        # Column labels (a-h)
        column_frame = tk.Frame(board_frame, bg="#2b2b2b")
        column_frame.grid(row=0, column=1, sticky="ew")

        for i, letter in enumerate("abcdefgh"):
            label = tk.Label(
                column_frame,
                text=letter,
                font=("Arial", 12, "bold"),
                bg="#2b2b2b",
                fg="white",
                width=8,
            )
            label.grid(row=0, column=i)

        # Create the chess board grid
        self.board_frame = tk.Frame(board_frame, bg="#2b2b2b")
        self.board_frame.grid(row=1, column=1)

        # Row labels and board squares
        for row in range(8):
            # Row number labels (8-1)
            row_label = tk.Label(
                board_frame,
                text=str(8 - row),
                font=("Arial", 12, "bold"),
                bg="#2b2b2b",
                fg="white",
                width=8,
            )
            row_label.grid(row=row + 1, column=0, sticky="e", padx=(0, 5))

            button_row = []
            for col in range(8):
                # Determine square color
                is_light = (row + col) % 2 == 0
                color = "#f0d9b5" if is_light else "#b58863"

                button = tk.Button(
                    self.board_frame,
                    width=6,
                    height=3,
                    bg=color,
                    font=("Arial", 16),
                    command=lambda r=row, c=col: self.square_clicked(r, c),
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                button_row.append(button)

            self.board_buttons.append(button_row)

            # Right row labels
            row_label_right = tk.Label(
                board_frame,
                text=str(8 - row),
                font=("Arial", 12, "bold"),
                bg="#2b2b2b",
                fg="white",
                width=2,
            )
            row_label_right.grid(row=row + 1, column=2, sticky="w", padx=(5, 0))

        # Bottom column labels
        bottom_column_frame = tk.Frame(board_frame, bg="#2b2b2b")
        bottom_column_frame.grid(row=9, column=1, sticky="ew")

        for i, letter in enumerate("abcdefgh"):
            label = tk.Label(
                bottom_column_frame,
                text=letter,
                font=("Arial", 12, "bold"),
                bg="#2b2b2b",
                fg="white",
                width=8,
            )
            label.grid(row=0, column=i)

        # Control buttons
        button_frame = tk.Frame(self.root, bg="#2b2b2b")
        button_frame.pack(pady=20)

        reset_button = tk.Button(
            button_frame,
            text="New Game",
            font=("Arial", 12),
            command=self.new_game,
            bg="#4CAF50",
            fg="white",
            padx=20,
        )
        reset_button.pack(side=tk.LEFT, padx=10)

        reload_button = tk.Button(
            button_frame,
            text="Reload UI",
            font=("Arial", 12),
            command=self.reload_ui,
            bg="#2196F3",
            fg="white",
            padx=20,
        )
        reload_button.pack(side=tk.LEFT, padx=10)

        quit_button = tk.Button(
            button_frame,
            text="Quit",
            font=("Arial", 12),
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            padx=20,
        )
        quit_button.pack(side=tk.LEFT, padx=10)

    def square_clicked(self, row, col):
        """Handle square click events"""
        if self.game.get_game_state() != "UNFINISHED":
            messagebox.showinfo(
                "Game Over", f"Game is finished! Winner: {self.game.get_game_state()}"
            )
            return

        if self.selected_square is None:
            # First click - select a piece
            piece = self.game.get_piece_type(row, col)
            if piece == 0:
                messagebox.showwarning(
                    "Invalid Selection", "Please select a piece to move."
                )
                return

            # Check if it's the current player's piece
            if self.game.check_if_valid_player(piece) is False:
                messagebox.showwarning(
                    "Invalid Selection", "Please select one of your own pieces."
                )
                return

            self.selected_square = (row, col)
            self.highlight_selected_square(row, col)

        else:
            # Second click - make a move
            start_row, start_col = self.selected_square

            if (row, col) == self.selected_square:
                # Clicking the same square deselects it
                self.clear_selection()
                return

            # Convert coordinates to chess notation
            start_pos = chr(ord("a") + start_col) + str(8 - start_row)
            end_pos = chr(ord("a") + col) + str(8 - row)

            # Try to make the move
            if self.game.make_move(start_pos, end_pos):
                self.clear_selection()
                self.update_board()
                self.update_game_info()

                # Check for game end
                if self.game.get_game_state() != "UNFINISHED":
                    messagebox.showinfo(
                        "Game Over", f"Winner: {self.game.get_game_state()}!"
                    )
            else:
                messagebox.showwarning("Invalid Move", "That move is not allowed.")
                self.clear_selection()

    def highlight_selected_square(self, row, col):
        """Highlight the selected square"""
        self.board_buttons[row][col].configure(bg="#ffff99")

    def clear_selection(self):
        """Clear the current selection and reset square colors"""
        self.selected_square = None
        self.update_board_colors()

    def update_board_colors(self):
        """Update the colors of all board squares"""
        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = "#f0d9b5" if is_light else "#b58863"
                self.board_buttons[row][col].configure(bg=color)

    def update_board(self):
        """Update the visual representation of the board"""
        for row in range(8):
            for col in range(8):
                piece = self.game.get_piece_type(row, col)
                symbol = self.piece_symbols.get(piece, "")
                self.board_buttons[row][col].configure(text=symbol)

        self.update_board_colors()

    def update_game_info(self):
        """Update the game state and current player labels"""
        self.game_state_label.configure(
            text=f"Game State: {self.game.get_game_state()}"
        )
        self.current_player_label.configure(
            text=f"Current Player: {self.game.get_current_player()}"
        )

    def new_game(self):
        """Start a new game"""
        self.game = ChessVar()
        self.selected_square = None
        self.update_board()
        self.update_game_info()

    # For development purposes, reload the UI
    # This method can be called to reset the UI without restarting the application
    def reload_ui(self):
        """Reload the UI by destroying and recreating all widgets"""
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Clear board buttons reference
        self.board_buttons.clear()

        # Recreate UI
        self.setup_ui()
        self.update_board()
        self.update_game_info()

    def run(self):
        """Start the GUI (enter the Tkinter event loop)"""
        self.root.mainloop()


if __name__ == "__main__":
    chess_gui = ChessGUI()
    chess_gui.run()
