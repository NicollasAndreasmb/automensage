import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from config import EXCEL_FILE
from storage import save_contacts
from main import main as send_messages

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação de mensagens 1.0")
        self.df = pd.DataFrame()

        # Frame de botões
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(fill='x', pady=5)
        tk.Button(frame_buttons, text="Abrir Planilha", command=self.open_excel).pack(side='left', padx=5)
        tk.Button(frame_buttons, text="Salvar Planilha", command=self.save_excel).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Enviar Mensagens", command=self.send_messages).pack(side="left", padx=5)

        # Frame da Treeview
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(fill='both', expand=True)
        self.tree = None

        # Log de mensagens
        self.log = tk.Text(root, height=10)
        self.log.pack(fill='x')

    def log_message(self, msg):
        self.log.insert(tk.END, f"{msg}\n")
        self.log.see(tk.END)
        self.root.update()

    def open_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.df = pd.read_excel(path)
            self.load_tree()
            self.log_message(f"Planilha {path} carregada!")

    def load_tree(self):
        # Limpa o frame
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill='both', expand=True)

        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"

        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.bind('<Double-1>', self.on_double_click)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1
        x, y, width, height = self.tree.bbox(item, column)

        value = self.tree.item(item, "values")[col_index]
        entry = tk.Entry(self.tree_frame)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event):
            new_val = entry.get()
            values = list(self.tree.item(item, "values"))
            values[col_index] = new_val
            self.tree.item(item, values=values)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def save_excel(self):
        rows = []
        for child in self.tree.get_children():
            rows.append(self.tree.item(child)['values'])
        self.df = pd.DataFrame(rows, columns=self.df.columns)
        save_contacts(self.df, EXCEL_FILE)
        self.log_message(f"Planilha salva em {EXCEL_FILE}")

    def send_messages(self):
        self.save_excel()
        self.log_message("Iniciando envio de mensagens...")
        try:
            send_messages()
            self.log_message("Envio concluído.")
        except Exception as e:
            self.log_message(f"Erro: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("1000x600")
    root.mainloop()
