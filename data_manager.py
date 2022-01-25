import connection

HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id","submission_time","vote_number","question_id","message","image"]

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
    print(answer_list)
    if id in [int(answer['question_id']) for answer in answer_list]:
        answers = [answer['message'] for answer in answer_list if int(answer['question_id']) == id]
        return answers
    else:
        return False


def add_question(question):
    data = get_question_list()
    for header in HEADER:
        if header not in list(question.keys()):
            question[header] = fill_post(post_type='question', header=header)
    data.append(question)
    connection.write_file('question', data)


def post_answer(answer, question_id):
    data = get_answer_list()
    answer['question_id'] = question_id
    for header in ANSWER_HEADER:
        if header not in list(answer.keys()):
            answer[header] = fill_post(post_type='answer', header=header)
    data.append(answer)
    connection.write_file('answer', data)


def fill_post(post_type, header):
    if header == 'id':
        return generate_new_id(post_type)
    elif header == 'submission_time':
        return 1234
    elif header == 'view_number':
        return 0
    elif header == 'vote_number':
        return 0


def generate_new_id(post_type):
    if post_type == 'question':
        return len(get_question_list())
    if post_type == 'answer':
        return len(get_answer_list())



#
# def sort_question():