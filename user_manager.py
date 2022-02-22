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
    cursor.execute(sql.SQL("SELECT username, registration_date, profile_picture, reputation FROM users WHERE id={id}").format(
        id=sql.Literal(user_id)
    ))
    return realdict_to_dict(cursor.fetchall())


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
