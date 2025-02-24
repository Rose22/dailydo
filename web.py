import flask
import dailydo

app = flask.Flask(__name__)
todo = dailydo.TodoListDaily("todo")
todo.load()

@app.route("/")
def home():
    # load from file each time the page loads, to support cross device syncing and the like
    todo.load()

    return flask.render_template("home.html", todo=todo)

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if flask.request.method == "POST":
        if flask.request.form['new_item']:
            todo.add(flask.request.form['new_item'])
            todo.save()

    return flask.redirect(flask.url_for("home"))

@app.route("/edit")
def edit_list():
    return flask.render_template("home.html", edit=True, todo=todo)

@app.route("/delete/<index>")
def delete_item(index):
    index = int(index)-1
    todo.delete(index)
    todo.save()
    return flask.redirect(flask.url_for("edit_list"))

@app.route("/move/<index>/<direction>")
def move_item(index, direction):
    index = int(index)-1
    match direction:
        case "up":
            todo.move_up(index)
        case "down":
            todo.move_down(index)
    todo.save()

    return flask.redirect(flask.url_for("edit_list"))

@app.route("/check/<index>")
def check_item(index):
    index = int(index)-1
    todo.mark_done(index)
    todo.save()

    return flask.redirect(flask.url_for("home"))
@app.route("/uncheck/<index>")
def uncheck_item(index):
    index = int(index)-1
    todo.mark_todo(index)
    todo.save()

    return flask.redirect(flask.url_for("edit_list"))

@app.route("/movetotoday/<index>")
def move_to_today(index):
    index = int(index)-1
    todo.move_into_today(index)
    todo.save()

    return flask.redirect(flask.url_for("edit"))

app.run(debug=False)
