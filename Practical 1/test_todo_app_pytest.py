import pytest
import tkinter as tk
from todo_buggy import TodoApp

# ---------- Фікстура ----------
@pytest.fixture
def app():
    """Створює свіжий Tk та екземпляр застосунку для кожного тесту."""
    root = tk.Tk()
    root.withdraw()
    app = TodoApp(root)
    yield app
    root.destroy()

# ---------- Позитивні тести (конверсія з assert-прикладів) ----------
def test_add_valid_task(app):
    app.entry.delete(0, "end")
    app.entry.insert(0, "купити каву")
    app.add_task()
    assert len(app.tasks) == 1
    assert app.tasks[0]["text"] == "купити каву"
    assert app.tasks[0]["done"] is False

@pytest.mark.parametrize("raw, expected", [
    ("прочитати книгу", "прочитати книгу"),
    ("  прибрати  ", "прибрати"),
])
def test_add_valid_task_parametrized(app, raw, expected):
    app.entry.delete(0, "end")
    app.entry.insert(0, raw)
    app.add_task()
    assert len(app.tasks) == 1
    assert app.tasks[0]["text"] == expected
    assert app.tasks[0]["done"] is False

@pytest.mark.parametrize("raw", ["", "   ", "введіть тут нове завдання"])
def test_ignore_empty_or_placeholder_input(app, raw):
    before = len(app.tasks)
    app.entry.delete(0, "end")
    app.entry.insert(0, raw)
    app.add_task()
    assert len(app.tasks) == before

# ---------- Тест, що очікує помилку (raises) ----------
def test_toggle_done_requires_event_object(app):
    # Через помилковий виклик без event очікуємо AttributeError
    with pytest.raises(AttributeError):
        app.toggle_done()  # event=None за замовчуванням

# ---------- Пропуск тесту (skip) ----------
@pytest.mark.skip(reason="Потребує ручної взаємодії зі SimpleDialog (UI), пропускаємо в автозапуску")
def test_edit_task_interactive_dialog(app):
    # Функція показує діалогове вікно введення, що непридатне для CI без monkeypatch.
    app.tasks = [{"text": "A", "done": False}]
    app.refresh_listbox()
    app.listbox.select_set(0)
    app.edit_task()
    # (перевірка мала б порівнювати зміну тексту після ручного введення)
    assert True

# ---------- Очікувано несправний тест (xfail) ----------
@pytest.mark.xfail(reason="Відомий дефект: delete_task видаляє останній елемент замість вибраного")
def test_delete_selected_item_is_removed(app):
    app.tasks = [{"text": "A", "done": False},
                 {"text": "B", "done": False},
                 {"text": "C", "done": False}]
    app.refresh_listbox()
    app.listbox.select_set(0)  # очікуємо, що видалить 'A'
    app.delete_task()
    # Очікувана коректна поведінка:
    assert [t["text"] for t in app.tasks] == ["B", "C"]

# ---------- Навмисно помилковий тест для демонстрації звіту pytest ----------
def test_demo_failing():
    # Навмисно хибне твердження, щоб у звіті був приклад помилки (F)
    assert 1 == 2
