import tkinter
import printer


window = tkinter.Tk()
printer.print_all(window)

window.title('Chess Game')
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg='yellow', height=300, width=300)
canvas.pack()

label = tkinter.Label(canvas, text='Hello World')
label.place(x=10, y=10)
label.configure(font=('Arial', 12),
                bg='blue',
                fg='#ff0')

window.mainloop()