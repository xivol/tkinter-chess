from copy import deepcopy
from itertools import chain

WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class ChessPiece:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def __str__(self):
        if self.color == WHITE:
            return 'w' + self.char()
        else:
            return 'b' + self.char()

    def char(self):
        return ' '

    def can_move(self, board, row, col, row1, col1):
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Rook(ChessPiece):
    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True


class Pawn(ChessPiece):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight(ChessPiece):
    '''Класс коня. Пока что заглушка, которая может ходить в любую клетку.'''

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём


class King(ChessPiece):
    '''Класс короля. Пока что заглушка, которая может ходить в любую клетку.'''

    def char(self):
        return 'K'


class Queen(ChessPiece):
    '''Класс ферзя. Пока что заглушка, которая может ходить в любую клетку.'''

    def char(self):
        return 'Q'


class Bishop(ChessPiece):
    '''Класс слона. Пока что заглушка, которая может ходить в любую клетку.'''

    def char(self):
        return 'B'


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
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')

        if board.is_check():
            if board.is_mate():
                print('Шах и Мат!')
                break
            else:
                print('Шах!')

        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]
        self.kings = {WHITE: (0, 4), BLACK: (7, 4)}

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if isinstance(piece, King):
            self.kings[self.color] = (row1, col1)
        self.color = opponent(self.color)
        return True

    def get_king_pos(self, color):
        return self.kings[color]

    def is_under_attack_by(self, color, row, col):
        for i in range(8):
            for j in range(8):
                piece = self.field[i][j]
                if piece is None:
                    continue
                if piece.get_color() == color and \
                        piece.can_attack(self, i, j, row, col):
                    return True
        return False

    def is_check(self):
        k_row, k_col = self.get_king_pos(self.color)
        op_color = opponent(self.color)
        return self.is_under_attack_by(op_color, k_row, k_col)

    def is_mate(self):
        if not self.is_check(self.color):
            return False
        k_row, k_col = self.get_king_pos(self.color)
        king = self.field[k_row][k_col]
        op_color = opponent(self.color)

        for i in range(k_row - 1, k_row + 1):
            for j in range(k_col - 1, k_col + 1):
                if king.can_move(self, k_row, k_col, i, j) and \
                        not self.is_under_attack_by(op_color, i, j):
                    return False

        # ещё нужно проверить что нельзя
        # подставить под удар другую фигуру
        # ещё нужно проверить что нельзя
        # атаковать бъющую фигуру и
        # выйти таким образом из под шаха
        return True


# __name__ -- специальная переменная, в которую python записывает имя
# файла (без .py), если этот файл импортирован из друго, и "__main__", если
# этот файл запущен как программа.
# Другими словами, следующие две строчки:
#   запустят функцию main, если файл запущен как программа;
#   не сделают ничего, если этот файл импортирован из другого.
# Второй случай реализуется, например, когда тестирующий скрипт импортирует
# классы из вашего скрипта. В этом случае функця main не будет работать
# и портить вывод теста.

if __name__ == "__main__":
    main()
