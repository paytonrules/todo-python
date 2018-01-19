from enum import Enum

class FileCabinet:
    def __init__(self, stream):
        self._stream = stream

    def store(self, notepad):
        self._stream.seek(0)
        self._stream.truncate()
        self._stream.writelines('\n'.join(notepad.todos()))

    def take_out(self, notepad):
        for line in self._stream.readlines():
            notepad.write(line.strip())

class Notepad:
    def __init__(self):
        self._todos = []

    def todos(self):
        return tuple(self._todos)

    def write(self, todo):
        self._todos.append(todo)

    def remove(self, todo):
        self._todos.remove(todo)

    def remove_indexed(self, idx):
        self._todos.pop(idx)

class IOChannel:
    def __init__(self, i, o):
        self._input = i
        self._output = o

    def input(self):
        return self._input()

    def output(self, text):
        self._output(text)

class Commands:
    EXIT = 'e'
    ADD = 'a'
    COMPLETE = 'c'

class Console:
    def __init__(self, channel, stream):
        self._channel = channel
        self._fileCabinet = FileCabinet(stream)
        self._todolist = Notepad()

    def start(self):
        self._fileCabinet.take_out(self._todolist)

        moreCommands = True
        while moreCommands:
            self._print_todos()
            self._request_next_command()
            moreCommands = self._process_command(self._channel.input())

        self._fileCabinet.store(self._todolist)

    def _print_todos(self):
        self._channel.output("Here's your current todos.")

        for idx, todo in enumerate(self._todolist.todos()):
            self._channel.output("{0} {1}".format(idx + 1,todo))

    def _request_next_command(self):
            self._channel.output("Would you like to:")
            self._channel.output("{0} - Add Todo".format(Commands.ADD))
            self._channel.output("{0} - Complete A Todo".format(Commands.COMPLETE))
            self._channel.output("{0} - Exit".format(Commands.EXIT))
            self._channel.output("Enter {0}/{1}/{2}".format(Commands.ADD, Commands.COMPLETE, Commands.EXIT))

    def _process_command(self, input):
        if input == Commands.EXIT:
            return False;
        elif input == Commands.ADD:
            self._channel.output("Please enter yet another thing to do.")
            self._todolist.write(self._channel.input())
        elif input == Commands.COMPLETE:
            self._channel.output("Hooray! Which todo did you complete!")
            idx = int(self._channel.input())
            self._todolist.remove_indexed(idx - 1)

        return True

if __name__ == "__main__":
    channel = IOChannel(input, print)
    try:
        stream = open("todo.txt", "r+")
        console = Console(channel, stream)
        console.start()
    finally:
        stream.close()
