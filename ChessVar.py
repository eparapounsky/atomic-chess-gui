from enum import Enum

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


class ChessVar:
    """Represents a game of atomic chess"""

    def __init__(self):
        """Creates an instance of a game of atomic chess.
        Creates a starting board.
        Initializes game state to unfinished.
        Initializes first player to white."""

        self._board = [
            [1, 2, 3, 4, 5, 3, 2, 1],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [60, 60, 60, 60, 60, 60, 60, 60],
            [10, 20, 30, 40, 50, 30, 20, 10]
        ]
        self._game_state = "UNFINISHED"
        self._current_player = "WHITE"

    def get_game_state(self):
        """Returns the state of the game: UNFINISHED, WHITE_WON, or BLACK_WON"""
        return self._game_state

    def get_current_player(self):
        """Returns the current player: WHITE or BLACK"""
        return self._current_player

    def check_if_valid_player(self, piece):
        """Checks if the square being moved from does not contain the current player's piece
        :param piece: int, represents the piece being tested
        :return: False, if move is invalid"""

        if self._current_player == "BLACK" and piece > 6:
            return False
        if self._current_player == "WHITE" and piece < 10:
            return False

    def check_if_valid_atomic_move(self, piece, destination_column, destination_row):
        """Checks if the move is allowed by *atomic* chess rules.
        :param piece: int, represents the piece being moved
        :param destination_column: int, column of potential new piece location
        :param destination_row: int, row of potential new piece location"""

        # king not allowed to make captures
        if piece in (BK, WK) and self._board[destination_row][destination_column] != 0:
            return False

        # player cannot blow up both kings at once
        if self._board[destination_row][destination_column] != 0:
            pieces_list = []
            positions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for row, column in positions:
                try:
                    pieces_list.append(self._board[destination_row + row][destination_column + column])
                except IndexError:  # explosion on board edge
                    continue
            if 5 in pieces_list and 50 in pieces_list:
                return False

    def check_horizontal_vertical_move(self, current_column, current_row, destination_column, destination_row):
        """Checks if there are any pieces in the way of a potential horizontal or vertical move.
        :param current_column: int, column of current piece location
        :param current_row: int, row of current piece location
        :param destination_column: int, column of potential new piece location
        :param destination_row: int, row of potential new piece location"""

        if current_row == destination_row and current_column < destination_column:  # horizontal, to right
            checked_column = current_column + 1
            while checked_column != destination_column:
                if self._board[current_row][checked_column] != 0:
                    return False
                checked_column += 1

        elif current_row == destination_row and current_column > destination_column:  # horizontal, to left
            checked_column = current_column - 1
            while checked_column != destination_column:
                if self._board[current_row][checked_column] != 0:
                    return False
                checked_column -= 1

        elif current_column == destination_column and current_row > destination_row:  # vertical, to top
            checked_row = current_row - 1
            while checked_row != destination_row:
                if self._board[checked_row][current_column] != 0:
                    return False
                checked_row -= 1

        elif current_column == destination_column and current_row < destination_row:  # vertical, to bottom
            checked_row = current_row + 1
            while checked_row != destination_row:
                if self._board[checked_row][current_column] != 0:
                    return False
                checked_row += 1

    def check_diagonal_move(self, current_column, current_row, destination_column, destination_row):
        """Checks if there are any pieces in the way of a potential diagonal move.
        :param current_column: int, column of current piece location
        :param current_row: int, row of current piece location
        :param destination_column: int, column of potential new piece location
        :param destination_row: int, row of potential new piece location"""

        if current_row > destination_row and current_column < destination_column:  # bottom to top, to right
            checked_row = current_row - 1
            checked_column = current_column + 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row -= 1
                checked_column += 1

        elif current_row > destination_row and current_column > destination_column:  # bottom to top, to left
            checked_row = current_row - 1
            checked_column = current_column - 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row -= 1
                checked_column -= 1

        elif current_row < destination_row and current_column < destination_column:  # top to bottom, to right
            checked_row = current_row + 1
            checked_column = current_column + 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row += 1
                checked_column += 1

        elif current_row < destination_row and current_column > destination_column:  # top to bottom, to left
            checked_row = current_row + 1
            checked_column = current_column - 1
            while checked_row != destination_row:
                if self._board[checked_row][checked_column] != 0:
                    return False
                checked_row += 1
                checked_column -= 1

    def check_if_valid_chess_move(self, piece, current_column, current_row, destination_column, destination_row):
        """Checks if the move is allowed by regular chess rules.
        :param piece: int, represents the piece being moved
        :param current_column: int, column of current piece location
        :param current_row: int, row of current piece location
        :param destination_column: int, column of potential new piece location
        :param destination_row: int, row of potential new piece location"""

        row_distance = abs(current_row - destination_row)
        column_distance = abs(current_column - destination_column)

        # player cannot move off board
        if destination_column > 7 or destination_row < 0:
            return False

        # player cannot capture their own piece
        if piece < 10 and 0 < self._board[destination_row][destination_column] < 10:  # black
            return False
        if piece >= 10 and self._board[destination_row][destination_column] >= 10:  # white
            return False

        # rook can only move straight, no limit on spaces
        if piece in (BR, WR) and current_row != destination_row and current_column != destination_column:
            return False
        # check for pieces in rook's way
        if piece in (BR, WR):
            if self.check_horizontal_vertical_move(current_column, current_row,
                                                   destination_column, destination_row) is False:
                return False

        # horse can only move in L shape, can jump over pieces
        if piece in (BH, WH) and (row_distance, column_distance) not in [(1, 2), (2, 1)]:
            return False

        # bishop can only move diagonally, no limit on spaces
        if piece in (BB, WB) and row_distance != column_distance:
            return False
        # check for pieces in bishop's way
        if piece in (BB, WB):
            if self.check_diagonal_move(current_column, current_row, destination_column, destination_row) is False:
                return False

        # queen can move in any direction, no limit on spaces
        if piece in (BQ, WQ):
            if not (row_distance == column_distance or current_row == destination_row
                    or current_column == destination_column):
                return False

            # check horizontal/vertical moves for blocking pieces
            if current_row == destination_row or current_column == destination_column:
                if self.check_horizontal_vertical_move(current_column, current_row,
                                                       destination_column, destination_row) is False:
                    return False

            # check diagonal moves for blocking pieces
            if row_distance == column_distance:
                if self.check_diagonal_move(current_column, current_row, destination_column, destination_row) is False:
                    return False

        # king can only move 1 space at a time, any direction
        if piece in (BK, WK) and (row_distance > 1 or column_distance > 1):
            return False

        # pawns cannot move backwards or sideways
        if piece == BP and current_row >= destination_row:
            return False
        if piece == WP and current_row <= destination_row:
            return False

        # pawns can only move diagonally if making a capture
        if piece in (BP, WP) and self._board[destination_row][
                                    destination_column] == 0 and current_column != destination_column:
            return False

        # pawns cannot make head-on captures (only diagonal)
        if piece in (BP, WP) and self._board[destination_row][
                                    destination_column] != 0 and current_column == destination_column:
            return False

        # pawns can move forward 2 spaces on first turn, 1 thereafter
        if piece in (BP, WP) and (piece in self._board[1] or piece in self._board[6]):
            if row_distance > 2:
                return False
        elif piece in (BP, WP) and piece not in self._board[1] and piece not in self._board[6]:
            if row_distance > 1:
                return False

    def make_move(self, square_moved_from, square_moved_to):
        """Checks if the given move is valid.
        If so, moves a piece from one position to another on the board.
        :param square_moved_from: string, the current position of a piece on the board
        :param square_moved_to: string, the desired destination position of a piece on the board
        :return: False-if move is invalid, True-if move is valid"""

        current_position = list(square_moved_from)  # splits string into a list of characters
        destination_position = list(square_moved_to)

        current_column = ord(current_position[0]) - ord('a')  # unicode conversion, a = 0
        current_row = 8 - int(current_position[1])  # reverse order of rows

        piece = self.get_piece_type(current_row, current_column)

        destination_column = ord(destination_position[0]) - ord('a')
        destination_row = 8 - int(destination_position[1])

        if self.check_if_valid_player(piece) is False:
            return False

        if self.check_if_valid_atomic_move(piece, destination_column, destination_row) is False:
            return False

        if self.check_if_valid_chess_move(piece, current_column, current_row, destination_column,
                                          destination_row) is False:
            return False

        if self._game_state != "UNFINISHED":
            return False

        # make indicated move
        self._board[current_row][current_column] = 0
        if self._board[destination_row][destination_column] != 0:
            self._board[destination_row][destination_column] = 0  # capturing piece explodes
            positions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for row, column in positions:
                try:
                    if self._board[destination_row + row][destination_column + column] not in (BP, WP):  # not a pawn
                        self._board[destination_row + row][destination_column + column] = 0
                except IndexError:  # explosion on board edge
                    continue
        else:
            self._board[destination_row][destination_column] = piece

        self.check_if_king_dead()
        self.update_current_player()

        return True

    def update_current_player(self):
        """Updates the current player by alternating between black and white."""
        if self._current_player == "WHITE":
            self._current_player = "BLACK"
        else:
            self._current_player = "WHITE"

    def check_if_king_dead(self):
        """Checks if either of the kings has been captured"""
        if any(5 in row for row in self._board) is False:
            self._game_state = "WHITE_WON"
        elif any(50 in row for row in self._board) is False:
            self._game_state = "BLACK_WON"

    def print_board(self):
        """Prints out the chessboard with columns labeled a-h and rows labeled 1-8.
        Piece numbers are enumerated with initial representations."""
        print("    a  b  c  d  e  f  g  h")
        row_label = 8
        for row in self._board:
            print(f"{row_label}   ", end="")
            for piece in row:
                print(f"{Piece(piece).name} ", end="")
            print(f"  {row_label}")
            row_label -= 1
        print("    a  b  c  d  e  f  g  h")
        print()

    def get_piece_type(self, row, column):
        """Returns the piece at the given row and column in the chess board
        :param row: int, row of the desired piece
        :param column: int, column of the desired piece
        :return: int, piece at the given location"""
        return self._board[row][column]

def validate_input(start_pos, end_pos):
    start_pos = start_pos.lower()
    end_pos = end_pos.lower()

    # check for appropriate letter
    if start_pos[0] not in ("a", "b", "c", "d", "e", "f", "g", "h"):
        print("Please specify a valid square to move from.")
        return False
    if end_pos[0] not in ("a", "b", "c", "d", "e", "f", "g", "h"):
        print("Please specify a valid square to move to.")
        return False
    
    # check for appropriate number
    if start_pos[1] not in (1, 2, 3, 4, 5, 6, 7, 8):
        print("Please specify a valid square to move from.")
        return False
    if end_pos[1] not in (1, 2, 3, 4, 5, 6, 7, 8):
        print("Please specify a valid square to move to.")
        return False

if __name__ == "__main__":
    game = ChessVar()

    while True: 
        game.print_board()
        print("Game state:", game.get_game_state())
        print("Current player:", game.get_current_player())

        user_move = input("Enter your move (as 'e2 to e4'): ")
        start_pos, end_pos = user_move.split(" to ")

        if validate_input(start_pos, end_pos) is False:
            continue

        game.make_move(start_pos, end_pos)

        if game.get_game_state() != "UNFINISHED":
            print(f"WINNER: {game.get_game_state()}")
            break
