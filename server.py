from flask import Flask, render_template, request, redirect, url_for, session, flash
import connection
import data_manager
import user_manager
from datetime import timedelta
from werkzeug.utils import secure_filename
import os
from bonus_questions import SAMPLE_QUESTIONS
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/')

app = Flask(__name__)
app.secret_key = os.urandom(16)
# app.permanent_session_lifetime = timedelta(minutes=10)


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


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['psw']
        if user_manager.auth_register(session['username']):
            user_manager.register(session['username'], session['password'], "no_profile.png")
            user = user_manager.authenticate_user(session['username'], session['password'])
            session['id'] = user
            return redirect('/list')
        else:
            flash('Username already taken!')
    else:
        if "id" in session:
            return redirect('list')
    return render_template('register.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['psw']
        # TODO check if password is acceptable (length, special char, num)
        # TODO check if username is acceptable (only abc,ABC,0-9)
        user_id = user_manager.authenticate_user(session['username'], session['password'])
        if user_id:
            flash(f'You successfully logged in! Welcome {session["username"]}')
            session.pop('username', None)
            session.pop('password', None)
            session['id'] = user_id
            session.permanent = True
            if request.form['remember']:
                app.permanent_session_lifetime = timedelta(weeks=5)
            else:
                app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect('list')
        else:
            session.pop('username', None)
            session.pop('password', None)
            flash(u'Invalid login attempt.', 'error')
            return redirect('login')
    else:
        if is_logged_in():
            return redirect('list')
    return render_template('login.html')


@app.route("/logout")
def logout():
    if 'id' in session:
        session.pop('id')
        flash('Successfully logged out.')
    return redirect('list')


@app.route("/profile")
def profile():
    if 'id' in session:
        user_info = user_manager.get_user_by_id(session['id'])
        return render_template('profile.html', user_info=user_info)
    else:
        return redirect('login')


@app.route("/question/<int:id>")
def display_question(id):
    question = data_manager.get_question_by_id(id)
    comments = data_manager.get_comments_by_id('question_id', id)
    answer = data_manager.get_answers_by_id('question_id', id)
    for reply in answer:
        reply["comments"] = (data_manager.get_comments_by_id('answer_id', reply['id']))
    data_manager.count_view(id)
    tags = data_manager.get_tags(id)
    all_tags = data_manager.get_all_tag()
    asker = user_manager.get_user_by_id(question['user_id'])
    if not asker:
        asker = generate_profile()
        asker['id'] = 0
    return render_template('question.html', comments=comments, result=question,
                           answer_list=answer, question_id=id, tags=tags, all_tags=all_tags, asker=asker)


@app.route("/user/<int:user_id>", methods=['GET', 'POST'])
def show_user(user_id):
    user = user_manager.get_user_by_id(user_id)
    questions = user_manager.get_user_questions(user_id)
    if not user:
        user = generate_profile()
        flash("User not found. :( As a compensation here's a randomly generated profile:", 'error')
    return render_template('user.html', user_info=user, questions=questions)


def generate_profile():
    return {"username": "None Existent", "registration_date": "2000.12.12", "profile_picture": "cdcdcdcd2.jpg", "reputation": '-999'}


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
        tag_name = request.form.get('new_tag')
        data_manager.add_tag(question_id, tag_name)
    return redirect(f'/question/{question_id}')


@app.route("/add_pp", methods=['GET', 'POST'])
def add_pp():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOADS_PATH, filename))
        user_manager.add_pp(session['id'], filename)
        return redirect('profile')


@app.route("/add-question", methods=['GET', 'POST'])
def ask_question():
    if 'id' in session:
        if request.method == 'POST':
            result = request.form.to_dict()
            file = request.files['image']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOADS_PATH, filename))
                result['image'] = filename
            else:
                result['image'] = "no-image-icon-0.jpg"
            data_manager.add_question(result, session['id'])

            return redirect('/list')
        return render_template('ask.html')
    else:
        flash('Please log in to use this function.')
        return redirect('login')


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if 'id' in session:
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
    else:
        flash('Please log in to use this function.')
        return redirect('login')



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
    is_logged_in()
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


@app.route("/about")
def about():
    return render_template('about.html')


def is_logged_in():
    return True if 'id' in session else False


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )

@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)
