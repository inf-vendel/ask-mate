import psycopg2

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
    cursor.execute(sql.SQL("SELECT * FROM question ORDER BY id ASC"))
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_list(cursor):
    cursor.execute(sql.SQL("SELECT * FROM answer ORDER BY id ASC"))
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute(sql.SQL("SELECT title, message FROM question WHERE id={id}").format
                   (id=sql.Identifier("id")))
    return cursor.fetchall()


# def filter_question(question, headers=[]):
#     data = []
#
#     for item in headers:
#         data.append(question[item])
#     return data


def realdict_to_dict(d):
    new_d = []
    for row in d:
        new_d.append(dict(row))
    return new_d


@database_common.connection_handler
def get_answers_by_id(cursor, idtype, id):
    cursor.execute(sql.SQL("SELECT * FROM answer WHERE {idtype} = {id}").format
                   (idtype=sql.Identifier(idtype),
                    id=sql.Identifier("id")))
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, question):
    cursor.execute(sql.SQL("""INSERT INTO question (submission_time,view_number,vote_number,title,message,image)
    VALUES (CURRENT_TIMESTAMP, 0, 0, {title}, {message}, {image})""").format
                   (message=sql.Literal(question['message']),
                    title=sql.Literal(question['title']),
                    image=sql.Literal(question['image'])))


@database_common.connection_handler
def get_dict_from_list(cursor, list, head, id):
    # Where head == id in the list's dict is true.
    for i, question in enumerate(list):
        if int(question[head]) == id:
            return i


@database_common.connection_handler
def delete_row(cursor, question_id, dataset):
    cursor.execute(sql.SQL("DELETE FROM {dataset} WHERE id = {question_id}").format
                   (dataset=sql.SQL(dataset),  # sql table name
                    question_id=sql.Literal(question_id)))


@database_common.connection_handler
def post_answer(cursor, answer, question_id):
    query = f"""INSERT INTO answer (submission_time,vote_number,question_id,message,image) 
        VALUES (CURRENT_TIMESTAMP, 0, %(question_id)s, %(answer_message)s, %(answer_image)s)"""
    data = {'question_id': question_id, 'answer_message': answer['message'], 'answer_image': answer['image']}
    cursor.execute(query, data)
    try:
        cursor.fetchone()
    except psycopg2.ProgrammingError:
        pass


@database_common.connection_handler
def post_comment(cursor, comment, id, dataset):
    query = f"""INSERT INTO comment ({dataset},message,submission_time,edited_count) 
        VALUES ({id}, '{comment}', CURRENT_TIMESTAMP, 0)"""
    data = {'id': id, 'dataset': dataset, 'comment': comment}
    cursor.execute(query, data)
    # (result['message'], id=question_id, dataset='question_id')

@database_common.connection_handler
def sort_data(cursor, header, reversed):
    query = f"""SELECT * FROM question ORDER BY {header} {reversed};"""
    data = {'header': header, 'reversed': reversed}
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def edit_question(cursor, question_id, new_question_data):
    query = f"""UPDATE question SET title = '{new_question_data['title']}',
    message = '{new_question_data['message']}' WHERE id = {question_id};"""
    data = {'question_id': question_id, 'new_question_data': new_question_data}
    cursor.execute(query, data)


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    query = f"""SELECT title, message FROM answer WHERE id={id}"""
    data = {'id': id}
    cursor.execute(query, data)
    cur = cursor.fetchall()
    return realdict_to_dict(cur)


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

#
# def get_comments_by_id(cursor, id, dataset):
#     query = """SELECT message, submission_time FROM comment WHERE %(dataset)s = %(id)s"""
#     data = {'id': id, 'dataset': dataset}
#     cursor.execute(query, data)
#     cur = cursor.fetchall()
#     return realdict_to_dict(cur)


def checkinput(text):
    # TODO add a single quote to every single quote that is on its own.
    return text


@database_common.connection_handler
def search(text):
    query = f"""SELECT * FROM question WHERE LIKE'%'{text};"""
    pass
