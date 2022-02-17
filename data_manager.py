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
def get_question_by_id(cursor, id):
    cursor.execute(sql.SQL("SELECT title, message FROM question WHERE {col}={id}").format(
        col=sql.Literal(id),
        id=sql.Identifier('id'))
    )
    content = realdict_to_dict(cursor.fetchall())
    return content


@database_common.connection_handler
def get_answers_by_id(cursor, idtype, id):
    cursor.execute(sql.SQL("SELECT * FROM answer WHERE {col}={id} ORDER BY submission_time").format(
        col=sql.SQL(idtype),
        id=sql.Literal(id))
    )
    content = cursor.fetchall()
    return content


@database_common.connection_handler
def get_comments_by_id(cursor, idtype, id):
    cursor.execute(sql.SQL("SELECT * FROM comment WHERE {col}={id}").format(
        col=sql.SQL(idtype),
        id=sql.Literal(id))
    )
    content = cursor.fetchall()
    return content


def realdict_to_dict(d):
    new_d = []
    for row in d:
        new_d.append(dict(row))
    if new_d:
        return new_d[0]
    else:
        return []


@database_common.connection_handler
def add_question(cursor, question):
    cursor.execute(sql.SQL("""INSERT INTO question (submission_time,view_number,vote_number,title,message,image)
    VALUES (CURRENT_TIMESTAMP, 0, 0, {title}, {message}, {image})""").format(
        message=sql.Literal(question['message']),
        title=sql.Literal(question['title']),
        image=sql.Literal(question['image']))
    )


@database_common.connection_handler
def delete_row(cursor, question_id, dataset):
    cursor.execute(sql.SQL("DELETE FROM {dataset} WHERE id = {question_id}").format(
        dataset=sql.SQL(dataset),
        question_id=sql.Literal(question_id))
    )


@database_common.connection_handler
def post_answer(cursor, answer, question_id):
    query = f"""INSERT INTO answer (submission_time,vote_number,question_id,message,image) 
        VALUES (CURRENT_TIMESTAMP, 0, %(question_id)s, %(answer_message)s, %(answer_image)s)"""
    data = {'question_id': question_id, 'answer_message': answer['message'], 'answer_image': answer['image']}
    cursor.execute(query, data)


@database_common.connection_handler
def post_answer(cursor, answer, question_id):
    cursor.execute(sql.SQL("""INSERT INTO answer (submission_time,vote_number,question_id,message,image) 
        VALUES (CURRENT_TIMESTAMP, 0, {question_id}, {answer_message}, {answer_image})""").format(
        answer_message=sql.Literal(answer['message']),
        answer_image=sql.Literal(answer['image']),
        question_id=sql.Literal(question_id))
    )


@database_common.connection_handler
def post_comment(cursor, comment, id, idtype):
    cursor.execute(sql.SQL("""INSERT INTO comment ({idtype}, message, submission_time, edited_count)
    VALUES ({id},{message}, CURRENT_TIMESTAMP, 0)""").format(
        idtype=sql.SQL(idtype),
        id=sql.Literal(id),
        message=sql.Literal(comment))
    )

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
def edit_answer(cursor, answer_id, new_answer_data):
    query = f"""UPDATE answer SET message = '{new_answer_data['message']}' WHERE id = {answer_id};"""
    data = {'answer_id': answer_id, 'new_answer_data': new_answer_data}
    cursor.execute(query, data)


@database_common.connection_handler
def edit_comment(cursor, comment_id, new_comment_data):
    query = f"""UPDATE comment SET edited_count = edited_count + 1, message = '{new_comment_data['message']}' WHERE id = {comment_id};"""
    data = {'comment_id': comment_id, 'new_comment_data': new_comment_data}
    cursor.execute(query, data)


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    query = f"""SELECT * FROM answer WHERE id={id}"""
    data = {'id': id}
    cursor.execute(query, data)
    cur = cursor.fetchall()
    return realdict_to_dict(cur)


@database_common.connection_handler
def get_comment_by_id(cursor, id):
    query = f"""SELECT * FROM comment WHERE id={id}"""
    data = {'id': id}
    cursor.execute(query, data)
    cur = cursor.fetchall()
    return realdict_to_dict(cur)



@database_common.connection_handler
def count_view(cursor, id):
    query = f"SELECT view_number FROM question WHERE id = {id}"
    cursor.execute(query)
    view_number = (realdict_to_dict(cursor.fetchall()))['view_number'] + 1
    query = f"""UPDATE question SET view_number = {view_number} WHERE id = {id};"""
    cursor.execute(query)


@database_common.connection_handler
def vote_message(cursor, id, dataset, vote):
    id = int(id)
    query = f"SELECT vote_number FROM {dataset} WHERE id = {id}"
    cursor.execute(query)
    vote_number = (realdict_to_dict(cursor.fetchall()))['vote_number'] + vote
    query = f"""UPDATE {dataset} SET vote_number = {vote_number} WHERE id = {id};"""
    cursor.execute(query)


@database_common.connection_handler
def search(cursor, text):
    cursor.execute(sql.SQL("""SELECT * FROM question WHERE title
        ILIKE {text} or message ILIKE {text}; """).format(
        text=sql.Literal(f"%{text}%"))
    )
    content = cursor.fetchall()
    cursor.execute(sql.SQL("""SELECT * FROM question WHERE id IN (SELECT question_id FROM answer WHERE title
            ILIKE {text} or message ILIKE {text})""").format(
        text=sql.Literal(f"%{text}%"))
    )
    content2 = cursor.fetchall()
    return content, content2
