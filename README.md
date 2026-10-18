# 🧮 Python Calculator

A clean, dark-themed calculator built with Python and Tkinter. It has click sounds, smooth hover animations, a live result preview and full keyboard support. It needs no extra packages.

<p align="center">
  <img src="screenshots/calculator-empty.png" alt="Calculator on startup" width="260">
  &nbsp;&nbsp;&nbsp;
  <img src="screenshots/calculator-expression.png" alt="Calculator with a live preview" width="260">
</p>

---

## ✨ Features

- **Modern dark UI** with an orange operator column and a large display
- **Live preview**: the result appears above the display as you type (`96×69` shows `6624`)
- **Click sounds**: different tones for digits, operators, clear, equals and errors, generated in code so no audio files are needed
- **Smooth animations**: buttons fade on hover and flash when pressed
- **Keyboard support**: type with your keyboard as well as the mouse
- **Safe maths**: expressions are parsed instead of passed to `eval()`
- **Friendly errors**: dividing by zero shows a message instead of crashing

---

## 🚀 Getting Started

### Requirements

- Python **3.8 or newer**
- Tkinter (included with the standard Python installer on Windows and macOS)

> **Linux:** if Tkinter is missing, install it with `sudo apt install python3-tk`.

### Run it

```bash
python calculator.py
```

---

## ⌨️ Keyboard Shortcuts

| Key                     | Action                |
| ----------------------- | --------------------- |
| `0` – `9`               | Enter digits          |
| `+` `-` `*` `/`         | Add, subtract, multiply, divide |
| `(` `)`                 | Brackets              |
| `.`                     | Decimal point         |
| `Enter` or `=`          | Calculate             |
| `Backspace`             | Delete last character |
| `Esc`                   | Clear everything      |

---

## 🔊 Sound Support

Sounds work out of the box on most systems:

| Platform | Player used |
| -------- | ----------- |
| Windows  | `winsound` (built in) |
| macOS    | `afplay` (built in)   |
| Linux    | `aplay` (needs ALSA utilities) |

If no sound player is found, the calculator runs silently and still works normally.

---

## 📁 Project Structure

```
.
├── calculator.py
├── screenshots/
│   ├── calculator-empty.png
│   └── calculator-expression.png
└── README.md
```

---

## 🛠️ Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
