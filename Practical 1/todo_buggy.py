
import tkinter as tk
from tkinter import messagebox, filedialog

"""
To-Do List (intentionally buggy) — Практична робота №1

УВАГА: У застосунку навмисно присутні 2–3 помилки UI/UX та 3 функціональні помилки.
Шукайте коментарі "BUG:" нижче — вони пояснюють, у чому проблема.
"""

"""
Тестова зміна для перевірки git
"""

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Завдання - todo")  # BUG(UI/UX-2): Неконсистентність назв: у заголовку "Завдання - todo", на кнопках інша термінологія/регістр.
        self.tasks = []

        # Головний фрейм
        self.frame = tk.Frame(root)
        self.frame.pack(padx=12, pady=12, fill="both", expand=True)

        # Ввід нового завдання
        self.entry = tk.Entry(self.frame, width=40, fg="#dddddd")  # BUG(UI/UX-1): Дуже низька контрастність тексту (сірий на світлому).
        self.entry.insert(0, "введіть тут нове завдання")
        self.entry.pack(anchor="w")

        # Список завдань + (навмисно) захований скролбар
        self.listbox = tk.Listbox(self.frame, height=10, activestyle="none")
        self.listbox.pack(fill="both", expand=True, pady=(8, 8))
        # BUG(UI/UX-3): Скролбар не додано взагалі -> при великій кількості елементів користувач не бачить, що список прокручується.

        # Панель кнопок (спеціально у незвичному порядку)
        btns = tk.Frame(self.frame)
        btns.pack(fill="x")

        self.btn_delete = tk.Button(btns, text="delete", command=self.delete_task)  # BUG(UI/UX-2): неконсистентний регістр/мова.
        self.btn_delete.pack(side="left", padx=4)

        self.btn_add = tk.Button(btns, text="Add Task", command=self.add_task)
        self.btn_add.pack(side="left", padx=4)

        self.btn_edit = tk.Button(btns, text="Редагувати", command=self.edit_task)
        self.btn_edit.pack(side="left", padx=4)

        self.btn_save = tk.Button(btns, text="Save to File", command=self.save_to_file)
        self.btn_save.pack(side="left", padx=4)

        self.btn_load = tk.Button(btns, text="Load from File", command=self.load_from_file)
        self.btn_load.pack(side="left", padx=4)

        # Підказка
        self.hint = tk.Label(self.frame, text="Порада: двічі клацніть для відмітки виконання (псевдо).")
        self.hint.pack(anchor="w", pady=(6, 0))

        # Подія подвійного кліку для позначки "виконано"
        self.listbox.bind("<Double-1>", self.toggle_done)  # BUG(FUNC-3): Позначка "виконано" працює некоректно для вибраного індексу.

    def add_task(self):
        text = self.entry.get().strip()
        if not text or text == "введіть тут нове завдання":
            # Ніякого повідомлення про помилку — тихо ігноруємо.
            # BUG(UI/UX-4, необов'язковий): Відсутній чіткий зворотний зв'язок про помилкове введення.
            return
        self.tasks.append({"text": text, "done": False})
        self.refresh_listbox()
        self.entry.delete(0, "end")

    def edit_task(self):
        # BUG(FUNC-1): Редагування змінює ЛИШЕ текст у listbox, але не у self.tasks -> після оновлення список "втратить" правку.
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        current = self.listbox.get(idx)
        new = tk.simpledialog.askstring("Редагувати", "Новий текст:", initialvalue=current)
        if new is not None and new.strip():
            # Змінюємо лише відображення, не дані:
            self.listbox.delete(idx)
            self.listbox.insert(idx, new.strip() + (" [✓]" if current.endswith("[✓]") else ""))

    def delete_task(self):
        # BUG(FUNC-2): Видаляє ОСТАННІЙ елемент, а не вибраний (off-by-selection).
        if not self.tasks:
            return
        sel = self.listbox.curselection()
        if not sel:
            # Якщо нічого не вибрано — все одно видалимо останній!
            self.tasks.pop()
        else:
            # І навіть якщо вибрано — теж видалимо останній :) навмисно неправильно
            self.tasks.pop()
        self.refresh_listbox()

    def toggle_done(self, event=None):
        # BUG(FUNC-3): Неправильний індекс через event.widget.nearest та зсув; інколи перемикає не той елемент.
        idx = event.widget.nearest(event.y) + 1  # зайвий +1
        if 0 <= idx < len(self.tasks):
            self.tasks[idx]["done"] = not self.tasks[idx]["done"]
            self.refresh_listbox()

    def save_to_file(self):
        # BUG(FUNC-4 EXTRA, необов'язковий): Обрізає останній елемент при збереженні через зсув у зрізі.
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                # навмисно пропускаємо останній елемент
                for item in self.tasks[:-1]:
                    line = f"{item['text']}||{int(item['done'])}\n"
                    f.write(line)
            messagebox.showinfo("Збережено", f"Завдання збережено до {path}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path:
            return
        try:
            items = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if "||" in line:
                        text, done = line.rstrip("\n").split("||", 1)
                        items.append({"text": text, "done": bool(int(done))})
            self.tasks = items
            self.refresh_listbox()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def refresh_listbox(self):
        self.listbox.delete(0, "end")
        for item in self.tasks:
            label = item["text"] + (" [✓]" if item["done"] else "")
            self.listbox.insert("end", label)

if __name__ == "__main__":
    root = tk.Tk()
    # Ненадійні мінімальні розміри — дрібні, можуть спричиняти обрізання контенту на деяких системах.
    root.minsize(260, 280)
    app = TodoApp(root)
    root.mainloop()
