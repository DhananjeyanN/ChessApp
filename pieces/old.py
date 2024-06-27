class Piece:
    def __init__(self, color, url):
        self.__color = color
        self.__url = url

    def get_color(self):
        return self.__color

    def get_url(self):
        return self.__url

    def is_legit_move(self, board, source, dest, log):
        pass

    def move(self, board, source, dest, log):
        r_obj = self.is_legit_move(board=board, source=source, dest=dest, log=log)
        if isinstance(r_obj, bool) and r_obj:
            log.add_log(source=source, dest=dest, piece=self)
            board.move_piece(start=source, stop=dest, piece=self)
            return True
        elif isinstance(r_obj, Piece):
            log.add_log(source=source, dest=dest, piece=self)
            board.move_piece(start=source, stop=dest, piece=r_obj)
            return True
        return False

    def __str__(self):
        pass

class Pawn(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, board, source, dest, log, check_promotion=True):
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

        if y1 == start_row and y2 == y1 + direction * 2 and board[y2][x2].is_empty() and board[y1 + direction][x1].is_empty():
            return True

        if not board[y2][x2].is_empty():
            if (x1 + 1 == x2 or x1 - 1 == x2) and y2 == y1 + direction and board[y2][x2].get_piece().get_color() != self.get_color():
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
            piece_choice = input('Enter Piece Choice (queen, knight, bishop, rook): ').lower()
            piece_map = {
                'queen': Queen,
                'knight': Knight,
                'bishop': Bishop,
                'rook': Rook
            }
            if piece_choice in piece_map:
                p = piece_map[piece_choice](color=self.get_color(), url=f'images/{self.get_color()}-{piece_choice}.png')
                log.add_promotion(piece=board[y][x].get_piece(), cord=dest, new_piece=p)
                return p
            else:
                return False
        return False

    def __str__(self):
        return f'{self.get_color()[0]}P'

class Queen(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, board, source, dest, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        step_y = (y2 - y1) // max(1, abs(y2 - y1))
        step_x = (x2 - x1) // max(1, abs(x2 - x1))
        if (x1 - x2 == 0 or y1 - y2 == 0 or abs(x2 - x1) == abs(y2 - y1)):
            check_x = x1 + step_x
            check_y = y1 + step_y
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}Q'


class Rook(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, board, source, dest, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        step_y = (y2 - y1) // max(1, abs(y2 - y1)) if y1 != y2 else 0
        step_x = (x2 - x1) // max(1, abs(x2 - x1)) if x1 != x2 else 0
        if x1 == x2 or y1 == y2:
            check_x = x1 + step_x
            check_y = y1 + step_y
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}R'


class Bishop(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, board, source, dest, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        step_y = (y2 - y1) // max(1, abs(y2 - y1))
        step_x = (x2 - x1) // max(1, abs(x2 - x1))
        if abs(x2 - x1) == abs(y2 - y1):
            check_x = x1 + step_x
            check_y = y1 + step_y
            while check_x != x2 or check_y != y2:
                if not board[check_y][check_x].is_empty():
                    return False
                check_x += step_x
                check_y += step_y
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}B'


class King(Piece):
    def __init__(self, color, url):
        super().__init__(color, url)

    def is_legit_move(self, board, source, dest, log):
        board = board.board
        y1, x1 = source
        y2, x2 = dest
        if (abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or (abs(y1 - y2) == 1 and abs(x1 - x2) == 0) or (
                abs(x1 - x2) == 1 and abs(y1 - y2) == 1):
            if not board[y2][x2].is_empty():
                if board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                log.add_capture(piece=board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}K'


class Knight(Piece):
    def init(self, color, url):
        super().init(color, url)

    def is_legit_move(self, board, source, dest, log):
        y1, x1 = source
        y2, x2 = dest
        if (abs(x1 - x2) == 2 and abs(y1 - y2) == 1) or (abs(x1 - x2) == 1 and abs(y1 - y2) == 2):
            if not board.board[y2][x2].is_empty():
                if board.board[y2][x2].get_piece().get_color() == self.get_color():
                    return False
                log.add_capture(piece=board.board[y2][x2].get_piece())
            return True
        return False

    def __str__(self):
        return f'{self.get_color()[0]}N'

class Board:
    def __init__(self):
        self.board = [[Square() for _ in range(8)] for _ in range(8)]

    def initialize_board(self):
        for row in self.board:
            for square in row:
                square.set_piece(None)
        for i in range(8):
            self.board[6][i].set_piece(Pawn(color='white', url='images/white-pawn.png'))
            self.board[1][i].set_piece(Pawn(color='black', url='images/black-pawn.png'))
        piece_positions = {
            Rook: [(0, 0), (0, 7), (7, 0), (7, 7)],
            Knight: [(0, 1), (0, 6), (7, 1), (7, 6)],
            Bishop: [(0, 2), (0, 5), (7, 2), (7, 5)],
            Queen: [(0, 3), (7, 3)],
            King: [(0, 4), (7, 4)]
        }
        for piece, positions in piece_positions.items():
            for y, x in positions:
                color = 'black' if y < 2 else 'white'
                self.board[y][x].set_piece(piece(color=color, url=f'images/{color}-{piece.__name__.lower()}.png'))
        return self.board[7][4].get_piece(), self.board[0][4].get_piece()

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
        return self.board[y][x].get_piece()

    def has_piece(self, cord, piece):
        x, y = cord
        return self.board[y][x].get_piece() == piece
class Square:
    def init(self):
        self.__piece = None

    def is_empty(self):
        return self.__piece is None

    def set_piece(self, piece):
        self.__piece = piece

    def get_piece(self):
        return self.__piece


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
        self.turn = 'white'  # Start with white by default
        self.is_white = True  # White starts first
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
        try:
            move = move.replace(",", " ").replace("to", " ").split()
            if len(move) != 2:
                raise ValueError
            file, rank = move[0][0], 8 - int(move[0][1])
            file2, rank2 = move[1][0], 8 - int(move[1][1])
            file = ord(file) - ord('a')
            file2 = ord(file2) - ord('a')
            return (rank, file), (rank2, file2)
        except (IndexError, ValueError):
            print("Invalid move format. Please use the format 'e2 e4' or 'e2,e4'.")
            return None, None

    def get_input(self):
        move = input('Enter Move ex: e2 e4 or e2,e4: ')
        return self.convert_input(move)

    def move_piece(self):
        origin, dest = self.get_input()
        if origin is None or dest is None:
            return False

        piece = self.board.board[origin[0]][origin[1]].get_piece()
        if piece and piece.get_color() == self.turn:
            if piece.move(board=self.board, source=origin, dest=dest, log=self.log):

                return True
            else:
                print('MOVE NOT VALID, TRY AGAIN!!!')
                return False
        else:
            print('WRONG COLOR, TRY AGAIN!!!')
            return False

    def player_setup(self):
        self.pw = input('Enter White Player Name: ')
        self.pb = input('Enter Black Player Name: ')
        turn = input('Enter the name of 1st mover (white/black): ').lower()
        if turn == 'white':
            self.turn = 'white'
            self.is_white = True
        elif turn == 'black':
            self.turn = 'black'
            self.is_white = False
        else:
            print("Invalid input. Starting with white by default.")
            self.turn = 'white'
            self.is_white = True

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

    def determine_check(self, pm=False):
        if pm:
            king_pos = self.bkp if self.turn == 'black' else self.wkp
            opponent_color = self.turn
        else:
            king_pos = self.bkp if self.turn == 'white' else self.wkp
            opponent_color = 'white' if self.turn == 'black' else 'black'
        print(opponent_color, 'OPPONENT KING', king_pos, self.turn)
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y].get_piece()
                if piece and piece.get_color() != opponent_color:
                    if isinstance(piece, Pawn):
                        if piece.is_legit_move(source=(x, y), dest=king_pos, board=self.board, log=self.log, check_promotion=False):
                            self.checked_king = self.board.board[king_pos[0]][king_pos[1]].get_piece()
                            print(opponent_color, 'OPPONENT KING2')
                            return True
                    else:
                        if piece.is_legit_move(source=(x, y), dest=king_pos, board=self.board, log=self.log):
                            self.checked_king = self.board.board[king_pos[0]][king_pos[1]].get_piece()
                            print(opponent_color, 'OPPONENT KING3')
                            return True
        self.checked_king = None
        return False

    def is_checkmate(self):
        original_turn = "black" if self.turn == 'white' else 'white'
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y].get_piece()
                if piece and piece.get_color() == original_turn:
                    legal_moves = self.generate_legal_moves(piece=piece, piece_pos=(x, y))
                    print(f'LEGAL MOVES FOR {piece} at {x, y}: {legal_moves}')
                    for s, d in legal_moves:
                        x2, y2 = d
                        x1, y1 = s
                        captured_piece = self.board.board[x2][y2].get_piece()
                        self.board.move_piece(start=s, stop=d, piece=piece)
                        self.board.print_board()
                        if self.determine_check(pm=False) is False:
                            self.board.move_piece(start=d, stop=s, piece=piece)
                            if captured_piece:
                                self.board.board[x2][y2].set_piece(piece=captured_piece)
                            print(f'CHECKMATE NOT POSSIBLE FOR {original_turn},legal move found!!! at {s, d}')
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
                if piece.is_legit_move(dest=(x, y), source=piece_pos, board=self.board, log=self.log):
                    l_moves.append((piece_pos, (x, y)))
        return l_moves

    def generate_legal_moves(self, piece, piece_pos):
        l_moves = []
        for x in range(8):
            for y in range(8):
                if piece.is_legit_move(dest=(x, y), source=piece_pos, board=self.board, log=self.log):
                    l_moves.append((piece_pos, (x, y)))
        return l_moves

    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
            self.is_white = False
        else:
            self.turn = 'white'
            self.is_white = True

    def run_game(self):
        self.start_game()
        self.player_setup()
        while True:
            self.print_board()
            if self.move_piece():
                self.get_king_pos()
                print(self.turn)
                if self.determine_check():
                    print(f'{"black" if self.turn =="white" else "white"} King In Check !!!')
                    if self.is_checkmate():
                        print(f'Game Over!!! PLAYER {self.turn} WINS!!!')
                        break
                self.switch_turn()

game = Game()
game.run_game()