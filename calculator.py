import tkinter as tk
import math

def num(s):
    return float(s.replace(",", "."))

def fmt(x):
    return str(int(x)) if x == int(x) else str(round(x, 10)).replace(".", ",")

def click(key):
    global current, first, op, reset
    if current == "Error" and key not in ("C", "CE"):
        return
    if key in "0123456789,":
        if reset:
            current = "0" if key == "," else ""
            reset = False
        if key == "," and "," in current:
            return
        if current == "0" and key != ",":
            current = ""
        current += key
    elif key in ["+", "-", "×", "÷"]:
        if op and not reset:
            calc()
            if current == "Error":
                entry_var.set(current)
                return
        first, op, reset = num(current), key, True
    elif key == "=":
        calc()
    elif key == "C":
        current, first, op, reset = "0", None, None, True
    elif key == "CE":
        current, reset = "0", True
    elif key == "←":
        current = current[:-1]
        if current in ("", "-"):
            current = "0"
    elif key == "±":
        current = fmt(-num(current)) if num(current) != 0 else "0"
    elif key in ["√", "x²", "1/x", "%"]:
        try:
            x = num(current)
            r = math.sqrt(x) if key == "√" else x ** 2 if key == "x²" else 1 / x if key == "1/x" else x / 100
            current = fmt(r)
        except (ValueError, OverflowError, ZeroDivisionError):
            current = "Error"
        reset = True
    entry_var.set(current)

def calc():
    global current, op, reset
    if op is None:
        return
    b = num(current)
    try:
        if op == "+": r = first + b
        elif op == "-": r = first - b
        elif op == "×": r = first * b
        else: r = first / b  # first — первое число, b — второе
        current = fmt(r)
    except (ZeroDivisionError, OverflowError):
        current = "Error"
    op, reset = None, True

def show_info():
    top = tk.Toplevel(Tk1)
    top.title("О программе")
    top.grab_set()
    top.geometry("300x150")
    tk.Label(top, text="Разработчик: Иванов И.И.\n\nСпасибо моим родителям\nза поддержку и терпение!", justify="center").pack(pady=20)
    tk.Button(top, text="ОК", command=top.destroy).pack()

Tk1 = tk.Tk()
Tk1.title("Калькулятор")
Tk1.geometry("300x400")
Tk1.resizable(False, False)

entry_var = tk.StringVar(value="0")
entry = tk.Entry(Tk1, textvariable=entry_var, font=("Arial", 24), justify="right", state="readonly")
entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=10)

rows = ["% √ x² 1/x", "CE C ← ÷", "7 8 9 ×", "4 5 6 -", "1 2 3 +", "± 0 , ="]
current, first, op, reset = "0", None, None, True

for row, line in enumerate(rows, 1):
    for col, text in enumerate(line.split()):
        btn = tk.Button(Tk1, text=text, font=("Arial", 14), command=lambda t=text: click(t))
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

Tk1.grid_rowconfigure(0, weight=2)
for i in range(1, 7): Tk1.grid_rowconfigure(i, weight=1)
for i in range(4): Tk1.grid_columnconfigure(i, weight=1)

tk.Button(Tk1, text="Инфо", command=show_info, font=("Arial", 10)).grid(row=7, column=0, columnspan=4, sticky="nsew")
Tk1.mainloop()
