from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route("/list", methods=['GET', 'POST'])
def list_questions():
    orber_by = id
    order_direction = 'down'
    question_list = data_manager.get_question_list()
    return render_template('list.html', question_list=question_list, header=connection.QUESTION_HEADER)


@app.route("/question/<int:id>", methods=['GET', 'POST'])
def display_question(id):
    question = data_manager.get_question_by_id(id)
    header = ["title", "message"]
    result = data_manager.filter_question(question, header)
    answer = data_manager.get_answers_by_id(id)
    return render_template('question.html', result=result, answer_list=answer, header=header, question_id=id)


@app.route("/add-question", methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        result = request.form.to_dict()
        data_manager.add_question(result)
        return redirect('/list')
    return render_template('ask.html')


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        result = request.form.to_dict()
        data_manager.post_answer(result, question_id=question_id)
        return redirect(f'/question/{question_id}')
    return render_template('new_answer.html', question_id=question_id)


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )



# @app.route("/question/<question_id>/delete")
# @app.route("/question/<question_id>/edit")
# @app.route("/question/<question_id>/vote_up")
# @app.route("/question/<question_id>/vote_down")
# # Sorting: /list?order_by=title&order_direction=desc
# @app.route("/answer/<answer_id>/delete")
# @app.route("/answer/<answer_id>/vote_up")
# @app.route("/answer/<answer_id>/vote_down")