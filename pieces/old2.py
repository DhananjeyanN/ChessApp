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

    def move(self, board, source, dest, log):
        r_obj = self.is_legit_move(board=board, source=source, dest=dest, log=log)
        typ = type(r_obj)
        if typ == bool and r_obj is True:
            log.add_log(source=source, dest=dest, piece=self)
            board.move_piece(start=source, stop=dest, piece=self)
            return True
        elif typ is Queen or typ is Bishop or typ is Knight or typ is Rook:
            log.add_log(source=source, dest=dest, piece=self)
            board.move_piece(start=source, stop=dest, piece=r_obj)
            return True
        return False

    def __str__(self):
        pass


class Pawn(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board, log, check_promotion= True):
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
            if check_promotion:
                cbp = self.can_be_promoted(dest=dest, board=board, log=log)
                if cbp:
                    return cbp
            return True
        if y1 == start_row and y2 == y1 + direction * 2 and board[y2][x2].is_empty() and board[y1 + direction][x1]:
            if check_promotion:
                cbp = self.can_be_promoted(dest=dest, board=board, log=log)
                if cbp:
                    return cbp
            return True
        if not board[y2][x2].is_empty(): #y1,x3 -> y7,x4
            if ((x1 + 1 == x2 or x1 - 1 == x2) and y2 == y1 + direction) and (board[y2][x2].get_piece().get_color() != board[y1][x1].get_piece().get_color()):
                log.add_capture(piece=board[y2][x2].get_piece())
                if check_promotion:
                    cbp = self.can_be_promoted(dest=dest, board=board, log=log)
                    if cbp:
                        return cbp
                return True
        return False

    def can_be_promoted(self, dest, board, log):
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

    def can_en_passent(self):
        pass

    def __str__(self):
        return f'{self.get_color()[0]}P'


class Queen(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        step_y = 0
        step_x = 0
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
        if (x1 - x2 != 0 and y1 - y2 == 0) or (x1 - x2 == 0 and y1 - y2 != 0) or (abs(x2 - x1) == abs(y2 - y1)):
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == board[y1][x1].get_piece().get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}Q'


class Rook(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board, log):
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
        if x1 - x2 != 0 and y1 - y2 == 0 or x1 - x2 == 0 and y1 - y2 != 0:
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == board[y1][x1].get_piece().get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
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
                if board[y2][x2].get_piece().get_color() == board[y1][x1].get_piece().get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}B'


class King(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        if (abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or (abs(y1 - y2) == 1 and abs(x1 - x2) == 0) or (
                abs(x1 - x2) == 1 and abs(y1 - y2) == 1):
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == board[y1][x1].get_piece().get_color():
                    return False
                else:
                    log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def can_castle(self):
        pass

    def __str__(self):
        return f'{self.get_color()[0]}K'


class Knight(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, source, dest, board, log):
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

    def __str__(self):
        return f'{self.get_color()[0]}N'


class Board:
    def __init__(self):
        self.board = [[Square() for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                s = Square()
                self.board[i][j] = s

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
        self.board[x1][y1].set_piece(piece=None)
        self.board[x2][y2].set_piece(piece=piece)

    def get_piece(self, cord):
        x, y = cord
        return self.board[y][x].get_piece()

    def has_piece(self, cord, piece):
        x, y = cord
        if self.board[y][x].get_piece() == piece:
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


class Game:
    def __init__(self):
        self.board = Board()
        self.log = BoardLog()
        self.pw = None
        self.pb = None
        self.turn = None
        self.white_king = None
        self.black_king = None
        self.wkp = None
        self.bkp = None
        self.checked_king = None

    def start_game(self):
        self.white_king, self.black_king = self.board.initialize_board()

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
        move_color = self.turn
        origin, dest = self.get_input()
        color = self.board.board[origin[0]][origin[1]].get_piece().get_color()
        print(move_color, color, 'COLOR')
        if move_color == color:
            if self.board.board[origin[0]][origin[1]].get_piece().move(board=self.board, source=origin, dest=dest, log=self.log):
                self.switch_turn()
                return True
            else:
                print('MOVE NOT VALID TRY AGAIN!!!')
                return False
        else:
            print('WRONG COLOR TRY AGAIN!!!')
            return False

    def player_setup(self):
        pw = input('Enter White Player Name: ')
        pb = input('Enter Black Player Name: ')
        turn = input('Enter the name of 1st mover: ')
        if turn == pw:
            self.turn = 'white'
        else:
            self.turn = 'black'

    def get_king_pos(self):
        if self.wkp is None and self.bkp is None:
            self.wkp, self.bkp = (7, 4), (0, 4)
        else:
            log_check = self.log.logs[-1]
            if log_check[0] == self.white_king:
                self.wkp = log_check[2]
            elif log_check[0] == self.black_king:
                self.bkp = log_check[2]

        print('WHITE KING POS: ', self.wkp, 'BLACK KING POS: ', self.bkp)

    def determine_check(self, target_king):
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y].get_piece()
                if piece is not None:
                    if type(piece) is not Pawn:
                        if piece.get_color() == 'white':
                            if piece.is_legit_move(source=(x, y), dest=target_king, board=self.board, log=self.log):
                                return 'black'
                        else:
                            if piece.is_legit_move(source=(x, y), dest=target_king, board=self.board, log=self.log):
                                return 'white'
                    else:
                        if piece.get_color() == 'white':
                            if piece.is_legit_move(source=(x, y), dest=target_king, board=self.board, log=self.log, check_promotion=False):
                                return 'black'
                        else:
                            if piece.is_legit_move(source=(x, y), dest=target_king, board=self.board, log=self.log, check_promotion=False):
                                return 'white'
        return ''

    def is_checkmate(self, player_turn):
        print(player_turn, 'PLAYER TURN')
        pieces = []
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y].get_piece()
                if piece and piece.get_color() == self.turn:
                    pieces.append(piece)
                    legal_moves = self.generate_legal_moves(piece=piece, piece_pos=(x,y))
                    print(legal_moves)
                    for s, d in legal_moves:
                        x2, y2 = d
                        captured_piece = self.board.board[x2][y2].get_piece()
                        self.board.move_piece(start=s, stop=d, piece=piece)
                        is_check = self.determine_check(target_king= self.bkp if self.turn == 'white' else self.wkp)
                        if not is_check:
                            self.board.move_piece(start=d,stop=s, piece=piece)
                            if captured_piece:
                                self.board.board[x2][y2].set_piece(piece=captured_piece)
                            print('FalseEEEE')
                            return False
                        else:
                            self.board.move_piece(start=d, stop=s, piece=piece)
                            if captured_piece:
                                self.board.board[x2][y2].set_piece(piece=captured_piece)
        return True

    def generate_legal_moves(self, piece, piece_pos):
        l_moves = []
        for x in range(8):
            for y in range(8):
                if piece.is_legit_move(dest=(x,y), source=piece_pos, board=self.board, log=self.log):
                    l_moves.append((piece_pos, (x,y)))
        return l_moves

    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def run_game(self):
        i = 0
        self.start_game()
        self.player_setup()
        while i != 1:
            self.print_board()
            if self.move_piece():
                self.get_king_pos()
                if self.turn:
                    target_king = self.bkp
                else:
                    target_king = self.wkp
                is_check = self.determine_check(target_king)
                if is_check:
                    print(f'{is_check} King In Check!!!')
                    if self.is_checkmate(player_turn=self.turn):
                        if self.turn == 'white':
                            turn = 'black'
                        else:
                            turn = 'white'
                        print(f'Game Over!!! PLAYER {turn} WINS!!!')


game = Game()
game.run_game()
