from django.db import models


# Create your models here.

class Piece:
    def __init__(self, color, url):
        self.__color = color
        self.url = url

    def get_color(self):
        return self.__color

    def is_legit_move(self):
        pass

    def move(self, board, source, dest):
        if self.is_legit_move(board=board, source=source, dest=dest):
            board.move_piece(start=source, stop=dest, piece=self)


class Pawn(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        if self.get_color() == 'white':
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        if x1 == x2 and y2 == y1 + direction and board[y2][x2].is_empty():
            return True
        if y1 == start_row and y2 == y1 + direction*2 and board[y2][x2].is_empty() and board[y1 + direction][x1]:
            return True
        if x1 + 1 == x2 or x1 - 1 == x2 and y2 == y1 + direction and not board[y2][x2].is_empty():
            return True
        return False

    def can_be_promoted(self, dest, piece_choice, board):
        x, y = dest
        if self.color == 'white':
            if x == 7:
                if piece_choice == 'queen':
                    board[x][y] = Queen(color=self.get_color(), url='queen_url')
                elif piece_choice == 'knight':
                    board[x][y] = Knight(color=self.get_color(), url='knight_url')
                elif piece_choice == 'bishop':
                    board[x][y] = Bishop(color=self.get_color(), url='bishop_url')
                elif piece_choice == 'rook':
                    board[x][y] = Rook(color=self.get_color(), url='rook_url')
            return True
        else:
            if x == 0:
                if piece_choice == 'queen':
                    board[x][y] = Queen(color=self.get_color(), url='queen_url')
                elif piece_choice == 'knight':
                    board[x][y] = Knight(color=self.get_color(), url='knight_url')
                elif piece_choice == 'bishop':
                    board[x][y] = Bishop(color=self.get_color(), url='bishop_url')
                elif piece_choice == 'rook':
                    board[x][y] = Rook(color=self.get_color(), url='rook_url')
            return True

    def can_en_passent(self):
        pass

    def __str__(self):
        return f'{self.get_color()[0]}P'


class Queen(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board):
        x1, y1 = source
        x2, y2 = dest
        step_y = 0
        step_x = 0
        if x2 > x1:
            step_x = 1
        elif x1 > x2:
            step_x = -1
        else:
            step_x = 0

        if y2 > y1:
            step_x = 1
        elif y1 > y2:
            step_y = -1
        else:
            step_y = 0
        check_x = x1 + step_x
        check_y = y1 + step_y
        if x1 - x2 != 0 and y1 - y2 == 0 or x1 - x2 == 0 and y1 - y2 != 0 or x2 - x1 / y2 - y1 == 1:
            while check_x != x2 or check_y != y2:
                if not board[check_x][check_y].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if board[x2][y2].get_piece().get_color() == board[x1][y1].get_piece().get_color():
                return False
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}Q'


class Rook(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board):
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
        print(x1,x2, step_x, y1, y2, step_y, check_x, check_y)
        if x1 - x2 != 0 and y1 - y2 == 0 or x1 - x2 == 0 and y1 - y2 != 0:
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == board[y1][x1].get_piece().get_color():
                    return False
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}R'


class Bishop(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board):
        x1, y1 = source
        x2, y2 = dest
        if x2 > x1:
            step_x = 1
        elif x1 > x2:
            step_x = -1
        else:
            step_x = 0

        if y2 > y1:
            step_x = 1
        elif y1 > y2:
            step_y = -1
        else:
            step_y = 0
        check_x = x1 + step_x
        check_y = y1 + step_y
        if x2 - x1 / y2 - y1 == 1:
            while check_x != x2 or check_y != y2:
                if not board[check_x][check_y].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if board[x2][y2].get_piece().get_color() == board[x1][y1].get_piece().get_color():
                return False
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}B'


class King(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board):
        x1, y1 = source
        x2, y2 = dest
        if (abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or (abs(y1 - y2) == 1 and abs(x1 - x2) == 0) or (
                abs(x1 - x2) == 1 and abs(y1 - y2) == 1):
            if board[x2][y2].get_piece().get_color() == board[x1][y1].get_piece().get_color():
                return False
            return True
        return False

    def can_castle(self):
        pass

    def __str__(self):
        return f'{self.get_color()[0]}K'


class Knight(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board):
        x1, y1 = source
        x2, y2 = dest
        if (abs(x1 - x2) == 2 and abs(y1 - y2) == 1) or (abs(x1 - x2) == 1 and abs(y1 - y2) == 2):
            if not board.board[x2][y2].is_empty():
                if board.board[x2][y2].get_piece().get_color() == self.get_color():
                    return False
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}N'


class Board:
    def __init__(self):
        self.board = [[Square() for _ in range(8)] for _ in range(8)]
        print(self.board)
        for i in range(8):
            for j in range(8):
                s = Square()
                self.board[i][j] = s
                print(id(self.board[i][j]))

    def initialize_board(self):
        for x in range(8):
            for y in range(8):
                self.board[x][y].set_piece(None)
        for i in range(8):
            b_pawn = Pawn(color='black', url='images/black-pawn.png')
            w_pawn = Pawn(color='white', url='images/white-pawn.png')

            self.board[6][i].set_piece(w_pawn)
            self.board[1][i].set_piece(b_pawn)

        b_rook = Rook(color='black', url='images/black-rook.png')
        w_rook = Rook(color='white', url='images/white-rook.png')
        b_rook2 = Rook(color='black', url='images/black-rook.png')
        w_rook2 = Rook(color='white', url='images/white-rook.png')

        self.board[0][0].set_piece(b_rook)
        self.board[0][7].set_piece(b_rook2)
        self.board[7][0].set_piece(w_rook)
        self.board[7][7].set_piece(w_rook2)

        b_bishop = Bishop(color='black', url='images/black-bishop.png')
        w_bishop = Bishop(color='white', url='images/white-bishop.png')
        b_bishop2 = Bishop(color='black', url='images/black-bishop.png')
        w_bishop2 = Bishop(color='white', url='images/white-bishop.png')

        self.board[0][2].set_piece(b_bishop)
        self.board[0][5].set_piece(b_bishop2)
        self.board[7][2].set_piece(w_bishop2)
        self.board[7][5].set_piece(w_bishop)

        b_knight = Knight(color='black', url='images/black-knight.png')
        w_knight = Knight(color='white', url='images/white-knight.png')
        b_knight2 = Knight(color='black', url='images/black-knight.png')
        w_knight2 = Knight(color='white', url='images/white-knight.png')

        self.board[0][1].set_piece(b_knight)
        self.board[0][6].set_piece(b_knight2)
        self.board[7][1].set_piece(w_knight2)
        self.board[7][6].set_piece(w_knight)

        b_queen = Queen(color='black', url='images/black-queen.png')
        w_queen = Queen(color='white', url='images/white-queen.png')

        self.board[0][3].set_piece(b_queen)
        self.board[7][3].set_piece(w_queen)

        b_king = King(color='black', url='images/black-king.png')
        w_king = King(color='white', url='images/white-king.png')

        self.board[0][4].set_piece(b_king)
        self.board[7][4].set_piece(w_king)
        print(self.board)

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
        self.board[x1][y1].set_piece(piece=None)
        self.board[x2][y2].set_piece(piece=piece)

    def get_piece(self, cord):
        x, y = cord
        return self.board[y][x].get_piece()

    def has_piece(self, cord, piece):
        x, y = cord
        if board[y][x].get_piece() == piece:
            return True
        return False


class Square:
    def __init__(self):
        self.__piece = None
        self.color = None

    def is_empty(self):
        if self.__piece is None:
            return True
        else:
            return False

    def set_piece(self, piece):
        self.__piece = piece

    def get_piece(self):
        return self.__piece

    def remove_piece(self):
        self.__piece = None


class BoardLog:
    def __init__(self):
        self.logs = []
        self.captured_white = []
        self.captured_black = []
        self.promoted = []

    def add_log(self, piece, source, dest):
        self.logs.append([piece, source, dest])

    def has_moved(self, piece):
        for i in self.logs:
            if piece in i[0]:
                return True
        return False

    def add_capture(self, piece):
        if piece.get_color() == 'white':
            self.captured_white.append(piece)
        else:
            self.captured_black.append(piece)

    def add_promotion(self, piece, new_piece, cord):
        self.promoted.append([piece, new_piece, cord])


def convert_input(move):
    file, rank = move[0], 8 - int(move[1])
    file = ord(file) - ord('a')
    return rank, file


# board = Board()
# board.initialize_board()
# board.print_board()
# print(board.board[0][1].get_piece())
# print(board.board[0][1].get_piece().is_legit_move(source=[0, 1], dest=[2, 2], board=board))
# print(board.board[0][2].get_piece())
#
# board.board[0][1].get_piece().move(board=board, source=[0, 1], dest=[2, 2])
# board.print_board()
#
# print(convert_input('c8'))


class Game:
    def __init__(self):
        self.board = Board()

    def start_game(self):
        self.board.initialize_board()

    def print_board(self):
        self.board.print_board()


    def convert_input(self, move):
        file, rank = move[0], 8 - int(move[1])
        file2, rank2 = move[3], 8 - int(move[4])
        file = ord(file) - ord('a')
        file2 = ord(file2) - ord('a')
        return (rank, file), (rank2, file2)

    def get_input(self):
        move = input('Enter Move ex: b2,b3: ')
        return self.convert_input(move)

    def move_piece(self):
        origin, dest = self.get_input()
        if self.board.board[origin[0]][origin[1]].get_piece().is_legit_move(source=origin, dest=dest, board=self.board):
            self.board.board[origin[0]][origin[1]].get_piece().move(board=self.board, source=origin, dest=dest)
        else:
            print('MOVE NOT VALID!!!')
        self.print_board()

    def run_game(self):
        i = 0
        game.start_game()
        while i != 1:
            game.print_board()
            game.move_piece()

game = Game()
game.run_game()
