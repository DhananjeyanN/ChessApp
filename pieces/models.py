class Square:
    def __init__(self):
        self.__piece = None
        self.color = None

    def is_empty(self) -> bool:
        return self.__piece is None

    def set_piece(self, piece: 'Piece') -> None:
        if isinstance(piece, Piece) or piece is None:
            self.__piece = piece
        else:
            raise ValueError("Invalid piece type")

    def get_piece(self) -> 'Piece':
        return self.__piece

    def remove_piece(self) -> None:
        self.__piece = None

    def __str__(self) -> str:
        return f"Square(color={self.color}, piece={self.__piece})"

    def __repr__(self) -> str:
        return self.__str__()

class BoardLog:
    def __init__(self):
        self.logs = []
        self.captured_white = []
        self.captured_black = []
        self.promoted = []

    def add_log(self, piece: 'Piece', source: tuple, dest: tuple) -> None:
        self.logs.append([piece, source, dest])

    def has_moved(self, piece: 'Piece') -> bool:
        for log in self.logs:
            if piece == log[0]:
                return True
        return False

    def add_capture(self, piece: 'Piece') -> None:
        if piece.get_color() == 'white':
            self.captured_white.append(piece)
        else:
            self.captured_black.append(piece)

    def add_promotion(self, piece: 'Piece', new_piece: 'Piece', cord: tuple) -> None:
        self.promoted.append([piece, new_piece, cord])

class Piece:
    def __init__(self, color: str, url: str):
        self.__color = color
        self.url = url

    def get_color(self) -> str:
        return self.__color

    def is_legit_move(self, board: 'Board', source: tuple, dest: tuple, log: 'BoardLog') -> bool:
        pass

    def move(self, board: 'Board', source: tuple, dest: tuple, log: 'BoardLog') -> bool:
        r_obj = self.is_legit_move(board=board, source=source, dest=dest, log=log)
        typ = type(r_obj)
        if typ == bool and r_obj is True:
            log.add_log(source=source, dest=dest, piece=self)
            board.move_piece(start=source, stop=dest, piece=self)
            return True
        elif typ in [Queen, Bishop, Knight, Rook]:
            log.add_log(source=source, dest=dest, piece=self)
            board.move_piece(start=source, stop=dest, piece=r_obj)
            return True
        return False

    def __str__(self) -> str:
        return f"Piece(color={self.__color}, url={self.url})"

class Pawn(Piece):
    def __init__(self, color: str, url: str):
        super().__init__(color, url)

    def is_legit_move(self, source: tuple, dest: tuple, board: 'Board', log: 'BoardLog') -> bool:
        y1, x1 = source
        y2, x2 = dest
        direction = -1 if self.get_color() == 'white' else 1
        start_row = 6 if self.get_color() == 'white' else 1
        end_row = 0 if self.get_color() == 'white' else 7

        # Forward move
        if x1 == x2:
            # Single step forward
            if y2 == y1 + direction and board.board[y2][x2].is_empty():
                if y2 == end_row:
                    self.promote(source, dest, board, log)
                return True
            # Double step from start row
            if y1 == start_row and y2 == y1 + 2 * direction and board.board[y2][x2].is_empty() and \
                    board.board[y1 + direction][x1].is_empty():
                return True

        # Captures
        if abs(x2 - x1) == 1 and y2 == y1 + direction:
            if not board.board[y2][x2].is_empty() and board.board[y2][
                x2].get_piece().get_color() != self.get_color():
                if y2 == end_row:
                    self.promote(source, dest, board, log)
                return True

        return False

    def promote(self, source: tuple, dest: tuple, board: 'Board', log: 'BoardLog') -> None:
        # Automatic promotion to a queen for simplicity, adjust as needed
        promotion_piece = Queen(color=self.get_color(), url=f'images/{self.get_color()}-queen.png')
        board.set_piece(dest, promotion_piece)
        log.add_promotion(self, promotion_piece, dest)

    def can_be_promoted(self, dest: tuple, board: 'Board', log: 'BoardLog') -> bool:
        y, x = dest
        if (y == 7 and self.get_color() == 'black') or (y == 0 and self.get_color() == 'white'):
            piece_choice = input('Enter Piece Choice: ')
            if piece_choice == 'queen':
                p = Queen(color=self.get_color(), url=f'images/{self.get_color()}-queen.png')
            elif piece_choice == 'knight':
                p = Knight(color=self.get_color(), url=f'images/{self.get_color()}-knight.png')
            elif piece_choice == 'bishop':
                p = Bishop(color=self.get_color(), url=f'images/{self.get_color()}-bishop.png')
            elif piece_choice == 'rook':
                p = Rook(color=self.get_color(), url=f'images/{self.get_color()}-rook.png')
            else:
                return False
            log.add_promotion(piece=board[y][x].get_piece(), cord=dest, new_piece=p)
            return p
        return False

    def can_en_passent(self) -> bool:
        # Implement en passant logic here
        pass

    def __str__(self) -> str:
        return f'{self.get_color()[0]}P'

class Knight(Piece):
    def __init__(self, color: str, url: str):
        super().__init__(color, url)

    def is_legit_move(self, source: tuple, dest: tuple, board: 'Board', log: 'BoardLog') -> bool:
        y1, x1 = source
        y2, x2 = dest
        if (abs(x1 - x2) == 2 and abs(y1 - y2) == 1) or (abs(x1 - x2) == 1 and abs(y1 - y2) == 2):
            if not board.board[y2][x2].is_empty():
                if board.board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                else:
                    log.add_capture(piece=board.board[y2][x2].get_piece())
            return True
        return False

    def __str__(self) -> str:
        return f'{self.get_color()[0]}N'


class Rook(Piece):
    def __init__(self, color: str, url: str):
        super().__init__(color, url)

    def is_legit_move(self, source: tuple, dest: tuple, board: 'Board', log: 'BoardLog') -> bool:
        board = board.board
        step_y = 0
        step_x = 0
        y1, x1 = source
        y2, x2 = dest

        if x2 > x1:
            step_x = 1
        elif x1 > x2:
            step_x = -1
        else:
            step_x = 0

        if y2 > y1:
            step_y = 1
        elif y1 > y2:
            step_y = -1
        else:
            step_y = 0

        check_x = x1 + step_x
        check_y = y1 + step_y

        if (x1 - x2 != 0 and y1 - y2 == 0) or (x1 - x2 == 0 and y1 - y2 != 0):
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y

            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self) -> str:
        return f'{self.get_color()[0]}R'


class Bishop(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        step_x = 0
        step_y = 0
        if x2 > x1:
            step_x = 1
        elif x1 > x2:
            step_x = -1
        else:
            step_x = 0

        if y2 > y1:
            step_y = 1
        elif y1 > y2:
            step_y = -1
        else:
            step_y = 0
        check_x = x1 + step_x
        check_y = y1 + step_y
        if abs(x2 - x1) == abs(y2 - y1):
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}B'

class Queen(Piece):
    def __init__(self, color: str, url: str):
        super().__init__(color, url)

    def is_legit_move(self, source: tuple, dest: tuple, board: 'Board', log: 'BoardLog') -> bool:
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        step_y = 0
        step_x = 0

        if x2 > x1:
            step_x = 1
        elif x1 > x2:
            step_x = -1

        if y2 > y1:
            step_y = 1
        elif y1 > y2:
            step_y = -1

        check_x = x1 + step_x
        check_y = y1 + step_y

        if (x1 - x2 != 0 and y1 - y2 == 0) or (x1 - x2 == 0 and y1 - y2 != 0) or (abs(x2 - x1) == abs(y2 - y1)):
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y

            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self) -> str:
        return f'{self.get_color()[0]}Q'

class King(Piece):
    def __init__(self, color: str, url: str):
        super().__init__(color, url)

    def is_legit_move(self, source: tuple, dest: tuple, board: 'Board', log: 'BoardLog') -> bool:
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        if (abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or (abs(y1 - y2) == 1 and abs(x1 - x2) == 0) or (abs(x1 - x2) == 1 and abs(y1 - y2) == 1):
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def can_castle(self) -> bool:
        # Implement castling logic here
        pass

    def __str__(self) -> str:
        return f'{self.get_color()[0]}K'


class Board:
    def __init__(self):
        self.board = [[Square() for _ in range(8)] for _ in range(8)]

    def initialize_board(self):
        for x in range(8):
            for y in range(8):
                self.board[x][y].set_piece(None)

        for i in range(8):
            b_pawn = Pawn(color='black', url='images/black-pawn.png')
            w_pawn = Pawn(color='white', url='images/white-pawn.png')

            self.board[1][i].set_piece(b_pawn)
            self.board[6][i].set_piece(w_pawn)

        b_rook1 = Rook(color='black', url='images/black-rook.png')
        b_rook2 = Rook(color='black', url='images/black-rook.png')
        w_rook1 = Rook(color='white', url='images/white-rook.png')
        w_rook2 = Rook(color='white', url='images/white-rook.png')

        self.board[0][0].set_piece(b_rook1)
        self.board[0][7].set_piece(b_rook2)
        self.board[7][0].set_piece(w_rook1)
        self.board[7][7].set_piece(w_rook2)

        b_bishop1 = Bishop(color='black', url='images/black-bishop.png')
        b_bishop2 = Bishop(color='black', url='images/black-bishop.png')
        w_bishop1 = Bishop(color='white', url='images/white-bishop.png')
        w_bishop2 = Bishop(color='white', url='images/white-bishop.png')

        self.board[0][2].set_piece(b_bishop1)
        self.board[0][5].set_piece(b_bishop2)
        self.board[7][2].set_piece(w_bishop1)
        self.board[7][5].set_piece(w_bishop2)

        b_knight1 = Knight(color='black', url='images/black-knight.png')
        b_knight2 = Knight(color='black', url='images/black-knight.png')
        w_knight1 = Knight(color='white', url='images/white-knight.png')
        w_knight2 = Knight(color='white', url='images/white-knight.png')

        self.board[0][1].set_piece(b_knight1)
        self.board[0][6].set_piece(b_knight2)
        self.board[7][1].set_piece(w_knight1)
        self.board[7][6].set_piece(w_knight2)

        b_queen = Queen(color='black', url='images/black-queen.png')
        w_queen = Queen(color='white', url='images/white-queen.png')

        self.board[0][3].set_piece(b_queen)
        self.board[7][3].set_piece(w_queen)

        b_king = King(color='black', url='images/black-king.png')
        w_king = King(color='white', url='images/white-king.png')

        self.board[0][4].set_piece(b_king)
        self.board[7][4].set_piece(w_king)
        return w_king, b_king

    def print_board(self):
        print('  -', end='')
        print('+---+' * 8)
        for x in range(8):
            print(8 - x, end=' ')
            print('| ', end='')
            for y in range(8):
                if self.board[x][y].get_piece() is None:
                    print('  ', end=' | ')
                else:
                    print(self.board[x][y].get_piece(), end=' | ')
            print()
            print('  -', end='')
            print('+---+' * 8)
        print('    a    b    c    d    e    f    g    h')

    def move_piece(self, start, stop, piece):
        x1, y1 = start
        x2, y2 = stop
        self.board[x1][y1].set_piece(None)
        self.board[x2][y2].set_piece(piece)

    def get_piece(self, cord):
        x, y = cord
        return self.board[x][y].get_piece()

    def has_piece(self, cord, piece):
        x, y = cord
        return self.board[x][y].get_piece() == piece

    def set_piece(self, cord, piece):
        x, y = cord
        self.board[x][y].set_piece(piece)


class Game:
    def __init__(self):
        self.board = Board()
        self.board.initialize_board()
        self.log = BoardLog()
        self.turn =self.player_setup()
    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

    def player_setup(self):
        pw = input('Enter White Player Name: ')
        pb = input('Enter Black Player Name: ')
        turn = input('Enter the name of 1st mover: ')
        if turn == pw:
            self.turn = 'white'
            self.is_white = True
        else:
            self.is_white = False
            self.turn = 'black'
        return self.turn

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.get_color() != color:
                    if piece.is_legit_move((row, col), king_pos, self.board, self.log):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.get_color() == color:
                    for r in range(8):
                        for c in range(8):
                            if piece.is_legit_move((row, col), (r, c), self.board, self.log):
                                original_piece = self.board.get_piece((r, c))
                                self.board.move_piece((row, col), (r, c), piece)
                                if not self.is_in_check(color):
                                    self.board.move_piece((r, c), (row, col), piece)
                                    self.board.set_piece((r, c), original_piece)
                                    return False
                                self.board.move_piece((r, c), (row, col), piece)
                                self.board.set_piece((r, c), original_piece)
        return True

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if isinstance(piece, King) and piece.get_color() == color:
                    return (row, col)
        return None

    def move(self, source, dest):
        piece = self.board.get_piece(source)
        if piece and piece.get_color() == self.turn:
            if piece.move(self.board, source, dest, self.log):
                if self.is_in_check(self.turn):
                    print(f"Move places {self.turn} in check! Illegal move.")
                    self.board.move_piece(dest, source, piece)
                    return False
                self.switch_turn()
                return True
            else:
                print("Illegal move!")
        else:
            print("No piece at source or not your turn!")
        return False

    def play(self):
        while True:
            self.board.print_board()
            if self.is_checkmate(self.turn):
                print(f"Checkmate! {self.turn} loses.")
                break
            if self.is_in_check(self.turn):
                print(f"{self.turn} is in check!")
            print(f"{self.turn}'s move")
            source,dest = input("Enter source (e.g., 'e2,e4'): ").strip().split(",")
            source = (8 - int(source[1]), ord(source[0]) - ord('a'))
            dest = (8 - int(dest[1]), ord(dest[0]) - ord('a'))
            self.move(source, dest)


def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()