from flask import Flask, render_template, request, redirect, url_for
import connection

app = Flask(__name__)


@app.route('/')
@app.route("/list")
def list_questions():
    question_list = connection.read_question_file()
    return render_template('list.html', question_list=question_list, header=connection.HEADER)


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )

# @app.route("/question/<question_id>")
# @app.route("/add-question")
# @app.route("/question/<question_id>/new-answer")
# @app.route("/question/<question_id>/delete")
# @app.route("/question/<question_id>/edit")
# @app.route("/question/<question_id>/vote_up")
# @app.route("/question/<question_id>/vote_down")
# # Sorting: /list?order_by=title&order_direction=desc
# @app.route("/answer/<answer_id>/delete")
# @app.route("/answer/<answer_id>/vote_up")
# @app.route("/answer/<answer_id>/vote_down")