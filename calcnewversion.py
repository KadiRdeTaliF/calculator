import tkinter as tk
from decimal import Decimal

BG, DIM = "#1e1f26", "#9a9ca5"
OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
       "×": lambda a, b: a * b, "÷": lambda a, b: a / b}
ROWS = ["% √ x² 1/x", "CE C ← ÷", "7 8 9 ×", "4 5 6 -", "1 2 3 +", "± 0 , ="]
KEYMAP = {"*": "×", "/": "÷", ".": ",", "\r": "=", "\x08": "←", "\x7f": "←", "\x1b": "C"}

def fmt(d):  # Decimal -> строка с запятой, без лишних нулей
    if abs(d) < Decimal("1e15"):
        d = round(d, 10)
    return "0" if d == 0 else format(d.normalize(), "f").replace(".", ",")

class Calc:
    def __init__(self, root):
        self.root = root
        root.title("Калькулятор")
        root.configure(bg=BG); root.resizable(False, False)
        # reset: следующая цифра начинает новое число; wait: ждём второй операнд
        self.cur, self.first, self.op, self.last, self.reset, self.wait = "0", None, None, None, True, False
        self.hist, self.var = tk.StringVar(), tk.StringVar(value="0")
        for r, (v, f, fg, pad) in enumerate([(self.hist, 11, DIM, (10, 0)), (self.var, 30, "white", (0, 10))]):
            tk.Label(root, textvariable=v, font=("Arial", f), bg=BG, fg=fg, anchor="e").grid(
                row=r, column=0, columnspan=4, sticky="ew", padx=10, pady=pad)
        for r, line in enumerate(ROWS, start=2):
            for c, k in enumerate(line.split()):
                color = "#ff9f0a" if k in OPS or k == "=" else "#33353f" if k.isdigit() or k == "," else "#4a4d59"
                tk.Button(root, text=k, font=("Arial", 16), width=4, bg=color, fg="white", activebackground=DIM,
                          bd=0, relief="flat", command=lambda t=k: self.press(t)).grid(
                    row=r, column=c, sticky="nsew", padx=2, pady=2)
        tk.Button(root, text="Инфо", bg=BG, fg=DIM, bd=0, command=self.info).grid(row=8, column=0, columnspan=4, pady=4)
        root.bind("<Key>", lambda e: self.press(KEYMAP.get(e.char, e.char)))

    def num(self):
        return Decimal(self.cur.replace(",", "."))
    def show(self, s):
        self.cur = s; self.var.set(s)

    def equals(self):
        if self.op:  # обычное вычисление
            a, op, b = self.first, self.op, self.num()
            self.last = (op, b)
        elif self.last:  # повторное «=» применяет последнюю операцию ещё раз
            a, (op, b) = self.num(), self.last
        else:
            return
        self.hist.set(f"{fmt(a)} {op} {fmt(b)} =")
        try: self.show(fmt(OPS[op](a, b)))
        except (ArithmeticError, ValueError): self.show("Error")
        self.op, self.reset, self.wait = None, True, False

    def operator(self, k):
        if self.op and not self.wait:  # цепочка: 2 + 3 + ... сначала считаем 2 + 3
            self.equals()
            if self.cur == "Error":
                return
        self.first, self.op, self.last = self.num(), k, None
        self.reset = self.wait = True
        self.hist.set(f"{fmt(self.first)} {k}")

    def unary(self, k):
        try:
            x = self.num()
            if k == "%":  # как в Windows: 5 + 10 % -> 5 + 0,5
                r = self.first * x / 100 if self.op in ("+", "-") else x / 100
            else:
                r = {"√": x.sqrt, "x²": lambda: x * x, "1/x": lambda: 1 / x}[k]()
            self.show(fmt(r))
        except (ArithmeticError, ValueError):
            self.show("Error")
        self.reset, self.wait = True, False

    def press(self, k):
        if self.cur == "Error" and k not in ("C", "CE"):
            return
        if k.isdigit() and len(k) == 1 or k == ",":
            if self.reset:
                self.cur, self.reset, self.wait = ("0" if k == "," else ""), False, False
            if (k == "," and "," in self.cur) or len(self.cur) >= 16:
                return
            self.show(("" if self.cur == "0" and k != "," else self.cur) + k)
        elif k in OPS: self.operator(k)
        elif k == "=": self.equals()
        elif k in ("√", "x²", "1/x", "%"): self.unary(k)
        elif k == "C": self.op, self.first, self.last, self.reset = None, None, None, True; self.hist.set(""); self.show("0")
        elif k == "CE": self.reset = True; self.show("0")
        elif k == "←" and not self.reset: self.show(self.cur[:-1] if len(self.cur) > 1 and self.cur[:-1] != "-" else "0")
        elif k == "±" and self.num() != 0: self.show(self.cur[1:] if self.cur[0] == "-" else "-" + self.cur)

    def info(self):
        top = tk.Toplevel(self.root)
        top.title("О программе"); top.grab_set()
        tk.Label(top, text="Разработчик: Иванов И.И.\n\nСпасибо моим родителям\nза поддержку и терпение!", padx=30, pady=20).pack()
        tk.Button(top, text="ОК", command=top.destroy).pack(pady=(0, 15))

root = tk.Tk()
app = Calc(root)
root.mainloop()
