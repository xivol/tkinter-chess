def print_all(window):
    """
    Print all tkinter events
    https://www.tcl.tk/man/tcl8.3/TkCmd/bind.html#M7
    """
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
