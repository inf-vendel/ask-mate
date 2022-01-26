import connection

QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id","submission_time","vote_number","question_id","message","image"]


def get_question_list():
    question_list = connection.read_file('question')
    sorted_list = sorted(question_list, key=lambda x: int(x['id']), reverse=True)
    return sorted_list


def get_answer_list():
    answer_list = connection.read_file('answer')
    return answer_list


def get_question_by_id(id):
    question_list = get_question_list()
    jani = get_dict_from_list(question_list, "id", id)
    return question_list[jani]


def filter_question(question, headers=[]):
    data = []
    for item in headers:
        data.append(question[item])
    return data


def get_answers_by_id(id):
    answer_list = get_answer_list()
    if id in [int(answer['question_id']) for answer in answer_list]:
        answers = [answer['message'] for answer in answer_list if int(answer['question_id']) == id]
        return answers
    else:
        return []


def add_question(question):
    data = get_question_list()
    for header in QUESTION_HEADER:
        if header not in list(question.keys()):
            question[header] = fill_post(post_type='question', header=header)
    data.append(question)
    connection.write_file('question', data, header=QUESTION_HEADER)


def get_dict_from_list(list, head, id):
    for i, question in enumerate(list):
        if int(question[head]) == id:
            return i


def delete_question(question_id):
    question_list = get_question_list()
    id = int(question_id)
    del question_list[get_dict_from_list(id=id, list=question_list, head="id")]
    connection.write_file('question', question_list, header=QUESTION_HEADER)


def post_answer(answer, question_id):
    data = get_answer_list()
    answer['question_id'] = question_id
    for header in ANSWER_HEADER:
        if header not in list(answer.keys()):
            answer[header] = fill_post(post_type='answer', header=header)
    data.append(answer)
    connection.write_file('answer', data, header=ANSWER_HEADER)


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
    arr = get_question_list() if post_type == 'question' else get_answer_list()
    ids = [int(q['id']) for q in arr]
    new_id = max(ids) + 1
    if post_type == 'question':
        return new_id
    if post_type == 'answer':
        return new_id


def sort_data(data, header, reversed):
    sorted_list = sorted(data, key=lambda x: int(x[header]), reverse=reversed)
    return sorted_list

