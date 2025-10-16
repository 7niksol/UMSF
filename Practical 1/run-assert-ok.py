import tkinter as tk
from todo_buggy import TodoApp

# Тест 1: додавання валідного завдання
root = tk.Tk(); root.withdraw()
app = TodoApp(root)
app.entry.delete(0, "end")
app.entry.insert(0, "купити каву")
app.add_task()
assert len(app.tasks) == 1 and app.tasks[0]["text"] == "купити каву" and app.tasks[0]["done"] is False, "має додати 1 таску"
root.destroy()

# Тест 2: ігнор порожнього/плейсхолдерного вводу
root = tk.Tk(); root.withdraw()
app = TodoApp(root)
before = len(app.tasks)
app.entry.delete(0, "end")
app.add_task()  # порожньо -> має ігноритись
assert len(app.tasks) == before, "порожній ввід не має створювати таску"
root.destroy()

print("OK: усі позитивні assert-тести пройшли")