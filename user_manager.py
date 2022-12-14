import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_common
import hash
from data_manager import realdict_to_dict

@database_common.connection_handler
def auth_register(cursor, username):
    # Authenticate registration
    if get_user_by_name(username):
        return False
    else:
        return True

@database_common.connection_handler
def register(cursor, username, password, profile_picture):
    password_hashed = hash.hash_password(password)
    cursor.execute(sql.SQL("""INSERT INTO users (username, password, registration_date, profile_picture, reputation)
        VALUES({username}, {password}, CURRENT_TIMESTAMP, {profile_picture}, 0)""").format(
        username = sql.Literal(username),
        password=sql.Literal(password_hashed),
        profile_picture=sql.Literal(profile_picture)
    ))


@database_common.connection_handler
def get_user_by_name(cursor, username):
    cursor.execute(sql.SQL("SELECT * FROM users WHERE username={username}").format(
        username=sql.Literal(username)
    ))
    return cursor.fetchall()


@database_common.connection_handler
def get_user_by_id(cursor, user_id):
    cursor.execute(sql.SQL("""SELECT id, username, registration_date, profile_picture, reputation
        FROM users WHERE id={id}""").format(
        id=sql.Literal(user_id)
    ))
    return realdict_to_dict(cursor.fetchall())


@database_common.connection_handler
def get_all_user(cursor):
    cursor.execute(sql.SQL("""SELECT users.username, users.registration_date, COUNT(q.id) as questions, COUNT(a.id) AS answers
    FROM users LEFT JOIN question AS q on users.id = q.user_id
    LEFT JOIN answer AS a on users.id = a.user_id
    GROUP BY users.username, users.registration_date, users.id"""))
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_user_questions(cursor, id):
    cursor.execute(sql.SQL("""SELECT *
    FROM users JOIN question ON users.id=question.user_id WHERE users.id={id};""").format(id=sql.Literal(id)))
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_user_comments(cursor, id):
    cursor.execute(sql.SQL("""SELECT *
    FROM users JOIN comment ON users.id=comment.user_id WHERE users.id={id};""").format(id=sql.Literal(id)))
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_user_answers(cursor, id):
    cursor.execute(sql.SQL("""SELECT *
    FROM users JOIN answer ON users.id=answer.user_id WHERE users.id={id};""").format(id=sql.Literal(id)))
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def add_pp(cursor, id, filename):
    cursor.execute(sql.SQL("""UPDATE users SET profile_picture={filename} WHERE id={id};""").format(
        id=sql.Literal(id),
        filename=sql.Literal(filename)))


@database_common.connection_handler
def authenticate_user(cursor, username, password):
    cursor.execute(sql.SQL("SELECT id, password FROM users WHERE username={username} ").format(
        username=sql.Literal(username),
    ))
    data = cursor.fetchall()
    if not data:
        return False
    elif hash.verify_password(password, data[0]['password']):
        return data[0]['id']
    else:
        return False
