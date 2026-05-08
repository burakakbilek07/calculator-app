import tkinter as tk
import ast
import operator

history = []
dark_mode = False
all_buttons = []

FONT_MAIN = ("Segoe UI", 22)
FONT_BTN = ("Segoe UI", 12)
FONT_HISTORY = ("Segoe UI", 10)

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow
}

def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise Exception("Only numbers are allowed")

        elif isinstance(node, ast.BinOp):
            if type(node.op) not in operators:
                raise Exception("Invalid operation")
            return operators[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )

        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -eval_node(node.operand)
            else:
                raise Exception("Invalid operation")

        else:
            raise Exception("Invalid expression")

    tree = ast.parse(expr, mode='eval')
    return eval_node(tree)

def on_click(value):
    if value == "√":
        entry.insert(tk.END, "**0.5")
    else:
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

        expr = expr.replace(",", ".")
        expr = expr.replace("^", "**")
        expr = expr.replace("%", "/100")

        if len(expr) > 100:
            raise Exception("Expression too long")

        if expr.strip() == "":
            return

        result = safe_eval(expr)

        history.append(f"{expr} = {result}")
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        update_history()

    except ZeroDivisionError:
        entry.delete(0, tk.END)
        entry.insert(0, "Cannot divide by 0")

    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def update_history():
    history_box.delete(0, tk.END)
    for item in history[-10:]:
        history_box.insert(tk.END, item)

# Light tema
def set_light_theme():
    global dark_mode
    dark_mode = False
    
    bg = "#f0f0f0"
    root.config(bg=bg)
    entry.config(bg="white", fg="black", insertbackground="black")
    history_box.config(bg="white", fg="black")
    settings_frame.config(bg=bg)
    buttons_frame.config(bg=bg)

    for widget in settings_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg="SystemButtonFace", fg="black")
        elif isinstance(widget, tk.Label):
            widget.config(bg=bg, fg="black")
    
    for canvas, circle, color in all_buttons:
        canvas.config(bg=bg, highlightbackground=bg, highlightcolor=bg)
        canvas.itemconfig(circle, fill=color)

def set_dark_theme():
    global dark_mode
    dark_mode = True

    bg = "#1e1e1e"

    root.config(bg=bg)
    entry.config(bg=bg, fg="white", insertbackground="white")
    history_box.config(bg=bg, fg="white")
    settings_frame.config(bg=bg)
    buttons_frame.config(bg=bg)

    for widget in settings_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg="#2d2d2d", fg="white")
        elif isinstance(widget, tk.Label):
            widget.config(bg=bg, fg="white")

    for canvas, circle, color in all_buttons:
        canvas.config(bg=bg, highlightbackground=bg, highlightcolor=bg)
        canvas.itemconfig(circle, fill=color)

def toggle_settings():
    if settings_frame.winfo_viewable():
        settings_frame.grid_remove()
    else:
        settings_frame.grid(row=2, column=0, columnspan=4, sticky="we")

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

root = tk.Tk()
root.title("CalcPro")
root.geometry("350x550")
root.config(bg="#f0f0f0")

buttons_frame = tk.Frame(root, bg=root.cget("bg"))
buttons_frame.grid(row=4, column=0, columnspan=4)

try:
    root.iconbitmap("ikon.ico")
except:
    pass

entry = tk.Entry(root, font=FONT_MAIN, justify="right", bd=0)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15, sticky="we")

root.bind("<Return>", calculate)
root.bind("<Escape>", clear_all)
root.bind("<BackSpace>", backspace)

def create_round_button(text, command, r, c):
    canvas = tk.Canvas(
        buttons_frame,
        width=70,
        height=70,
        bd=0,
        highlightthickness=0,
        bg="SystemButtonFace"
    )

    canvas.grid(row=r, column=c, padx=8, pady=8)

    if text in ["+", "-", "*", "/", "="]:
        color = "#ff9f0a"

    elif text in ["C", "⌫", "⚙", "%"]:
        color = "#a5a5a5"

    else:
        color = "#333333"

    circle = canvas.create_oval(5, 5, 65, 65, fill=color, outline="")
    canvas.create_text(35, 35, text=text, fill="white", font=("Segoe UI", 16, "bold"))

    def click_effect():
        canvas.scale("all", 35, 35, 0.92, 0.92)
        canvas.after(50, lambda: canvas.scale("all", 35, 35, 1.08, 1.08))
        canvas.after(100, lambda: canvas.scale("all", 35, 35, 1.0, 1.0))

    canvas.bind("<Button-1>", lambda e: [click_effect(), command()])

    is_scaled = False

    def on_enter(e):
        nonlocal is_scaled
        if not is_scaled:
            canvas.scale("all", 35, 35, 1.05, 1.05)
            is_scaled = True

    def on_leave(e):
        nonlocal is_scaled
        if is_scaled:
            canvas.scale("all", 35, 35, 1/1.05, 1/1.05)
            is_scaled = False

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    all_buttons.append((canvas, circle, color))

create_round_button("⚙", toggle_settings, 1, 0)
create_round_button("⌫", backspace, 1, 1)
create_round_button("C", clear_all, 1, 2)
create_round_button("=", calculate, 1, 3)

settings_frame = tk.Frame(root, bg="#f0f0f0")

tk.Button(settings_frame, text="White Theme",
          font=FONT_BTN, command=set_light_theme).pack(fill="x", padx=10, pady=2)

tk.Button(settings_frame, text="Dark Theme",
          font=FONT_BTN, command=set_dark_theme).pack(fill="x", padx=10, pady=2)

tk.Label(settings_frame, text="Creator: Burak Akbilek",
         font=("Segoe UI", 9), bg="#f0f0f0").pack(pady=5)

settings_frame.grid(row=2, column=0, columnspan=4, sticky="we")

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "√", "0", "%", "+"
]

row = 2
col = 0

for b in buttons:
    create_round_button(b, lambda x=b: on_click(x), row, col)
    col += 1
    if col > 3:
        col = 0
        row += 1

history_box = tk.Listbox(root, height=8,
                         font=FONT_HISTORY, bd=0)
history_box.grid(row=8, column=0, columnspan=4,
                 sticky="we", padx=10, pady=10)

root.mainloop()
