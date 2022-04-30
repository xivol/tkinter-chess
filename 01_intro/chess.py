WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


# Инициализация цвета
color = WHITE
other_color = BLACK
# Проверка цвета
if color == BLACK:
    pass
# сравнение цветов
color == other_color
# Цвет противника
opponent_color = opponent(color)

def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class ChessPiece:
    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col

    def get_color(self):
        return self.color

    def __str__(self):
        if self.color == WHITE:
            return 'w' + self.char()
        else:
            return 'b' + self.char()

    def set_position(self, new_row, new_col):
        self.row = new_row
        self.col = new_col

    def char(self):
        return ' '

    def can_move(self, to_row, to_col):
        return False


class Rook(ChessPiece):
    def char(self):
        return 'R'

    def can_move(self, to_row, to_col):
        if self.row != to_row and \
            self.col != to_col:
            return False
        return True


class Pawn(ChessPiece):
    def char(self):
        return 'P'

    def can_move(self, to_row, to_col):
        if to_col != self.col:
            return False
        if self.color == WHITE:
            if to_row < self.row:
                return False
            if to_row - self.row > 2:
                return False
            if to_row - self.row == 2 and \
                self.row > 1:
                return False
        else:
            if to_row > self.row:
                return False
            if self.row - to_row > 2:
                return False
            if self.row - to_row == 2 and \
                self.row < 6:
                return False
        return True



class Board:
    def __init__(self):
        self.player_color = WHITE
        self.field = []
        for _ in range(8):
            self.field.append([None] * 8)
        self.init_board()

    def init_board(self):
        for i in range(8):
            self.field[1][i] = Pawn( 1, i, WHITE)
            self.field[6][i] = Pawn(6, i, BLACK)
        self.field[0][0] = Rook(0, 0, WHITE)
        self.field[0][7] = Rook(0, 7, WHITE)
        self.field[7][0] = Rook(7, 0, BLACK)
        self.field[7][7] = Rook(7, 7, BLACK)

    def cell(self, row, col):
        return self.field[row][col] if self.field[row][col] else '  '

    def current_player_color(self):
        return self.player_color

    def move_piece(self, from_row, from_col, to_row, to_col):
        if not correct_coords(from_row, from_col) or \
                not correct_coords(to_row, to_col):
            return False
        if from_row == to_row and from_col == to_col:
            return False  # нельзя пойти в ту же клетку

        piece = self.field[from_row][from_col]
        if piece is None:
            return False
        if piece.get_color() != self.player_color:
            return False
        if not piece.can_move(to_row, to_col):
            return False

        self.field[from_row][from_col] = None  # Снять фигуру.
        self.field[to_row][to_col] = piece  # Поставить на новое место.
        piece.set_position(to_row, to_col)
        self.player_color = opponent(self.player_color)
        return True


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


if __name__ == '__main__':
    main()