# test_todo_app.py
import io
import os
import tempfile
import unittest
from unittest.mock import patch
import tkinter as tk
from types import SimpleNamespace

from todo_buggy import TodoApp  

class TkAppCase(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = TodoApp(self.root)

    def tearDown(self):
        self.root.destroy()

    # --- Happy path ---
    def test_add_task_happy(self):
        self.app.entry.delete(0, "end")
        self.app.entry.insert(0, "прочитати книжку")
        self.app.add_task()
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0]["text"], "прочитати книжку")
        self.assertFalse(self.app.tasks[0]["done"])

    def test_ignore_placeholder_on_add(self):
        # плейсхолдер/порожній не має додавати
        before = len(self.app.tasks)
        self.app.entry.delete(0, "end")
        self.app.add_task()
        self.assertEqual(len(self.app.tasks), before)

    def test_load_from_file(self):
        # робимо тимчасовий файл з 2 рядками
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as f:
            f.write("task1||0\n")
            f.write("task2||1\n")
            path = f.name
        try:
            with patch("tkinter.filedialog.askopenfilename", return_value=path):
                self.app.load_from_file()
            self.assertEqual(len(self.app.tasks), 2)
            self.assertEqual(self.app.tasks[0]["text"], "task1")
            self.assertFalse(self.app.tasks[0]["done"])
            self.assertTrue(self.app.tasks[1]["done"])
        finally:
            os.remove(path)

    # --- Тести, що фіксують відомі баги (сьогодні впадуть) ---
    def test_delete_should_remove_selected_not_last(self):
        # підготуємо 3 таски
        for t in ["A", "B", "C"]:
            self.app.entry.delete(0, "end"); self.app.entry.insert(0, t); self.app.add_task()
        # вибираємо перший і тиснемо delete
        self.app.listbox.selection_clear(0, "end")
        self.app.listbox.selection_set(0)
        self.app.delete_task()

        # очікувана поведінка: видаляється "A"
        # фактична (з багом): видалиться "C" -> цей тест має звалитись
        self.assertListEqual([x["text"] for x in self.app.tasks], ["B", "C"])

    def test_toggle_done_should_flip_exact_index(self):
        for t in ["X", "Y"]:
            self.app.entry.delete(0, "end"); self.app.entry.insert(0, t); self.app.add_task()
        evt = SimpleNamespace(widget=self.app.listbox, y=0)
        self.app.toggle_done(evt)
        # очікуємо зміни для індексу 0, а не 1
        self.assertTrue(self.app.tasks[0]["done"])
        self.assertFalse(self.app.tasks[1]["done"])

    def test_edit_should_update_model_not_only_listbox(self):
        # підготуємо 1 таску
        self.app.entry.delete(0, "end"); self.app.entry.insert(0, "old"); self.app.add_task()
        # вибрати 0 і відредагувати
        self.app.listbox.selection_set(0)
        with patch("tkinter.simpledialog.askstring", return_value="new"):
            self.app.edit_task()

        # очікування: self.tasks[0]["text"] == "new"
        # фактично (з багом) модель не змінюється -> тест впаде
        self.assertEqual(self.app.tasks[0]["text"], "new")

    # --- Збереження у файл: сьогодні некоректно скипає останній елемент ---
    def test_save_to_file_should_write_all_items(self):
        for t in ["t1", "t2", "t3"]:
            self.app.entry.delete(0, "end"); self.app.entry.insert(0, t); self.app.add_task()
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as f:
            path = f.name
        try:
            with patch("tkinter.filedialog.asksaveasfilename", return_value=path), \
                 patch("tkinter.messagebox.showinfo"):
                self.app.save_to_file()
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.rstrip("\n") for line in f]
            # очікуємо 3 рядки, але з багом буде 2 -> тест впаде
            self.assertEqual(len(lines), 3)
            self.assertIn("t3||0", lines)  # перевіримо, що останній не загубився
        finally:
            os.remove(path)

if __name__ == "__main__":
    unittest.main(verbosity=2)