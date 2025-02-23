import os
import flask
import datetime

app = flask.Flask(__name__)

class DayClock():
    def __init__(self):
        # store today's date internally. this will be updated each day to check if a day has passed
        self._day = datetime.date.today()

    def tick(self):
        """check if a day has passed. if so, update the internally stored day to the current day"""

        currentday = datetime.date.today()
        print(f"stored day: {self._day}, currentday: {currentday}")
        if currentday > self._day:
            self._day = currentday
            return True

        return False

class TodoList():
    """has 2 lists: todo and done. contains methods to manage both lists as a group and save them into a file"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.todo = []
        self.done = []

    def add(self, item):
        self.todo.append(item)

        return self.save()
    def move(self, index, direction):
        match direction:
            case "up":
                if index > 0:
                    self.todo[index-1], self.todo[index] = self.todo[index], self.todo[index-1]
            case "down":
                if index < len(self.todo)-1:
                    self.todo[index+1], self.todo[index] = self.todo[index], self.todo[index+1]

        return self.save()
    def markdone(self, index):
        item = self.todo.pop(index)
        self.done.append(item)

        return self.save()
    def marktodo(self, index):
        item = self.done.pop(index)
        self.todo.insert(0, item)

        return self.save()
    def delete(self, index):
        self.done.pop(index)
        return self.save()

    def load(self):
        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, 'r') as f:
            file_content = f.read()
            if not file_content:
                return

            todo, done = file_content.split("---\n")
            self.todo = todo.strip().split("\n")
            self.done = done.strip().split("\n")
    def save(self):
        with open(self.filepath, 'w') as f:
            for item in self.todo:
                f.write(f"{item}\n")

            f.write("---\n")

            for item in self.done:
                f.write(f"{item}\n")

        return self
    def clear(self):
        self.todo = []
        self.done = []
        with open(self.filepath, 'w') as f:
            f.write('')

        return

todo = TodoList("todo")
todo.load()

dayclock = DayClock()

@app.route("/")
def home():
    if dayclock.tick():
        todo.clear()

    return flask.render_template("home.html", todo=todo)

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if flask.request.method == "POST":
        if flask.request.form['new_item']:
            todo.add(flask.request.form['new_item'])

    return flask.redirect(flask.url_for("home"))

@app.route("/delete/<index>")
def delete_item(index):
    index = int(index)-1
    todo.delete(index)
    return flask.redirect(flask.url_for("home"))

@app.route("/move/<index>/<direction>")
def move_item(index, direction):
    index = int(index)-1
    todo.move(index, direction)

    return flask.redirect(flask.url_for("home"))

@app.route("/check/<index>")
def check_item(index):
    index = int(index)-1
    todo.markdone(index)

    return flask.redirect(flask.url_for("home"))
@app.route("/uncheck/<index>")
def uncheck_item(index):
    index = int(index)-1
    todo.marktodo(index)

    return flask.redirect(flask.url_for("home"))

app.run(debug=False)
