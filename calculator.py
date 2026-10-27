import tkinter as tk
from tkinter import messagebox
import math

def click(key):
    global current, op, reset
    if key in "0123456789,":
        if reset:
            current = "0" if key == "," else ""
            reset = False
        if key == "," and "," in current:
            return
        current += key
        entry_var.set(current)
    elif key in ["+", "-", "×", "÷"]:
        if current:
            calc()
        op = key
        reset = True
    elif key == "=":
        calc()
        op = None
        reset = True
    elif key == "C":
        current, op, reset = "0", None, True
        entry_var.set(current)
    elif key == "CE":
        current, reset = "0", True
        entry_var.set(current)
    elif key == "←":
        current = current[:-1] if len(current) > 1 else "0"
        entry_var.set(current)
    elif key == "±":
        current = str(-float(current)) if current not in ["0", ""] else "0"
        entry_var.set(current)
    elif key == "√":
        current = str(math.sqrt(float(current))) if float(current) >= 0 else "Error"
        entry_var.set(current)
        reset = True
    elif key == "x²":
        current = str(float(current) ** 2)
        entry_var.set(current)
        reset = True
    elif key == "1/x":
        current = str(1 / float(current)) if float(current) != 0 else "Error"
        entry_var.set(current)
        reset = True
    elif key == "%":
        current = str(float(current) / 100)
        entry_var.set(current)
        reset = True

def calc():
    global current, op
    if op and current:
        try:
            val = float(current)
            if op == "+": current = str(float(current) + val)
            elif op == "-": current = str(float(current) - val)
            elif op == "×": current = str(float(current) * val)
            elif op == "÷": current = str(float(current) / val) if val != 0 else "Error"
            entry_var.set(current)
        except:
            current = "Error"
            entry_var.set(current)
        reset = True

def show_info():
    top = tk.Toplevel(root)
    top.title("О программе")
    top.grab_set()
    top.geometry("300x150")
    tk.Label(top, text="Разработчик: Иванов И.И.\n\nСпасибо моим родителям\nза поддержку и терпение!", justify="center").pack(pady=20)
    tk.Button(top, text="ОК", command=top.destroy).pack()

root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x400")
root.resizable(False, False)

entry_var = tk.StringVar(value="0")
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 24), justify="right", state="readonly")
entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=10)

buttons = [
    ("%", 1, 0), ("√", 1, 1), ("x²", 1, 2), ("1/x", 1, 3),
    ("CE", 2, 0), ("C", 2, 1), ("←", 2, 2), ("÷", 2, 3),
    ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3),
    ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3),
    ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
    ("±", 6, 0), ("0", 6, 1), (",", 6, 2), ("=", 6, 3)
]

current, op, reset = "0", None, False

for text, row, col in buttons:
    cmd = lambda t=text: click(t) if t not in ["=", "C", "CE", "←", "±", "√", "x²", "1/x", "%"] else click(t)
    btn = tk.Button(root, text=text, font=("Arial", 14), command=cmd)
    btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

root.grid_rowconfigure(0, weight=2)
for i in range(1, 7): root.grid_rowconfigure(i, weight=1)
for i in range(4): root.grid_columnconfigure(i, weight=1)

tk.Button(root, text="Инфо", command=show_info, font=("Arial", 10)).grid(row=7, column=0, columnspan=4, sticky="nsew")
root.mainloop()