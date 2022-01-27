import csv
import os

QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id","submission_time","vote_number","question_id","message","image"]
DATA_FIELD_PATH_1 = 'sample_data/question.csv'
DATA_FIELD_PATH_2 = 'sample_data/answer.csv'


def read_file(data_field):
    path = data_field
    list = []
    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            list.append(row)
    return list


def write_file(data_field, data, header):
    path = data_field
    with open(path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header)
        writer.writeheader()
        writer.writerows(data)


