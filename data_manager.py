import connection

HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]


def get_question_list():
    question_list = connection.read_file('question')
    return question_list


def get_answer_list():
    answer_list = connection.read_file('answer')
    return answer_list


def get_question_by_id(id):
    question_list = get_question_list()
    if len(question_list) <= id:
        return f"There is no question with id:{id}."
    else:
        return question_list[id-1]

def filter_question(question, headers=[]):
    data = []
    for item in headers:
        data.append(question[item])
    return data

def get_answer_by_id(id):
    answer_list = get_answer_list()
    if id in [int(answer['question_id']) for answer in answer_list]:
        answers = [answer['message'] for answer in answer_list if int(answer['question_id']) == id]
        return answers
    else:
        return False

# def add_question(question):
#     data = connection.read_file()
#     data.append(question)
#     connection.write_file()
#
#
# def post_answer():
#     pass
#
# def sort_question():