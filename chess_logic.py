from enum import Enum
from typing import List

# Constants representing chess pieces
# Integers used to represent pieces for easier validation and movement logic
__ = 0  # empty space
BR = 1  # black rook
BH = 2  # black horse/knight
BB = 3  # black bishop
BQ = 4  # black queen
BK = 5  # black king
BP = 6  # black pawn
WR = 10  # white rook
WH = 20  # white horse/knight
WB = 30  # white bishop
WQ = 40  # white queen
WK = 50  # white king
WP = 60  # white pawn


class Piece(Enum):
    """Enumeration for chess pieces"""

    __ = __  # empty space
    BR = BR  # black rook
    BH = BH  # black horse/knight
    BB = BB  # black bishop
    BQ = BQ  # black queen
    BK = BK  # black king
    BP = BP  # black pawn
    WR = WR  # white rook
    WH = WH  # white horse/knight
    WB = WB  # white bishop
    WQ = WQ  # white queen
    WK = WK  # white king
    WP = WP  # white pawn


class AtomicChessGame:
    """
    Represents a game of atomic chess.

    Atomic chess is a variant of chess where:
    1. Kings cannot capture pieces
    2. When a capture occurs, an "explosion" destroys the capturing piece,
       captured piece, and all non-pawn pieces in surrounding 8 squares
    3. Players cannot make moves that would destroy both kings
    4. Game ends when one king is destroyed

    Attributes:
        _board: 8x8 list representing the chess board with piece values
        _game_state: Current state ("UNFINISHED", "WHITE_WON", "BLACK_WON")
        _current_player: Current player ("WHITE" or "BLACK")
    """

    def __init__(self) -> None:
        """Creates an instance of a game of atomic chess.
        Creates a starting board.
        Initializes game state to unfinished.
        Initializes first player to white."""

        self._board: List[List[int]] = [
            [1, 2, 3, 4, 5, 3, 2, 1],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [60, 60, 60, 60, 60, 60, 60, 60],
            [10, 20, 30, 40, 50, 30, 20, 10],
        ]
        self._game_state: str = "UNFINISHED"
        self._current_player: str = "WHITE"

    def make_move(self, square_moved_from: str, square_moved_to: str) -> bool:
        """
        Moves a piece from one square to another if the move is valid according to atomic chess rules.
        If a capture occurs, implements the atomic explosion that eliminates all non-pawn pieces
        in the 8 surrounding squares.
        After the move, checks if any king has been eliminated and updates the current player.
        Parameters:
            square_moved_from (str): The algebraic notation of the starting square (e.g., "e2")
            square_moved_to (str): The algebraic notation of the destination square (e.g., "e4")
        Returns:
            bool: True if the move was valid and executed, False otherwise
        """
        # parse square notations to coordinates
        current_row, current_column = self.parse_square_notation(square_moved_from)
        destination_row, destination_column = self.parse_square_notation(
            square_moved_to
        )

        piece = self.get_piece_type(current_row, current_column)

        # validate the move
        if not self.validate_move(
            piece, current_row, current_column, destination_row, destination_column
        ):
            return False

        # execute the move
        self._board[current_row][current_column] = 0

        # handle capture with atomic explosion
        if self._board[destination_row][destination_column] != 0:
            self._board[destination_row][
                destination_column
            ] = 0  # Captured piece explodes
            self.execute_atomic_explosion(destination_row, destination_column)
        else:
            # Normal move without capture
            self._board[destination_row][destination_column] = piece

        # update game state
        self.check_if_king_dead()
        self.update_current_player()

        return True

    def get_game_state(self) -> str:
        """Returns the state of the game: UNFINISHED, WHITE_WON, or BLACK_WON"""
        return self._game_state

    def get_current_player(self) -> str:
        """Returns the current player: WHITE or BLACK"""
        return self._current_player

    def get_piece_type(self, row: int, column: int) -> int:
        """Returns the piece at the given row and column in the chess board.
        Parameters:
            row (int): row of the desired piece
            column (int): column of the desired piece
        Returns:
            int: the piece type at the specified location
        """
        return self._board[row][column]

    def check_if_valid_player(self, piece: int) -> bool:
        """Checks if the square being moved from does not contain the current player's piece
        Parameters:
            piece (int): represents the piece being tested
        Returns:
            bool: True if the piece belongs to the current player, False otherwise
        """

        if self._current_player == "BLACK" and piece > 6:
            return False
        if self._current_player == "WHITE" and piece < 10:
            return False
        return True

    def check_if_valid_atomic_move(
        self, piece: int, destination_column: int, destination_row: int
    ) -> bool:
        """Checks if the move is allowed by *atomic* chess rules.
        Parameters:
            piece (int): represents the piece being moved
            destination_column (int): column of potential new piece location
            destination_row (int): row of potential new piece location
        Returns:
            bool: True if the move is valid according to atomic chess rules, False otherwise
        """

        # king not allowed to make captures
        if piece in (BK, WK) and self._board[destination_row][destination_column] != 0:
            return False

        # player cannot blow up both kings at once
        if self._board[destination_row][destination_column] != 0:
            pieces_list = []
            positions = [
                (0, 0),
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]
            for row, column in positions:
                try:
                    pieces_list.append(
                        self._board[destination_row + row][destination_column + column]
                    )
                except IndexError:  # explosion on board edge
                    continue
            if 5 in pieces_list and 50 in pieces_list:
                return False

        return True

    def check_horizontal_vertical_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """
        Checks if there are any pieces in the way of a potential horizontal or vertical move.
        Parameters:
            current_column (int): The column of the current piece location (0-indexed)
            current_row (int): The row of the current piece location (0-indexed)
            destination_column (int): The column of the potential new piece location (0-indexed)
            destination_row (int): The row of the potential new piece location (0-indexed)
        Returns:
            bool: True if the path is clear (no obstructions), False if there is at least one piece in the way
        """

        if (
            current_row == destination_row and current_column < destination_column
        ):  # horizontal, to right
            checked_column = current_column + 1
            while checked_column != destination_column:
                if self._board[current_row][checked_column] != 0:
                    return False
                checked_column += 1

        elif (
            current_row == destination_row and current_column > destination_column
        ):  # horizontal, to left
            checked_column = current_column - 1
            while checked_column != destination_column:
                if self._board[current_row][checked_column] != 0:
                    return False
                checked_column -= 1

        elif (
            current_column == destination_column and current_row > destination_row
        ):  # vertical, to top
            checked_row = current_row - 1
            while checked_row != destination_row:
                if self._board[checked_row][current_column] != 0:
                    return False
                checked_row -= 1

        elif (
            current_column == destination_column and current_row < destination_row
        ):  # vertical, to bottom
            checked_row = current_row + 1
            while checked_row != destination_row:
                if self._board[checked_row][current_column] != 0:
                    return False
                checked_row += 1

        return True

    def check_diagonal_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """
        Checks if there are any pieces in the way of a potential diagonal move.
        Handles all four diagonal directions.
        Parameters:
            current_column (int): column of current piece location (0-7)
            current_row (int): row of current piece location (0-7)
            destination_column (int): column of potential new piece location (0-7)
            destination_row (int): row of potential new piece location (0-7)
        Returns:
            bool: True if path is clear, False if obstructed
        """

        if (
            current_row > destination_row and current_column < destination_column
        ):  # bottom to top, to right
            checked_row = current_row - 1
            checked_column = current_column + 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row -= 1
                checked_column += 1

        elif (
            current_row > destination_row and current_column > destination_column
        ):  # bottom to top, to left
            checked_row = current_row - 1
            checked_column = current_column - 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row -= 1
                checked_column -= 1

        elif (
            current_row < destination_row and current_column < destination_column
        ):  # top to bottom, to right
            checked_row = current_row + 1
            checked_column = current_column + 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row += 1
                checked_column += 1

        elif (
            current_row < destination_row and current_column > destination_column
        ):  # top to bottom, to left
            checked_row = current_row + 1
            checked_column = current_column - 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row += 1
                checked_column -= 1

        return True

    def check_if_valid_chess_move(
        self,
        piece: int,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """
        Checks if the move is allowed by regular chess rules.
        Does not check for special moves like castling, en passant, or check/checkmate conditions.
        Parameters:
            piece (int): The piece being moved (uses piece constants like BP, WR, etc.)
            current_column (int): The column (0-7) of the piece's current position
            current_row (int): The row (0-7) of the piece's current position
            destination_column (int): The column (0-7) of the piece's intended destination
            destination_row (int): The row (0-7) of the piece's intended destination
        Returns:
            bool: True if the move is valid, False otherwise
        """
        if not self._is_destination_valid(piece, destination_column, destination_row):
            return False

        # check piece-specific movement rules
        if piece in (BR, WR):
            return self._is_valid_rook_move(current_column, current_row, destination_column, destination_row)
        elif piece in (BH, WH):
            return self._is_valid_knight_move(current_column, current_row, destination_column, destination_row)
        elif piece in (BB, WB):
            return self._is_valid_bishop_move(current_column, current_row, destination_column, destination_row)
        elif piece in (BQ, WQ):
            return self._is_valid_queen_move(current_column, current_row, destination_column, destination_row)
        elif piece in (BK, WK):
            return self._is_valid_king_move(current_column, current_row, destination_column, destination_row)
        elif piece in (BP, WP):
            return self._is_valid_pawn_move(piece, current_column, current_row, destination_column, destination_row)

        return False

    def _is_destination_valid(self, piece: int, destination_column: int, destination_row: int) -> bool:
        """Check if destination is on board and not occupied by own piece."""
        # player cannot move off board
        if destination_column < 0 or destination_column > 7 or destination_row < 0 or destination_row > 7:
            return False

        # player cannot capture their own piece
        target_piece = self._board[destination_row][destination_column]
        if piece < 10 and 0 < target_piece < 10:  # black piece capturing black
            return False
        if piece >= 10 and target_piece >= 10:  # white piece capturing white
            return False

        return True

    def _is_valid_rook_move(self, current_column: int, current_row: int, 
                           destination_column: int, destination_row: int) -> bool:
        """Check if rook move is valid."""
        # rook can only move straight (horizontal or vertical)
        if current_row != destination_row and current_column != destination_column:
            return False

        # check for pieces blocking the path
        return self.check_horizontal_vertical_move(
            current_column, current_row, destination_column, destination_row
        )

    def _is_valid_knight_move(self, current_column: int, current_row: int,
                             destination_column: int, destination_row: int) -> bool:
        """Check if knight move is valid."""
        row_distance = abs(current_row - destination_row)
        column_distance = abs(current_column - destination_column)
        
        # knight moves in L shape: 2+1 or 1+2
        return (row_distance, column_distance) in [(1, 2), (2, 1)]

    def _is_valid_bishop_move(self, current_column: int, current_row: int,
                             destination_column: int, destination_row: int) -> bool:
        """Check if bishop move is valid."""
        row_distance = abs(current_row - destination_row)
        column_distance = abs(current_column - destination_column)
        
        # bishop can only move diagonally
        if row_distance != column_distance:
            return False

        # check for pieces blocking the diagonal path
        return self.check_diagonal_move(
            current_column, current_row, destination_column, destination_row
        )

    def _is_valid_queen_move(self, current_column: int, current_row: int,
                            destination_column: int, destination_row: int) -> bool:
        """Check if queen move is valid."""
        row_distance = abs(current_row - destination_row)
        column_distance = abs(current_column - destination_column)
        
        # queen can move any amount of spaces in any direction
        is_straight = current_row == destination_row or current_column == destination_column
        is_diagonal = row_distance == column_distance
        
        if not (is_straight or is_diagonal):
            return False

        # check for blocking pieces based on movement type
        if is_straight:
            return self.check_horizontal_vertical_move(
                current_column, current_row, destination_column, destination_row
            )
        else:  # is_diagonal
            return self.check_diagonal_move(
                current_column, current_row, destination_column, destination_row
            )

    def _is_valid_king_move(self, current_column: int, current_row: int,
                           destination_column: int, destination_row: int) -> bool:
        """Check if king move is valid."""
        row_distance = abs(current_row - destination_row)
        column_distance = abs(current_column - destination_column)
        
        # king can only move 1 space in any direction
        return row_distance <= 1 and column_distance <= 1

    def _is_valid_pawn_move(self, piece: int, current_column: int, current_row: int,
                           destination_column: int, destination_row: int) -> bool:
        """Check if pawn move is valid."""
        row_distance = abs(current_row - destination_row)
        column_distance = abs(current_column - destination_column)
        target_piece = self._board[destination_row][destination_column]
        
        # pawns cannot move backwards
        if piece == BP and current_row >= destination_row:  # black pawn moving up
            return False
        if piece == WP and current_row <= destination_row:  # white pawn moving down
            return False

        # diagonal moves (captures)
        if column_distance == 1:
            # can only move diagonally if capturing
            if target_piece == 0:
                return False
            # must move exactly 1 row forward
            return row_distance == 1

        # straight moves (non-captures)
        if current_column == destination_column:
            # cannot capture pieces directly ahead
            if target_piece != 0:
                return False
            
            # check if pawn is on starting row (can move 2 spaces)
            is_on_starting_row = (piece == BP and current_row == 1) or (piece == WP and current_row == 6)
            
            if is_on_starting_row:
                return row_distance in [1, 2]
            else:
                return row_distance == 1

        return False

    def parse_square_notation(self, square: str) -> tuple[int, int]:
        """
        Converts algebraic notation (e.g., "e4") to board coordinates.
        Parameters:
            square (str): Square in algebraic notation
        Returns:
            tuple[int, int]: (row, column) coordinates (0-indexed)
        """
        column = ord(square[0]) - ord("a")
        row = 8 - int(square[1])
        return row, column

    def are_coordinates_valid(self, row: int, column: int) -> bool:
        """
        Checks if the given coordinates are within board bounds.
        Parameters:
            row (int): Row coordinate (0-7)
            column (int): Column coordinate (0-7)
        Returns:
            bool: True if coordinates are valid, False otherwise
        """
        return 0 <= row <= 7 and 0 <= column <= 7

    def execute_atomic_explosion(
        self, explosion_row: int, explosion_column: int
    ) -> None:
        """
        Executes an atomic explosion at the given coordinates, destroying all
        non-pawn pieces in the 8 surrounding squares.
        Parameters:
            explosion_row (int): Row where explosion occurs
            explosion_column (int): Column where explosion occurs
        """
        explosion_positions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for row_offset, col_offset in explosion_positions:
            target_row = explosion_row + row_offset
            target_col = explosion_column + col_offset

            if self.are_coordinates_valid(target_row, target_col):
                # only destroy non-pawn pieces
                if self._board[target_row][target_col] not in (BP, WP):
                    self._board[target_row][target_col] = 0

    def validate_move(
        self,
        piece: int,
        current_row: int,
        current_column: int,
        destination_row: int,
        destination_column: int,
    ) -> bool:
        """
        Validates if a move is legal according to all game rules.
        Parameters:
            piece (int): The piece being moved
            current_row (int): Current row of the piece
            current_column (int): Current column of the piece
            destination_row (int): Destination row
            destination_column (int): Destination column
        Returns:
            bool: True if move is valid, False otherwise
        """
        # check if coordinates are within bounds
        if not (
            self.are_coordinates_valid(current_row, current_column)
            and self.are_coordinates_valid(destination_row, destination_column)
        ):
            return False

        # check if there's actually a piece to move
        if piece == 0:
            return False

        # check if it's the current player's piece
        if not self.check_if_valid_player(piece):
            return False

        # check atomic chess rules
        if not self.check_if_valid_atomic_move(
            piece, destination_column, destination_row
        ):
            return False

        # check regular chess rules
        if not self.check_if_valid_chess_move(
            piece, current_column, current_row, destination_column, destination_row
        ):
            return False

        # check if game is still in progress
        if self._game_state != "UNFINISHED":
            return False

        return True

    def update_current_player(self) -> None:
        """Updates the current player by alternating between black and white."""
        if self._current_player == "WHITE":
            self._current_player = "BLACK"
        else:
            self._current_player = "WHITE"

    def check_if_king_dead(self) -> None:
        """Checks if either of the kings has been captured."""
        if any(5 in row for row in self._board) is False:
            self._game_state = "WHITE_WON"
        elif any(50 in row for row in self._board) is False:
            self._game_state = "BLACK_WON"
