import csv
import os

HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
DATA_FIELD_PATH_1 = 'sample_data/question.csv'
DATA_FIELD_PATH_2 = 'sample_data/question.csv'

def read_answer_file():
    list = []
    with open(DATA_FIELD_PATH_1, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            list.append(row)
    return list


def read_question_file():
    list = []
    with open(DATA_FIELD_PATH_2, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            list.append(row)
    return list


# def write_answer_file(file_name, table, separator=';'):
#     with open(file_name, "w") as file:
#         for record in table:
#             row = separator.join(record)
#             file.write(row + "\n")
