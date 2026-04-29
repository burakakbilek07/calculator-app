import tkinter as tk
import ast
import operator

# ----------------- GLOBAL -----------------
history = []
dark_mode = False

FONT_MAIN = ("Segoe UI", 22)
FONT_BTN = ("Segoe UI", 12)
FONT_HISTORY = ("Segoe UI", 10)

# ----------------- OPERATÖRLER -----------------
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}

# ----------------- GÜVENLİ HESAPLAMA -----------------
def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)

        elif isinstance(node, ast.Constant):  # Python 3.10+
            return node.value

        elif isinstance(node, ast.BinOp):
            if type(node.op) not in operators:
                raise Exception("Geçersiz işlem")
            return operators[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )

        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -eval_node(node.operand)
            else:
                raise Exception("Geçersiz işlem")

        else:
            raise Exception("Geçersiz ifade")

    tree = ast.parse(expr, mode='eval')
    return eval_node(tree)

# ----------------- FONKSİYONLAR -----------------
def on_click(value):
    entry.insert(tk.END, str(value))

def clear_all(event=None):
    entry.delete(0, tk.END)

def backspace(event=None):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current[:-1])

def calculate(event=None):
    try:
        expr = entry.get()

        if expr.strip() == "":
            return

        result = safe_eval(expr)

        history.append(f"{expr} = {result}")
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        update_history()

    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Hata")

def update_history():
    history_box.delete(0, tk.END)
    for item in history[-10:]:
        history_box.insert(tk.END, item)

# ----------------- TEMA -----------------
def set_light_theme():
    global dark_mode
    dark_mode = False

    root.config(bg="#f0f0f0")
    entry.config(bg="white", fg="black", insertbackground="black")
    history_box.config(bg="white", fg="black")

    for btn in all_buttons:
        btn.config(bg="#ffffff", fg="black")

def set_dark_theme():
    global dark_mode
    dark_mode = True

    root.config(bg="#1e1e1e")
    entry.config(bg="#1e1e1e", fg="white", insertbackground="white")
    history_box.config(bg="#1e1e1e", fg="white")

    for btn in all_buttons:
        btn.config(bg="#2d2d2d", fg="white")

def toggle_settings():
    if settings_frame.winfo_viewable():
        settings_frame.grid_remove()
    else:
        settings_frame.grid()

# ----------------- HOVER -----------------
def on_enter(e):
    if dark_mode:
        e.widget.config(bg="#444")
    else:
        e.widget.config(bg="#dcdcdc")

def on_leave(e):
    if dark_mode:
        e.widget.config(bg="#2d2d2d")
    else:
        e.widget.config(bg="#ffffff")

# ----------------- PENCERE -----------------
root = tk.Tk()
root.title("CalcPro")
root.geometry("350x550")
root.config(bg="#f0f0f0")

# İKON (aynı klasörde ikon.ico olmalı)
try:
    root.iconbitmap("ikon.ico")
except:
    pass

# ----------------- EKRAN -----------------
entry = tk.Entry(root, font=FONT_MAIN, justify="right", bd=0)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15, sticky="we")

# ----------------- KLAVYE -----------------
root.bind("<Return>", calculate)
root.bind("<Escape>", clear_all)
root.bind("<BackSpace>", backspace)

# ----------------- BUTON -----------------
all_buttons = []

def create_button(text, command, r, c):
    btn = tk.Button(root, text=text, width=8, height=2,
                    font=FONT_BTN, bd=0, relief="flat",
                    command=command)

    btn.grid(row=r, column=c, padx=5, pady=5)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    all_buttons.append(btn)

# ----------------- ÜST -----------------
create_button("⚙", toggle_settings, 1, 0)
create_button("⌫", backspace, 1, 1)
create_button("C", clear_all, 1, 2)
create_button("=", calculate, 1, 3)

# ----------------- SETTINGS -----------------
settings_frame = tk.Frame(root, bg="#f0f0f0")

tk.Button(settings_frame, text="White Theme",
          font=FONT_BTN, command=set_light_theme).pack(fill="x", padx=10, pady=2)

tk.Button(settings_frame, text="Dark Theme",
          font=FONT_BTN, command=set_dark_theme).pack(fill="x", padx=10, pady=2)

tk.Label(settings_frame, text="Creator: Burak Akbilek",
         font=("Segoe UI", 9), bg="#f0f0f0").pack(pady=5)

settings_frame.grid(row=2, column=0, columnspan=4, sticky="we")
settings_frame.grid_remove()

# ----------------- TUŞLAR -----------------
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "(", "0", ")", "+"
]

row = 3
col = 0

for b in buttons:
    create_button(b, lambda x=b: on_click(x), row, col)
    col += 1
    if col > 3:
        col = 0
        row += 1

# ----------------- GEÇMİŞ -----------------
history_box = tk.Listbox(root, height=8,
                         font=FONT_HISTORY, bd=0)
history_box.grid(row=8, column=0, columnspan=4,
                 sticky="we", padx=10, pady=10)

# ----------------- BAŞLAT -----------------
root.mainloop()
