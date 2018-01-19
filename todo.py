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

class Console:
    def __init__(self, channel, stream):
        self._channel = channel
        self._fileCabinet = FileCabinet(stream)
        self._todolist = Notepad()

    def start(self):
        self._fileCabinet.take_out(self._todolist)
        self._channel.output("Here's your current todos.")

        for idx, todo in enumerate(self._todolist.todos()):
            self._channel.output("{0} {1}".format(idx + 1,todo))

        while True:
            self._channel.output("Do you have any more? (y/n)")
            input = self._channel.input()
            if input == 'n':
                break;
            elif input == 'y':
                self._todolist.write(self._channel.input())
            elif input == 'c':
                idx = int(self._channel.input())
                self._todolist.remove_indexed(idx - 1)

        self._fileCabinet.store(self._todolist)

if __name__ == "__main__":
    channel = IOChannel(input, print)
    try:
        stream = open("todo.txt", "r+")
        console = Console(channel, stream)
        console.start()
    finally:
        stream.close()
