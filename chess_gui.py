import tkinter as tk
from tkinter import messagebox
from chess_logic import AtomicChessGame

# Constants for styling
WINDOW_SIZE = "800x1050"
BG_COLOR = "#2b2b2b"
LIGHT_SQUARE_COLOR = "#f0d9b5"
DARK_SQUARE_COLOR = "#b58863"
HIGHLIGHT_COLOR = "#ffffff"
TITLE_FONT = ("Arial", 30, "bold")
LABEL_FONT = ("Arial", 12, "bold")
BUTTON_FONT = ("Arial", 12, "bold")
PIECE_FONT = ("Arial", 16)


# This module creates a window with a GUI for the game
class ChessGUI:
    def __init__(self) -> None:
        """Initialize the Atomic Chess GUI window and game state."""
        self.root = tk.Tk()
        self.root.title("Atomic Chess")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BG_COLOR)

        self.game = AtomicChessGame()
        self.selected_square: tuple[int, int] | None = None
        self.board_buttons: list[list[tk.Button]] = []

        # use unicode symbols for pieces
        # 1-6: black pieces, 10-60: white pieces
        self.piece_symbols = {
            0: "",
            1: "♜",
            2: "♞",
            3: "♝",
            4: "♛",
            5: "♚",
            6: "♟",
            10: "♖",
            20: "♘",
            30: "♗",
            40: "♕",
            50: "♔",
            60: "♙",
        }

        self.setup_ui()
        self.update_board()

    def setup_ui(self) -> None:
        """Set up the main UI components: title, game info, chess board, and control buttons."""
        # Title
        title_label = tk.Label(
            self.root,
            text="Atomic Chess",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg="white",
        )
        title_label.pack(pady=15)

        # Game info bar
        info_bar = tk.Frame(self.root, bg=BG_COLOR)
        info_bar.pack(pady=5)

        self.game_state_label = tk.Label(
            info_bar,
            text="Game State: UNFINISHED",
            font=LABEL_FONT,
            bg=BG_COLOR,
            fg="white",
        )
        self.game_state_label.pack(side=tk.LEFT, padx=20)

        self.current_player_label = tk.Label(
            info_bar,
            text="Current Player: WHITE",
            font=LABEL_FONT,
            bg=BG_COLOR,
            fg="white",
        )
        self.current_player_label.pack(side=tk.LEFT, padx=20)

        # Chess board frame
        board_frame = tk.Frame(self.root, bg=BG_COLOR)
        board_frame.pack(pady=20)

        # Column labels (a-h)
        column_frame = tk.Frame(board_frame, bg=BG_COLOR)
        column_frame.grid(row=0, column=1, sticky="ew")
        for i, letter in enumerate("abcdefgh"):
            label = tk.Label(
                column_frame,
                text=letter,
                font=LABEL_FONT,
                bg=BG_COLOR,
                fg="white",
                width=8,
                height=2,
            )
            label.grid(row=0, column=i)

        # Create the chess board grid
        self.board_frame = tk.Frame(board_frame, bg=BG_COLOR)
        self.board_frame.grid(row=1, column=1)

        # Row labels and board squares
        left_row_frame = tk.Frame(board_frame, bg=BG_COLOR)
        left_row_frame.grid(row=0, column=0, rowspan=2)
        right_row_frame = tk.Frame(board_frame, bg=BG_COLOR)
        right_row_frame.grid(row=0, column=9, rowspan=2)

        for row in range(8):
            # left row labels (8-1)
            row_label = tk.Label(
                left_row_frame,
                text=str(8 - row),
                font=LABEL_FONT,
                bg=BG_COLOR,
                fg="white",
                width=2,
            )
            row_label.grid(row=row + 1, column=0, sticky="w", pady=(35))

            # square buttons
            button_row = []
            for col in range(8):
                # Use lambda with default args to capture current row/col
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE_COLOR if is_light else DARK_SQUARE_COLOR
                button = tk.Button(
                    self.board_frame,
                    width=6,
                    height=3,
                    bg=color,
                    font=PIECE_FONT,
                    command=lambda r=row, c=col: self.square_clicked(r, c),
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                button_row.append(button)
            self.board_buttons.append(button_row)

            # right row labels (8-1)
            row_label = tk.Label(
                right_row_frame,
                text=str(8 - row),
                font=LABEL_FONT,
                bg=BG_COLOR,
                fg="white",
                width=2,
            )
            row_label.grid(row=row + 1, column=0, sticky="w", pady=(35))

        # Bottom column labels
        bottom_column_frame = tk.Frame(board_frame, bg=BG_COLOR)
        bottom_column_frame.grid(row=9, column=1, sticky="ew")
        for i, letter in enumerate("abcdefgh"):
            label = tk.Label(
                bottom_column_frame,
                text=letter,
                font=LABEL_FONT,
                bg=BG_COLOR,
                fg="white",
                width=8,
            )
            label.grid(row=0, column=i)

        # Control buttons
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=20)

        reset_button = tk.Button(
            button_frame,
            text="New Game",
            font=BUTTON_FONT,
            command=self.new_game,
            bg="#4CAF50",
            fg="white",
            padx=20,
        )
        reset_button.pack(side=tk.LEFT, padx=10)

        quit_button = tk.Button(
            button_frame,
            text="Quit",
            font=BUTTON_FONT,
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            padx=20,
        )
        quit_button.pack(side=tk.LEFT, padx=20)

    def square_clicked(self, row: int, col: int) -> None:
        """Handle click events on chess squares."""
        if self.game.get_game_state() != "UNFINISHED":
            messagebox.showinfo(
                "Game Over", f"Game is finished! Winner: {self.game.get_game_state()}"
            )
            return

        if self.selected_square is None:
            piece = self.game.get_piece_type(row, col)
            if piece == 0:
                messagebox.showwarning(
                    "Invalid Selection", "Please select a piece to move."
                )
                return
            if not self.game.check_if_valid_player(piece):
                messagebox.showwarning(
                    "Invalid Selection", "Please select one of your own pieces."
                )
                return
            self.selected_square = (row, col)
            self.highlight_selected_square(row, col)
        else:
            start_row, start_col = self.selected_square
            if (row, col) == self.selected_square:
                self.clear_selection()
                return
            # Convert coordinates to chess notation
            start_pos = chr(ord("a") + start_col) + str(8 - start_row)
            end_pos = chr(ord("a") + col) + str(8 - row)
            if self.game.make_move(start_pos, end_pos):
                self.clear_selection()
                self.update_board()
                self.update_game_info()
                if self.game.get_game_state() != "UNFINISHED":
                    messagebox.showinfo(
                        "Game Over", f"Winner: {self.game.get_game_state()}!"
                    )
            else:
                messagebox.showwarning("Invalid Move", "That move is not allowed.")
                self.clear_selection()

    def highlight_selected_square(self, row: int, col: int) -> None:
        """Highlight the selected square."""
        self.board_buttons[row][col].configure(bg=HIGHLIGHT_COLOR)

    def clear_selection(self) -> None:
        """Clear the current selection and reset square colors."""
        self.selected_square = None
        self.update_board_colors()

    def update_board_colors(self) -> None:
        """Update the colors of all board squares."""
        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE_COLOR if is_light else DARK_SQUARE_COLOR
                self.board_buttons[row][col].configure(bg=color)

    def update_board(self) -> None:
        """Update the visual representation of the board."""
        for row in range(8):
            for col in range(8):
                piece = self.game.get_piece_type(row, col)
                symbol = self.piece_symbols.get(piece, "")
                self.board_buttons[row][col].configure(text=symbol)
        self.update_board_colors()

    def update_game_info(self) -> None:
        """Update the game state and current player labels."""
        self.game_state_label.configure(
            text=f"Game State: {self.game.get_game_state()}"
        )
        self.current_player_label.configure(
            text=f"Current Player: {self.game.get_current_player()}"
        )

    def new_game(self) -> None:
        """Start a new game."""
        self.game = AtomicChessGame()
        self.selected_square = None
        self.update_board()
        self.update_game_info()

    def run(self) -> None:
        """Start the GUI (enter the Tkinter event loop)."""
        self.root.mainloop()

    # For development: reload the UI without restarting the app
    def reload_ui(self) -> None:
        """Reload the UI by destroying and recreating all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.board_buttons.clear()
        self.setup_ui()
        self.update_board()
        self.update_game_info()


if __name__ == "__main__":
    chess_gui = ChessGUI()
    chess_gui.run()
