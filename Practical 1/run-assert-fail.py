import tkinter as tk
from types import SimpleNamespace
from todo_buggy import TodoApp

# БАГ(FUNC-2): delete повинен видаляти обране, а не останнє
root = tk.Tk(); root.withdraw()
app = TodoApp(root)
for t in ["A", "B", "C"]:
    app.entry.delete(0, "end"); app.entry.insert(0, t); app.add_task()
# вибираємо "A" (індекс 0)
app.listbox.selection_set(0)
app.delete_task()
# очікування: "A" видалили -> перший елемент тепер "B"
assert [x["text"] for x in app.tasks] == ["B", "C"], "delete має видаляти вибране, не останнє"
root.destroy()

# БАГ(FUNC-3): toggle_done має перемикати саме обране, без зсуву +1
root = tk.Tk(); root.withdraw()
app = TodoApp(root)
for t in ["X", "Y"]:
    app.entry.delete(0, "end"); app.entry.insert(0, t); app.add_task()

# подвійний клік по першому елементу -> очікуємо, що зробить done саме 0-й
evt = SimpleNamespace(widget=app.listbox, y=0)
app.toggle_done(evt)
assert app.tasks[0]["done"] is True and app.tasks[1]["done"] is False, "toggle_done має змінювати саме поточний індекс"
root.destroy()

print("Це повідомлення не має з’явитися, бо тести мають впасти")