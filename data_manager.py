import connection
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_common


QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
DATA_FIELD_PATH_1 = 'sample_data/question.csv'
DATA_FIELD_PATH_2 = 'sample_data/answer.csv'


@database_common.connection_handler
def get_question_list(cursor):
    query = """SELECT * FROM question ORDER BY id ASC;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_list(cursor):
    query = """SELECT * FROM answer ORDER BY id ASC;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, id):
    query = f"""SELECT title, message FROM question 
                WHERE id={id}"""
    data = {'id': id}
    cursor.execute(query, data)
    cur = cursor.fetchall()
    return realdict_to_dict(cur)


def filter_question(question, headers=[]):
    data = []

    for item in headers:
        data.append(question[item])
    return data


def realdict_to_dict(d):
    new_d = []
    for row in d:
        new_d.append(dict(row))
    return new_d


@database_common.connection_handler
def get_answers_by_id(cursor, id):
    query = f"""SELECT * FROM answer 
                    WHERE question_id='{id}'"""
    data = {'id': id}
    cursor.execute(query, data)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, question):
    query = f"""INSERT INTO question (submission_time,view_number,vote_number,title,message,image) 
    VALUES (CURRENT_TIMESTAMP, 0, 0, '{question['title']}', '{question['message']}', '{question['image']}')"""
    data = {'question': question['title']}
    cursor.execute(query, data)


@database_common.connection_handler
def get_dict_from_list(cursor, list, head, id):
    # Where head == id in the list's dict is true.
    for i, question in enumerate(list):
        if int(question[head]) == id:
            return i


@database_common.connection_handler
def delete_row(cursor, question_id, dataset):
    query = f"DELETE FROM {dataset} WHERE id = {question_id};"
    data = {'question_id': question_id, 'dataset': dataset}
    cursor.execute(query)


@database_common.connection_handler
def post_answer(cursor, answer, question_id):
    query = f"""INSERT INTO answer (submission_time,vote_number,question_id,message,image) 
        VALUES (CURRENT_TIMESTAMP, 0, '{question_id}', '{answer['message']}', '{answer['image']}')"""
    data = {'question_id': question_id, 'answer': answer}
    cursor.execute(query, data)


@database_common.connection_handler
def fill_post(post_type, header):
    if header == 'id':
        return generate_new_id(post_type)
    elif header == 'submission_time':
        return 1234
    elif header == 'view_number':
        return 0
    elif header == 'vote_number':
        return 0


@database_common.connection_handler
def generate_new_id(post_type):
    arr = get_question_list() if post_type == 'question' else get_answer_list()
    ids = [int(q['id']) for q in arr]
    new_id = max(ids) + 1
    if post_type == 'question':
        return new_id
    if post_type == 'answer':
        return new_id


@database_common.connection_handler
def sort_data(data, header, reversed):
    dir = True if reversed == "asc" else False
    sorted_list = sorted(data, key=lambda x: x[header], reverse=dir)
    return sorted_list


@database_common.connection_handler
def edit_question(question_id, new_question_data):
    question_list = get_question_list()
    id = int(question_id)
    question = get_question_by_id(id)
    question['title'] = new_question_data['title']
    question['message'] = new_question_data['message']
    element = get_dict_from_list(question_list, 'id', id)
    question_list[element] = question
    connection.write_file('sample_data/question.csv', question_list, header=QUESTION_HEADER)


@database_common.connection_handler
def get_answer_by_id(id):
    answers = get_answer_list()
    i = get_dict_from_list(answers, "id", id)
    return answers[i]


@database_common.connection_handler
def count_view(cursor, id):
    query = f"SELECT view_number FROM question WHERE id = {id}"
    cursor.execute(query)
    view_number = (realdict_to_dict(cursor.fetchall()))[0]['view_number'] + 1
    query = f"""UPDATE question SET view_number = {view_number} WHERE id = {id};"""
    cursor.execute(query)


@database_common.connection_handler
def vote_message(cursor, id, dataset, vote):
    id = int(id)
    query = f"SELECT vote_number FROM {dataset} WHERE id = {id}"
    cursor.execute(query)
    vote_number = (realdict_to_dict(cursor.fetchall()))[0]['vote_number'] + vote
    query = f"""UPDATE {dataset} SET vote_number = {vote_number} WHERE id = {id};"""
    cursor.execute(query)



