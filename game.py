import math
from time import time
import tkinter
import time
import sys
import os.path

_Windows = sys.platform == 'win32'

_root_window = None
_canvas = None
_canvas_xs = None
_canvas_ys = None
_canvas_x = None
_canvas_y = None
_canvas_col = None
_canvas_tsize = 12
_canvas_tserifs = 0

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))


def colorToVector(color):
    return [int(x, 16) / 256.0 for x in [color[1:3], color[3:5], color[5:7]]]


if _Windows:
    _canvas_tfonts = ['times new roman', 'lucida console']
else:
    _canvas_tfonts = ['times', 'lucidasans-24']
    pass  # XXX need defaults here


def sleep(secs):
    global _root_window
    if _root_window == None:
        time.sleep(secs)
    else:
        _root_window.update_idletasks()
        _root_window.after(int(1000 * secs), _root_window.quit)
        _root_window.mainloop()

def refresh(secs):
    # clear_screen()
    _canvas.update_idletasks()
    sleep(secs)

def begin_graphics(width=800, height=600, color=formatColor(0, 0, 0), title=None):

    global _root_window, _canvas, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys, _bg_color

    # Check for duplicate call
    if _root_window is not None:
        # Lose the window.
        _root_window.destroy()

    # Create the root window
    _root_window = tkinter.Tk()
    _root_window.protocol('WM_DELETE_WINDOW', _destroy_window)
    _root_window.title(title or 'Graphics Window')
    _root_window.resizable(0, 0)

    # width = 0.5 * _root_window.winfo_screenwidth()
    # height = 0.75 * _root_window.winfo_screenheight()

    # width = 500 if width < 500 else width
    # height = 500 if height < 500 else height

    # _root_window.geometry("%dx%d" % (width, height))

    # Save the canvas size parameters
    _canvas_xs, _canvas_ys = width - 1, height - 1
    _canvas_x, _canvas_y = 0, _canvas_ys
    _bg_color = color

    # Create the canvas object
    try:
        _canvas = tkinter.Canvas(_root_window, width=width, height=height)
        _canvas.pack()
        draw_background()
        _canvas.update()
    except:
        _root_window = None
        raise

def draw_background():
    corners = [(0, 0), (0, _canvas_ys),
               (_canvas_xs, _canvas_ys), (_canvas_xs, 0)]
    polygon(corners, _bg_color, fillColor=_bg_color,
            filled=True, smoothed=False)

def _destroy_window(event=None):
    sys.exit(0)
#    global _root_window
#    _root_window.destroy()
#    _root_window = None
    # print "DESTROY"

def end_graphics():
    global _root_window, _canvas, _mouse_enabled
    try:
        try:
            sleep(0.1)
            if _root_window != None:
                _root_window.destroy()
        except SystemExit as e:
            print(('Ending graphics raised an exception:', e))
    finally:
        _root_window = None
        _canvas = None
        _mouse_enabled = 0


def clear_screen(background=None):
    global _canvas_x, _canvas_y
    _canvas.delete('all')
    draw_background()
    _canvas_x, _canvas_y = 0, _canvas_ys

def polygon(coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
    c = []
    for coord in coords:
        c.append(coord[0])
        c.append(coord[1])
    if fillColor == None:
        fillColor = outlineColor
    if filled == 0:
        fillColor = ""
    poly = _canvas.create_polygon(
        c, outline=outlineColor, fill=fillColor, smooth=smoothed, width=width)
    if behind > 0:
        _canvas.tag_lower(poly, behind)  # Higher should be more visible
    return poly

def hexagon(pos, r, color, bg_color, filled=1, behind=0):
    x, y = pos
    diff_y = r * math.sin(math.radians(30))
    diff_x = r * math.cos(math.radians(30))
    coords = [(x, y - r), (x + diff_x, y - diff_y), (x + diff_x, y + diff_y), (x, y + r), (x - diff_x, y + diff_y), (x - diff_x, y - diff_y)]
    return polygon(coords, color, bg_color, filled, 0, behind=behind)

def circle(pos, r, outlineColor, fillColor, endpoints=None, style='chord', width=2):
    x, y = pos
    x0, x1 = x - r - 1, x + r
    y0, y1 = y - r - 1, y + r
    if endpoints == None:
        e = [0, 359]
    else:
        e = list(endpoints)
    while e[0] > e[1]:
        e[1] = e[1] + 360

    return _canvas.create_arc(x0, y0, x1, y1, outline=outlineColor, fill=fillColor,
                              extent=e[1] - e[0], start=e[0], style=style, width=width)