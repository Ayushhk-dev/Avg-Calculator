# Simple calculator using tkinter
# Dark theme, click sounds, hover animation and keyboard support

import ast
import math
import operator
import os
import struct
import subprocess
import sys
import tempfile
import tkinter as tk
import wave

expression = ""  # what the user has typed so far
just_calculated = False  # True right after pressing =

BG = "#1c1c1e"
FONT = "Helvetica"
OPERATORS = "÷×−+"


# Sounds


def make_beep(path, freq, ms):
    rate = 44100
    total = int(rate * ms / 1000)
    data = bytearray()
    for i in range(total):
        fade = min(1, i / 200, (total - i) / 800)
        data += struct.pack(
            "<h", int(10000 * fade * math.sin(2 * math.pi * freq * i / rate))
        )
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(bytes(data))


sound_folder = tempfile.mkdtemp()
sounds = {}
for name, freq, ms in [
    ("click", 900, 35),
    ("op", 650, 40),
    ("clear", 420, 70),
    ("equals", 1000, 150),
    ("error", 220, 160),
]:
    sounds[name] = os.path.join(sound_folder, name + ".wav")
    make_beep(sounds[name], freq, ms)


def play(name):
    path = sounds[name]
    try:
        if sys.platform.startswith("win"):
            import winsound

            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif sys.platform == "darwin":
            subprocess.Popen(["afplay", path])
        else:
            subprocess.Popen(["aplay", path], stderr=subprocess.DEVNULL)
    except Exception:
        pass


# Math

ALLOWED = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def solve(node):
    if isinstance(node, ast.Expression):
        return solve(node.body)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED:
        return ALLOWED[type(node.op)](solve(node.left), solve(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -solve(node.operand)
    raise ValueError("bad expression")


def evaluate(text):
    text = text.replace("÷", "/").replace("×", "*").replace("−", "-")
    return solve(ast.parse(text, mode="eval"))


def clean_up(text):
    """Remove dangling operators and close any open brackets."""
    while text and text[-1] in OPERATORS + "(":
        text = text[:-1]
    return text + ")" * (text.count("(") - text.count(")"))


def nice_number(n):
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return format(n, ".12g")


# Button logic


def update_screen():
    screen.config(
        text=expression or "0",
        fg="white",
        font=(FONT, 38 if len(expression) <= 10 else 24),
    )
    small.config(text="")
    # show a live preview of the answer while typing
    if expression and not just_calculated:
        try:
            if any(op in expression[1:] for op in OPERATORS):
                small.config(text=nice_number(evaluate(clean_up(expression))))
        except Exception:
            pass


def press(key):
    global expression, just_calculated

    if key == "C":
        expression = ""
        just_calculated = False
        play("clear")

    elif key == "⌫":
        expression = "" if just_calculated else expression[:-1]
        just_calculated = False
        play("clear")

    elif key == "=":
        calculate()
        return

    elif key in OPERATORS:
        if not expression and key != "−":
            return play("error")
        if expression and expression[-1] in OPERATORS:
            expression = expression[:-1]  # swap the old operator for the new one
        expression += key
        just_calculated = False
        play("op")

    else:  # digits, brackets and the decimal point
        if just_calculated:
            expression = ""
            just_calculated = False
        if key == ".":
            current = expression
            for op in OPERATORS + "()":
                current = current.split(op)[-1]
            if "." in current:
                return play("error")
        expression += key
        play("click")

    update_screen()


def calculate():
    global expression, just_calculated
    try:
        text = clean_up(expression)
        answer = nice_number(evaluate(text))
    except ZeroDivisionError:
        return show_error("Can't divide by zero")
    except Exception:
        return show_error("Error")
    small.config(text=text + " =")
    expression = answer
    just_calculated = True
    screen.config(text=answer)
    play("equals")


def show_error(message):
    global expression
    expression = ""
    play("error")
    screen.config(text=message, fg="#ff453a", font=(FONT, 20))
    window.after(1200, update_screen)


# Window

window = tk.Tk()
window.title("Calculator")
window.configure(bg=BG)
window.resizable(False, False)

small = tk.Label(window, bg=BG, fg="#8e8e93", font=(FONT, 13), anchor="e")
small.pack(fill="x", padx=18, pady=(18, 0))
screen = tk.Label(window, text="0", bg=BG, fg="white", font=(FONT, 38), anchor="e")
screen.pack(fill="x", padx=18, pady=(0, 10))

grid = tk.Frame(window, bg=BG)
grid.pack(padx=12, pady=(0, 14))


def fade(button, color, steps=6):
    """Smoothly change the button colour instead of snapping to it."""
    if getattr(button, "job", None):
        button.after_cancel(button.job)
    start = button.winfo_rgb(button["bg"])
    end = button.winfo_rgb(color)

    def step(i):
        mixed = [int((s + (e - s) * i / steps) / 256) for s, e in zip(start, end)]
        button.config(bg="#%02x%02x%02x" % tuple(mixed))
        if i < steps:
            button.job = button.after(15, step, i + 1)

    step(1)


# color schemes
number_style = ("#2c2c2e", "#3a3a3c", "#555558", "white")
gray_style = ("#a5a5a5", "#bdbdbd", "#e0e0e0", "black")
orange_style = ("#ff9f0a", "#ffb340", "#ffd080", "white")

layout = [
    ["C", "(", ")", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="],
]

buttons = {}
for r, row in enumerate(layout):
    for c, key in enumerate(row):
        if key in OPERATORS + "=":
            normal, hover, pressed, text_color = orange_style
        elif key in "C()⌫":
            normal, hover, pressed, text_color = gray_style
        else:
            normal, hover, pressed, text_color = number_style

        b = tk.Label(
            grid, text=key, bg=normal, fg=text_color, font=(FONT, 20), cursor="hand2"
        )
        b.grid(row=r, column=c, padx=5, pady=5, ipadx=14, ipady=14, sticky="nsew")
        b.colors = (normal, hover, pressed)

        b.bind("<Enter>", lambda e, b=b: fade(b, b.colors[1]))
        b.bind("<Leave>", lambda e, b=b: fade(b, b.colors[0]))
        b.bind("<ButtonPress-1>", lambda e, b=b: b.config(bg=b.colors[2]))
        b.bind(
            "<ButtonRelease-1>", lambda e, b=b, k=key: (fade(b, b.colors[1]), press(k))
        )
        buttons[key] = b

for i in range(4):
    grid.columnconfigure(i, weight=1, uniform="col")


# Keyboard support

key_names = {
    "*": "×",
    "/": "÷",
    "-": "−",
    "+": "+",
    "(": "(",
    ")": ")",
    ".": ".",
    "=": "=",
    "\r": "=",
    "\x08": "⌫",
    "\x1b": "C",
}


def on_key(event):
    key = event.char if event.char.isdigit() else key_names.get(event.char)
    if key is None:
        return
    b = buttons[key]
    b.config(bg=b.colors[2])
    window.after(90, lambda: fade(b, b.colors[0]))
    press(key)


window.bind("<Key>", on_key)
window.mainloop()
