import tkinter

window = tkinter.Tk()
events = """Activate
Destroy
Map
ButtonPress
Enter
MapRequest
ButtonRelease
Expose
Motion
Circulate
FocusIn
MouseWheel
FocusOut
Property
Colormap
Gravity
Reparent
Configure
KeyPress
ResizeRequest
ConfigureRequest
KeyRelease
Unmap
Create
Leave
Visibility
Deactivate"""
for ev in events.split():
    window.bind('<' + ev + '>', lambda ev: print(ev))

canvas = tkinter.Canvas(window, bg='white', height=600, width=600)
canvas.pack(fill=tkinter.BOTH)

label = tkinter.Label(canvas, text='Hello World')
label.place(x=10, y=10)
label.configure(text="goodbye World!")

all_pieces = []


class Piece:
    def __init__(self, x, y, size, canvas):
        self.x = x
        self.y = y
        self.size = size
        self.id = self.create_on(canvas)

    def create_on(self, canvas):
        x, y, size = self.x, self.y, self.size
        return canvas.create_oval(x, y, x + size, y + size, fill='purple')

    def move_to(self, canvas, x, y):
        px, py = self.x, self.y
        pw = self.size
        ph = self.size
        canvas.move(self.id,
                    x - px - pw // 2,
                    y - py - ph // 2)
        self.x = x - pw // 2
        self.y = y - ph // 2


for i in range(8):
    x = i * 600 // 9
    y = x
    size = 600 // 9
    all_pieces.append(Piece(x, y, size, canvas))

clicked = None


def click(ev):
    global clicked
    if clicked:
        return
    x, y = ev.x, ev.y
    for piece in all_pieces:
        px = piece.x + piece.size // 2
        py = piece.y + piece.size // 2
        dist = (px - x) ** 2 + (py - y) ** 2
        if dist < piece.size ** 2 // 4:
            clicked = piece
            break
    if clicked:
        canvas.itemconfig(clicked.id, fill='red')


def move(ev):
    x, y = ev.x, ev.y
    if clicked:
        clicked.move_to(canvas, x, y)


def release(ev):
    global clicked
    x, y = ev.x, ev.y
    if clicked:
        canvas.itemconfig(clicked.id, fill='purple')
        clicked = None


canvas.bind('<ButtonPress>', click)
canvas.bind('<Motion>', move)
canvas.bind('<ButtonRelease>', release)

window.mainloop()
