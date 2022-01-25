import csv
import os

HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
DATA_FIELD_PATH_1 = 'sample_data/question.csv'
DATA_FIELD_PATH_2 = 'sample_data/answer.csv'


def read_file(data_field):
    path = get_path(data_field)
    list = []
    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            list.append(row)
    return list


def write_file(data_field, data):
    path = get_path(data_field)
    with open(path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = HEADER)
        writer.writeheader()
        writer.writerows(data)


def get_path(data_field):
    global DATA_FIELD_PATH_1, DATA_FIELD_PATH_2
    if data_field == 'question':
        return DATA_FIELD_PATH_1
    else:
        return DATA_FIELD_PATH_2
