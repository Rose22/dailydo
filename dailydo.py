import os
import datetime

class TodoList:
    """simple todo list that has two internal lists: todo, and done. self explanatory"""
    def __init__(self):
        self._todo = []
        self._done = []

    def load(self, todo, done):
        self._todo = todo
        self._done = done

    def get_todo(self):
        return self._todo
    def get_done(self):
        return self._done

    def add(self, item):
        return self._todo.append(item)

    def move_up(self, index):
        """moves an item up the list"""
        if index > 0:
            self._todo[index-1], self._todo[index] = self._todo[index], self._todo[index-1]
    def move_down(self, index):
        """moves an item down the list"""
        if index < len(self._todo)-1:
            self._todo[index+1], self._todo[index] = self._todo[index], self._todo[index+1]

    def mark_done(self, index):
        """marking an item as done puts it in a seperate list where it's protected from modifications. you can always move it back into the todo list."""
        item = self._todo.pop(index)
        return self._done.append(item)
    def mark_todo(self, index):
        item = self._done.pop(index)
        return self._todo.insert(0, item)

    def delete(self, index):
        return self._todo.pop(index)

    def clear(self):
        self._todo = []
        self._done = []

class TodoListStorage:
    """handles storage of the todo list into a file"""
    def __init__(self, filepath):
        self._filepath = filepath

    def load(self):
        if not os.path.exists(self._filepath):
            return False

        with open(self._filepath, 'r') as f:
            file_split = f.read().split("---\n")
            if len(file_split) <= 1:
                return self.clear()

            todo = file_split[0].strip().split("\n")
            done = file_split[1].strip().split("\n")
            return (todo, done)

    def save(self, todo, done):
        with open(self._filepath, 'w') as f:
            # if both lists are blank, just write a blank file
            if not todo and not done:
                f.write('')
                return

            for item in todo:
                f.write(f"{item}\n")

            f.write("---\n")

            for item in done:
                f.write(f"{item}\n")

class TodoListDaily(TodoList):
    """a todo list that clears itself every day"""

    def __init__(self, filepath):
        super().__init__()
        self._storage = TodoListStorage(filepath)
        # store the day the class was initialized. will be updated later by self._tick()
        self._day = datetime.date.today()
        # roll over tasks from the day onto a yesterday list. we only keep 1 day of history, just in case
        self._todo_yesterday = []

    def _tick(self):
        """check if a day has passed. if so, update the internally stored day to the current day, and clear the list"""

        currentday = datetime.date.today()
        if currentday > self._day:
            # keep a copy of yesterday's list of tasks that weren't marked done
            self._todo_yesterday = super().get_todo()

            self._day = currentday
            self.clear()

    def get_todo(self):
        self._tick()
        return super().get_todo()
    def get_done(self):
        self._tick()
        return super().get_done()
    def get_yesterday(self):
        self._tick()
        return self._todo_yesterday
    def move_to_today(self, index):
        self._tick()
        return self.add(self._todo_yesterday.pop(index))

    def load(self):
        todo, done = self._storage.load()
        return super().load(todo, done)
    def save(self):
        return self._storage.save(self.get_todo(), self.get_done())

