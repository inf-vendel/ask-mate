from flask import Flask, render_template, request, redirect, url_for, session, flash
import connection
import data_manager
from datetime import timedelta
from werkzeug.utils import secure_filename
import os
import bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
@app.route("/list")
def list_questions(order_by="id", order_direction="desc", limit=0):
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    question_list = data_manager.get_question_list()
    # if limit:
    #     question_list = question_list[0:limit]
    list = data_manager.sort_data(order_by, order_direction) if order_by and order_direction else question_list
    return render_template('list.html',
                           question_list=list, header=connection.QUESTION_HEADER)


@app.route("login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        # Authenticate!
        database = data.users
        if session['email'] in database and hashing.verify_password(session['password'], database[session['email']]):
            flash('You just logged in! Welcome buddy!')
            return redirect('index')
        else:
            session.pop('email', None)
            session.pop('password', None)
            flash('Invalid login attempt.')
            return redirect('login')
    else:
        if "email" in session:
            return redirect('index')
    return render_template('login.html')




@app.route("/question/<int:id>")
def display_question(id):
    question = data_manager.get_question_by_id(id)
    comments = data_manager.get_comments_by_id('question_id', id)
    header = ['title', 'message']
    answer = data_manager.get_answers_by_id('question_id', id)
    for reply in answer:
        reply["comments"] = (data_manager.get_comments_by_id('answer_id', reply['id']))
    data_manager.count_view(id)
    tags = data_manager.get_tags(id)
    all_tags = data_manager.get_all_tag()
    return render_template('question.html', comments=comments, result=question,
                           answer_list=answer, header=header, question_id=id, tags=tags, all_tags=all_tags)


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'GET':
        data_manager.delete_row(question_id, 'question')
        return redirect('/list')
    return render_template('question.html')


@app.route("/<question_id>/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(answer_id, question_id):
    if request.method == 'GET':
        data_manager.delete_row(answer_id, 'answer')
        return redirect(f'/question/{question_id}')
    return render_template('question.html', question_id=question_id)


@app.route("/question/<question_id>/tag/<tag_id>/delete", methods=['GET', 'POST'])
def remove_tag(question_id, tag_id):
    if request.method == 'GET':
        data_manager.delete_tag(question_id, tag_id)
        return redirect(f'/question/{question_id}')
    return render_template('question.html', question_id=question_id)


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def add_tag(question_id):
    # tags = data_manager.get_tags(question_id)
    tags = data_manager.get_all_tag()
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        print('End point reached.')
        tag_name = request.form.get('new_tag')
        data_manager.add_tag(question_id, tag_name)
    return redirect(f'/question/{question_id}')


@app.route("/add-question", methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        result = request.form.to_dict()
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/', filename))
            result['image'] = filename
        else:
            result['image'] = "no-image-icon-0.jpg"
        data_manager.add_question(result)

        return redirect('/list')
    return render_template('ask.html')


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        result = request.form.to_dict()
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            # TODO file cannot be saved!
            result['image'] = filename
        else:
            result['image'] = "no-image-icon-0.jpg"
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


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question = data_manager.get_question_by_id(answer['question_id'])
    if request.method == 'POST':
        result = request.form.to_dict()
        data_manager.edit_answer(answer_id, result)
        return redirect(f'/question/{answer["question_id"]}')
    return render_template('edit_answer.html', answer=answer, question=question)


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    if comment['question_id']:
        question_id = comment['question_id']
    else:
        question_id = data_manager.get_answer_by_id(comment['answer_id'])['question_id']

    if request.method == 'POST':
        result = request.form.to_dict()
        data_manager.edit_comment(comment_id, result)
        return redirect(f'/question/{question_id}')
    return render_template('edit_comment.html', comment=comment)


@app.route('/question/<question_id>/<vote_type>')
def vote_question(question_id, vote_type):
    data_manager.vote_message(question_id, 'question', vote=int(vote_type))
    return redirect(f'/question/{question_id}')



@app.route("/question/<int:question_id>/answer/<answer_id>/vote_up", methods=['GET', 'POST'])
def vote_up_answer(answer_id, question_id):
    data_manager.vote_message(answer_id, 'answer', vote=1)
    return redirect(f'/question/{question_id}')


@app.route("/question/<int:question_id>/answer/<answer_id>/vote_down", methods=['GET', 'POST'])
def vote_down_answer(answer_id, question_id):
    data_manager.vote_message(answer_id, 'answer', vote=-1)
    return redirect(f'/question/{question_id}')


@app.route("/question/<int:question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        result = request.form.to_dict()
        data_manager.post_comment(comment = result['message'], id=question_id, idtype='question_id')
        return redirect(f'/question/{question_id}')
    return render_template('comment_question.html', question_id=question_id)


@app.route("/answer/<int:answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        answer = data_manager.realdict_to_dict(data_manager.get_answers_by_id('id', answer_id))
        result = request.form.to_dict()
        data_manager.post_comment(comment=result['message'], id=answer_id, idtype='answer_id')
        return redirect(f"/question/{answer['question_id']}")
    return render_template('comment_answer.html', answer_id=answer_id)


@app.route("/question/<question_id>/comment/<comment_id>/edit", methods=['GET', 'POST'])
def delete_question_comment(question_id, comment_id):
    if request.method == 'GET':
        data_manager.delete_row(comment_id, 'comment')
        return redirect(f'/question/{question_id}')
    return render_template('question.html')


@app.route("/search")
def search():
    search_phrase = request.args.get('search_phrase')
    tables = request.args.getlist('search_in')
    q,a = data_manager.search(search_phrase, tables)
    return render_template('list.html',
                           question_list=q, answer_list=a, header=connection.QUESTION_HEADER)


@app.route("/question/<question_id>/new_tag", methods=['GET', 'POST'])
def new_tag(question_id):
    if request.method == 'POST':
        print('POST', request.form['new_tag'])
        return redirect(f'/question/{question_id}')
    if request.method == 'GET':
        print('GET', request.form['new_tag'])
        return redirect(f'/question/{question_id}')
    return render_template('question.html', question_id=question_id)



if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
from flask import Flask, render_template
from bonus_questions import SAMPLE_QUESTIONS

app = Flask(__name__)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


if __name__ == "__main__":
    app.run(debug=True)
