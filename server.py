from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route('/')
@app.route("/list", methods=['GET', 'POST'])
def list_questions(order_by="id", order_direction="desc"):
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    question_list = data_manager.get_question_list()
    list = data_manager.sort_data(question_list, order_by, order_direction) if order_by and order_direction else question_list
    return render_template('list.html',
                           question_list=list, header=connection.QUESTION_HEADER)


@app.route("/question/<int:id>", methods=['GET', 'POST'])
def display_question(id):
    question = data_manager.get_question_by_id(id)
    header = ["title", "message"]
    result = data_manager.filter_question(question=question, headers=header)
    answer = data_manager.get_answers_by_id(id)
    return render_template('question.html', result=result, answer_list=answer, header=header, question_id=id)


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'GET':
        data_manager.delete_question(question_id)
        return redirect('/list')
    return render_template('question.html')


@app.route("/<question_id>/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(answer_id, question_id):
    if request.method == 'GET':
        data_manager.delete_answer(answer_id)
        return redirect(f'/question/{question_id}')
    return render_template('question.html', question_id=question_id)


@app.route("/add-question", methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        result = request.form.to_dict()
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            result['image'] = filename
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


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        result = request.form.to_dict()
        data_manager.edit_question(question_id, result)
        return redirect(f'/question/{question_id}')
    return render_template('edit_question.html', question_id=question_id, question=question)


# @app.route("/question/<question_id>/vote_up", methods=['GET', 'POST'])
# def vote_up_question(question_id):
#     data_manager.vote_message(question_id, 'question', vote = 1)
#     return redirect('/list')
#
#
# @app.route("/question/<question_id>/vote_down", methods=['GET', 'POST'])
# def vote_down_question(question_id):
#     data_manager.vote_message(question_id, 'question', vote = -1)
#     return redirect('/list')
#

@app.route('/question/<question_id>/<vote_type>')
def vote_question(question_id, vote_type):
    data_manager.vote_message(question_id, 'question', vote=int(vote_type))
    return redirect('/list')


@app.route("/question/<int:question_id>/answer/<answer_id>/vote_up", methods=['GET', 'POST'])
def vote_up_answer(answer_id, question_id):
    data_manager.vote_message(answer_id, 'answer', vote=1)
    return redirect(f'/question/{question_id}')


@app.route("/question/<int:question_id>/answer/<answer_id>/vote_down", methods=['GET', 'POST'])
def vote_down_answer(answer_id, question_id):
    data_manager.vote_message(answer_id, 'answer', vote=-1)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id, question_id):
    if request.method == 'POST':
        return redirect(f'/question/{question_id}')


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