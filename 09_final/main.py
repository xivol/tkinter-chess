import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
from chess import Board, WHITE


class Piece:
    def __init__(self, x, y, size, canvas, piece=None):
        self.x = x
        self.y = y
        self.size = size
        self.chess = piece
        self.id = self.create_on(canvas)

    def create_on(self, canvas):
        x, y, size = self.x, self.y, self.size
        image = Image.open(f'image/{self.chess}.png')
        image.thumbnail((size, size), Image.ANTIALIAS)
        self.imgTk = ImageTk.PhotoImage(image)
        x += size // 2
        y += size // 2
        return canvas.create_image(x, y, image=self.imgTk)

        # if self.chess.get_color() == WHITE:
        #     return canvas.create_oval(x, y, x + size, y + size, fill='white')
        # else:
        #     return canvas.create_oval(x, y, x + size, y + size, fill='black')

    def move_to(self, canvas, x, y):
        px, py = self.x, self.y
        pw = self.size
        ph = self.size
        canvas.move(self.id,
                    x - px - pw // 2,
                    y - py - ph // 2)
        self.x = x - pw // 2
        self.y = y - ph // 2

    def pick(self, canvas):
        # canvas.itemconfig(self.id, fill='orange')
        canvas.tag_raise(self.id)

    def put(self, canvas):
        pass
        # if self.chess.get_color() == WHITE:
        #     canvas.itemconfig(self.id, fill='white')
        # else:
        #     canvas.itemconfig(self.id, fill='black')


def init_canvas(canvas, size, board):
    all_pieces = []
    step = size // 8
    for i in range(8):
        for j in range(8):
            if i % 2 == j % 2:
                canvas.create_rectangle(i * step, j * step,
                                        (i + 1) * step, (j + 1) * step,
                                        fill='gray', width=0)

    psize = size // 8
    for i in range(8):
        for j in range(8):
            x = j * step + (step - psize) // 2
            y = (7 - i) * step + (step - psize) // 2
            if board.field[i][j]:
                p = Piece(x, y, psize, canvas, board.field[i][j])
                all_pieces.append(p)

    return all_pieces


window = tkinter.Tk()
window.title('Chess Game')
window.resizable(False, False)

size = 600
canvas = tkinter.Canvas(window, bg='white', height=size, width=size)
canvas.pack(fill=tkinter.NONE)

label = tkinter.Label(canvas, text='Hello World')
label.place(x=10, y=10)
label.configure(font=('Arial', 12),
                bg='#0ff',
                fg='black')

board = Board()
if board.current_player_color() == WHITE:
    label.configure(text="Ход белых")
else:
    label.configure(text="Ход черных")

all_pieces = init_canvas(canvas, size, board)
clicked = None


def board_coords(canvas, x, y):
    w = canvas.winfo_width() // 8
    h = canvas.winfo_height() // 8
    return x // w, 7 - y // h


def canvas_coords(canvas, c, r):
    size = canvas.winfo_width()
    step = size // 8
    psize = size // 9
    x = c * step + step // 2
    y = (7 - r) * step + step // 2
    return x, y


def get_piece(x, y):
    for piece in all_pieces:
        px = piece.x + piece.size // 2
        py = piece.y + piece.size // 2
        dist = (px - x) ** 2 + (py - y) ** 2
        if dist < piece.size ** 2 // 4 and \
                board.current_player_color() == piece.chess.get_color():
            return piece


def click(ev):
    global clicked
    if clicked:
        return
    x, y = ev.x, ev.y
    c, r = board_coords(canvas, x, y)
    clicked = get_piece(x, y)
    if clicked:
        clicked.start_pos = c, r
        clicked.pick(canvas)


def move(ev):
    x, y = ev.x, ev.y
    if clicked:
        clicked.move_to(canvas, x, y)


def release(ev):
    global clicked
    x, y = ev.x, ev.y
    c, r = board_coords(canvas, x, y)

    if clicked:
        if board.move_piece(clicked.start_pos[1], clicked.start_pos[0], r, c):
            x, y = canvas_coords(canvas, c, r)
            removed = get_piece(x, y)
            if removed:
                canvas.delete(removed.id)
                all_pieces.remove(removed)

            clicked.move_to(canvas, x, y)
            clicked.put(canvas)
            clicked = None
            if board.current_player_color() == WHITE:
                label.configure(text="Ход белых")
            else:
                label.configure(text="Ход черных")
        else:
            x, y = canvas_coords(canvas, *clicked.start_pos)
            clicked.move_to(canvas, x, y)
            clicked.put(canvas)
            clicked = None

            title = window.winfo_toplevel().title()
            messagebox.showwarning(title,
                                   'Координаты некорректы!\nПопробуйте другой ход.')


canvas.bind('<ButtonPress>', click)
canvas.bind('<Motion>', move)
canvas.bind('<ButtonRelease>', release)

window.mainloop()
