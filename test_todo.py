import unittest
import todo
import io

class TestTodo(unittest.TestCase):
    def setUp(self):
        self.notepad = todo.Notepad()

    def test_with_a_blank_sheet(self):
        self.assertEqual(self.notepad.todos(), tuple())

    def test_write_todo(self):
        todoItem = "This is a todo item"
        self.notepad.write(todoItem)

        self.assertEqual(self.notepad.todos(), (todoItem,))

    def test_many_todos(self):
        todoItemOne = "One"
        todoItemTwo = "Two"
        self.notepad.write(todoItemOne)
        self.notepad.write(todoItemTwo)

        self.assertEqual(self.notepad.todos(), (todoItemOne, todoItemTwo))

    def test_remove_todo(self):
        todoItem = "This is a todo item"
        self.notepad.write(todoItem)
        self.notepad.remove(todoItem)

        self.assertEqual(self.notepad.todos(), tuple())

    def test_remove_todo_by_index(self):
        self.notepad.write("irrelevant")
        self.notepad.remove_indexed(0)

        self.assertEqual(self.notepad.todos(), tuple())

class TestFileCabinet(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

    def test_writing_an_empty_list_to_the_file_cabinet(self):
        cabinet = todo.FileCabinet(self.stream)
        todoList = todo.Notepad()

        cabinet.store(todoList)
        self.assertEqual(self.stream.getvalue(), '')

    def test_writing_a_list_with_one_entry_to_the_file_cabinet(self):
        cabinet = todo.FileCabinet(self.stream)
        todoList = todo.Notepad()
        todoList.write("Write a todo list app")

        cabinet.store(todoList)
        self.assertEqual(self.stream.getvalue(), 'Write a todo list app')

    def test_writing_many_entries_to_the_file_cabinet(self):
        cabinet = todo.FileCabinet(self.stream)
        todoList = todo.Notepad()
        todoList.write("Write a todo list app")
        todoList.write("Profit")

        cabinet.store(todoList)
        self.assertEqual(self.stream.getvalue(), 'Write a todo list app\nProfit')

    def test_load_an_existing_todo_from_stream(self):
        self.stream.write("todo 1\n")
        self.stream.write("todo 2")
        self.stream.seek(0)
        cabinet = todo.FileCabinet(self.stream)
        todoList = todo.Notepad()
        cabinet.take_out(todoList)

        self.assertEqual(todoList.todos(), ("todo 1", "todo 2"))

    def test_append_to_the_next_todos_on_store(self):
        self.stream.write("todo 1\n")
        self.stream.seek(0)
        cabinet = todo.FileCabinet(self.stream)
        todoList = todo.Notepad()
        cabinet.take_out(todoList)
        todoList.write("todo 2")
        cabinet.store(todoList)

        self.assertEqual(self.stream.getvalue(), "todo 1\ntodo 2")

class TestConsole(unittest.TestCase):

    class FakeChannel:
        def __init__(self, inputs):
            self._inputs = inputs

        def input(self):
            return self._inputs.pop(0)

        def output(self, text):
            pass

    def test_ends_when_input_is_exit(self):
        channel = TestConsole.FakeChannel([todo.Commands.EXIT])
        stream = io.StringIO()
        console = todo.Console(channel, stream)
        console.start()

        self.assertEqual(stream.getvalue(), "")

    def test_accepts_a_todo_after_a_y(self):
        channel = TestConsole.FakeChannel([
            todo.Commands.ADD,
            'schedule birthday',
            todo.Commands.EXIT])
        stream = io.StringIO()
        console = todo.Console(channel, stream)
        console.start()

        self.assertEqual(stream.getvalue(), "schedule birthday")

    def test_loads_the_initial_todos_from_the_stream(self):
        stream = io.StringIO()
        stream.write("First todo\n")
        stream.seek(0)
        channel = TestConsole.FakeChannel([
            todo.Commands.ADD,
            'Second Todo',
            todo.Commands.EXIT])
        console = todo.Console(channel, stream)
        console.start()

        self.assertEqual(stream.getvalue(), "First todo\nSecond Todo")

    def test_marks_a_todo_as_done_when_asked(self):
        stream = io.StringIO()
        stream.write("First todo\n")
        stream.seek(0)
        channel = TestConsole.FakeChannel([
            todo.Commands.COMPLETE,
            '1',
            todo.Commands.EXIT])
        console = todo.Console(channel, stream)
        console.start()

        self.assertEqual(stream.getvalue(), "")
