from enum import Enum
from typing import List

# Piece constants
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

# Game constants
BOARD_SIZE = 8
EMPTY_SQUARE = 0
BLACK_KING_VALUE = 5
WHITE_KING_VALUE = 50
BLACK_PIECE_THRESHOLD = 6
WHITE_PIECE_MIN = 10

# Game states
GAME_UNFINISHED = "UNFINISHED"
GAME_WHITE_WON = "WHITE_WON"
GAME_BLACK_WON = "BLACK_WON"

# Players
PLAYER_WHITE = "WHITE"
PLAYER_BLACK = "BLACK"

# Board positions for pawn starting rows
BLACK_PAWN_START_ROW = 1
WHITE_PAWN_START_ROW = 6

# Piece value mappings
PIECE_W_PAWN = WP
PIECE_W_ROOK = WR
PIECE_W_KNIGHT = WH
PIECE_W_BISHOP = WB
PIECE_W_QUEEN = WQ
PIECE_W_KING = WK
PIECE_B_PAWN = BP
PIECE_B_ROOK = BR
PIECE_B_KNIGHT = BH
PIECE_B_BISHOP = BB
PIECE_B_QUEEN = BQ
PIECE_B_KING = BK


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
    A class to represent an Atomic Chess game.
    Atomic chess follows regular chess rules with these exceptions:
    1. Kings cannot capture pieces
    2. When a capture occurs, an "explosion" destroys the capturing piece,
       captured piece, and all non-pawn pieces in surrounding 8 squares
    3. A player wins by eliminating the opponent's king
    """

    def __init__(self) -> None:
        """Initialize the chess game with starting positions"""
        self._board: List[List[int]] = [
            [BR, BH, BB, BQ, BK, BB, BH, BR],
            [BP, BP, BP, BP, BP, BP, BP, BP],
            [
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
            ],
            [
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
            ],
            [
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
            ],
            [
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
                EMPTY_SQUARE,
            ],
            [WP, WP, WP, WP, WP, WP, WP, WP],
            [WR, WH, WB, WQ, WK, WB, WH, WR],
        ]
        self._game_state: str = GAME_UNFINISHED
        self._current_player: str = PLAYER_WHITE

    def make_move(self, square_moved_from: str, square_moved_to: str) -> bool:
        """
        Attempts to make a move on the chess board.
        If successful, updates the board position, handles atomic explosions
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
        self._board[current_row][current_column] = EMPTY_SQUARE

        # handle capture with atomic explosion
        if self._board[destination_row][destination_column] != EMPTY_SQUARE:
            self._board[destination_row][
                destination_column
            ] = EMPTY_SQUARE  # Captured piece explodes
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

    # Private helper methods

    def _valid_piece_for_player(self, piece: int, player: str) -> bool:
        """Check if a piece belongs to the current player"""
        if player == PLAYER_WHITE:
            return piece in [
                PIECE_W_PAWN,
                PIECE_W_ROOK,
                PIECE_W_KNIGHT,
                PIECE_W_BISHOP,
                PIECE_W_QUEEN,
                PIECE_W_KING,
            ]
        elif player == PLAYER_BLACK:
            return piece in [
                PIECE_B_PAWN,
                PIECE_B_ROOK,
                PIECE_B_KNIGHT,
                PIECE_B_BISHOP,
                PIECE_B_QUEEN,
                PIECE_B_KING,
            ]
        return False

    def _check_if_valid_player(self, piece: int) -> bool:
        """Checks if the square being moved from does not contain the current player's piece
        Parameters:
            piece (int): represents the piece being tested
        Returns:
            bool: True if the piece belongs to the current player, False otherwise
        """

        if self._current_player == PLAYER_BLACK and piece > BLACK_PIECE_THRESHOLD:
            return False
        if self._current_player == PLAYER_WHITE and piece < WHITE_PIECE_MIN:
            return False
        return True

    def _check_if_valid_atomic_move(
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
        if (
            piece in (BLACK_KING_VALUE, WHITE_KING_VALUE)
            and self._board[destination_row][destination_column] != EMPTY_SQUARE
        ):
            return False

        # player cannot blow up both kings at once
        if self._board[destination_row][destination_column] != EMPTY_SQUARE:
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
            if BLACK_KING_VALUE in pieces_list and WHITE_KING_VALUE in pieces_list:
                return False

        return True

    def _check_horizontal_vertical_move(
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
                if self._board[current_row][checked_column] != EMPTY_SQUARE:
                    return False
                checked_column += 1

        elif (
            current_row == destination_row and current_column > destination_column
        ):  # horizontal, to left
            checked_column = current_column - 1
            while checked_column != destination_column:
                if self._board[current_row][checked_column] != EMPTY_SQUARE:
                    return False
                checked_column -= 1

        elif (
            current_column == destination_column and current_row > destination_row
        ):  # vertical, to top
            checked_row = current_row - 1
            while checked_row != destination_row:
                if self._board[checked_row][current_column] != EMPTY_SQUARE:
                    return False
                checked_row -= 1

        elif (
            current_column == destination_column and current_row < destination_row
        ):  # vertical, to bottom
            checked_row = current_row + 1
            while checked_row != destination_row:
                if self._board[checked_row][current_column] != EMPTY_SQUARE:
                    return False
                checked_row += 1

        return True

    def _check_diagonal_move(
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
                if self._board[checked_row][checked_column] != EMPTY_SQUARE:
                    return False
                checked_row -= 1
                checked_column += 1

        elif (
            current_row > destination_row and current_column > destination_column
        ):  # bottom to top, to left
            checked_row = current_row - 1
            checked_column = current_column - 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != EMPTY_SQUARE:
                    return False
                checked_row -= 1
                checked_column -= 1

        elif (
            current_row < destination_row and current_column < destination_column
        ):  # top to bottom, to right
            checked_row = current_row + 1
            checked_column = current_column + 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != EMPTY_SQUARE:
                    return False
                checked_row += 1
                checked_column += 1

        elif (
            current_row < destination_row and current_column > destination_column
        ):  # top to bottom, to left
            checked_row = current_row + 1
            checked_column = current_column - 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != EMPTY_SQUARE:
                    return False
                checked_row += 1
                checked_column -= 1

        return True

    def _validate_standard_move(
        self,
        piece: int,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Validates basic move rules common to all pieces
        Parameters:
            piece (int): The piece being moved
            current_column (int): Starting column (0-7)
            current_row (int): Starting row (0-7)
            destination_column (int): Target column (0-7)
            destination_row (int): Target row (0-7)
        Returns:
            bool: True if move passes basic validation, False otherwise
        """
        # check board bounds
        if (
            destination_column < 0
            or destination_column >= BOARD_SIZE
            or destination_row < 0
            or destination_row >= BOARD_SIZE
        ):
            return False

        # player cannot capture their own piece
        target_piece = self._board[destination_row][destination_column]
        if (
            piece < WHITE_PIECE_MIN and EMPTY_SQUARE < target_piece < WHITE_PIECE_MIN
        ):  # black piece capturing black
            return False
        if (
            piece >= WHITE_PIECE_MIN and target_piece >= WHITE_PIECE_MIN
        ):  # white piece capturing white
            return False

        return True

    def _is_valid_rook_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Check if a rook move is valid (horizontal or vertical with clear path)"""
        # rook moves horizontally or vertically
        if current_row != destination_row and current_column != destination_column:
            return False

        # check if path is clear
        return self._check_horizontal_vertical_move(
            current_column, current_row, destination_column, destination_row
        )

    def _is_valid_bishop_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Check if a bishop move is valid (diagonal with clear path)"""
        row_distance = abs(destination_row - current_row)
        column_distance = abs(destination_column - current_column)

        # bishop moves diagonally
        if row_distance != column_distance:
            return False

        # check if path is clear
        return self._check_diagonal_move(
            current_column, current_row, destination_column, destination_row
        )

    def _is_valid_queen_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Check if a queen move is valid (combines rook and bishop moves)"""
        # queen moves like rook or bishop
        return self._is_valid_rook_move(
            current_column, current_row, destination_column, destination_row
        ) or self._is_valid_bishop_move(
            current_column, current_row, destination_column, destination_row
        )

    def _is_valid_king_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Check if a king move is valid (one square in any direction)"""
        row_distance = abs(destination_row - current_row)
        column_distance = abs(destination_column - current_column)

        # king moves exactly one square in any direction
        return (
            row_distance <= 1
            and column_distance <= 1
            and (row_distance + column_distance) > 0
        )

    def _is_valid_knight_move(
        self,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Check if a knight move is valid (L-shaped: 2+1 or 1+2)"""
        row_distance = abs(destination_row - current_row)
        column_distance = abs(destination_column - current_column)

        # knight moves in L-shape: 2 squares one direction, 1 square perpendicular
        return (row_distance == 2 and column_distance == 1) or (
            row_distance == 1 and column_distance == 2
        )

    def _is_valid_pawn_move(
        self,
        piece: int,
        current_column: int,
        current_row: int,
        destination_column: int,
        destination_row: int,
    ) -> bool:
        """Check if a pawn move is valid (forward movement, diagonal capture)"""
        row_distance = abs(destination_row - current_row)
        column_distance = abs(destination_column - current_column)
        target_piece = self._board[destination_row][destination_column]

        # pawns move forward only
        if piece == BP and current_row >= destination_row:  # black pawn moving up
            return False
        if piece == WP and current_row <= destination_row:  # white pawn moving down
            return False

        # diagonal moves (captures)
        if column_distance == 1:
            # can only move diagonally if capturing
            if target_piece == EMPTY_SQUARE:
                return False
            # must move exactly 1 row forward
            return row_distance == 1

        # straight moves (non-captures)
        if current_column == destination_column:
            # cannot capture pieces directly ahead
            if target_piece != EMPTY_SQUARE:
                return False

            # can move 1 or 2 squares from starting position
            if (
                piece == BP
                and current_row == BLACK_PAWN_START_ROW
                and row_distance <= 2
            ):
                return True
            if (
                piece == WP
                and current_row == WHITE_PAWN_START_ROW
                and row_distance <= 2
            ):
                return True

            # otherwise can only move 1 square
            return row_distance == 1

        return False

    def is_valid_position(self, row: int, column: int) -> bool:
        """Check if coordinates are within board boundaries.
        Parameters:
            row (int): Row coordinate (0-7)
            column (int): Column coordinate (0-7)
        Returns:
            bool: True if coordinates are valid, False otherwise
        """
        return 0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE

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
        # Define all 8 surrounding positions plus the explosion center
        explosion_positions = [
            (explosion_row - 1, explosion_column - 1),  # top-left
            (explosion_row - 1, explosion_column),  # top
            (explosion_row - 1, explosion_column + 1),  # top-right
            (explosion_row, explosion_column - 1),  # left
            (explosion_row, explosion_column),  # center
            (explosion_row, explosion_column + 1),  # right
            (explosion_row + 1, explosion_column - 1),  # bottom-left
            (explosion_row + 1, explosion_column),  # bottom
            (explosion_row + 1, explosion_column + 1),  # bottom-right
        ]

        for row, column in explosion_positions:
            # Check if position is within board bounds
            if self.is_valid_position(row, column):
                piece = self._board[row][column]
                # Destroy all pieces except pawns
                if piece not in (BP, WP, EMPTY_SQUARE):
                    self._board[row][column] = EMPTY_SQUARE

    def validate_move(
        self,
        piece: int,
        current_row: int,
        current_column: int,
        destination_row: int,
        destination_column: int,
    ) -> bool:
        """
        Validates if a move is legal according to chess and atomic chess rules.
        Parameters:
            piece (int): The piece being moved
            current_row (int): Starting row (0-7)
            current_column (int): Starting column (0-7)
            destination_row (int): Target row (0-7)
            destination_column (int): Target column (0-7)
        Returns:
            bool: True if the move is valid, False otherwise
        """
        # check basic move validation
        if not self._validate_standard_move(
            piece, current_column, current_row, destination_column, destination_row
        ):
            return False

        # check if there's actually a piece to move
        if piece == EMPTY_SQUARE:
            return False

        # check if it's the current player's piece
        if not self._check_if_valid_player(piece):
            return False

        # check atomic chess specific rules
        if not self._check_if_valid_atomic_move(
            piece, destination_column, destination_row
        ):
            return False

        # validate piece-specific movement rules
        if piece in (BR, WR):  # rook
            return self._is_valid_rook_move(
                current_column, current_row, destination_column, destination_row
            )
        elif piece in (BB, WB):  # bishop
            return self._is_valid_bishop_move(
                current_column, current_row, destination_column, destination_row
            )
        elif piece in (BQ, WQ):  # queen
            return self._is_valid_queen_move(
                current_column, current_row, destination_column, destination_row
            )
        elif piece in (BK, WK):  # king
            return self._is_valid_king_move(
                current_column, current_row, destination_column, destination_row
            )
        elif piece in (BH, WH):  # knight
            return self._is_valid_knight_move(
                current_column, current_row, destination_column, destination_row
            )
        elif piece in (BP, WP):  # pawn
            return self._is_valid_pawn_move(
                piece, current_column, current_row, destination_column, destination_row
            )

        return False

    def parse_square_notation(self, square: str) -> tuple[int, int]:
        """
        Converts algebraic notation (e.g., "e4") to board coordinates.
        Parameters:
            square (str): Square in algebraic notation (e.g., "a1", "h8")
        Returns:
            tuple[int, int]: (row, column) coordinates (0-indexed)
        """
        column = ord(square[0].lower()) - ord("a")
        row = BOARD_SIZE - int(square[1])  # convert to 0-indexed from bottom
        return row, column

    def check_if_king_dead(self) -> None:
        """
        Checks if either king has been eliminated and updates game state accordingly.
        """
        black_king_alive = False
        white_king_alive = False

        # scan the board for kings
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self._board[row][col]
                if piece == BLACK_KING_VALUE:
                    black_king_alive = True
                elif piece == WHITE_KING_VALUE:
                    white_king_alive = True

        # update game state based on which kings are alive
        if not black_king_alive and not white_king_alive:
            # Both kings dead - current player loses
            if self._current_player == PLAYER_WHITE:
                self._game_state = GAME_BLACK_WON
            else:
                self._game_state = GAME_WHITE_WON
        elif not black_king_alive:
            self._game_state = GAME_WHITE_WON
        elif not white_king_alive:
            self._game_state = GAME_BLACK_WON

    def update_current_player(self) -> None:
        """
        Switches the current player between WHITE and BLACK.
        """
        if self._current_player == PLAYER_WHITE:
            self._current_player = PLAYER_BLACK
        else:
            self._current_player = PLAYER_WHITE
