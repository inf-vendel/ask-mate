import csv
import os

from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor



QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
DATA_FIELD_PATH_1 = 'sample_data/question.csv'
DATA_FIELD_PATH_2 = 'sample_data/answer.csv'


def read_file(data_field):
    path = data_field
    list = []
    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            list.append(row)
    return convert_to_integer(list, ["id", "vote_number", "view_number", "submission_time"])



def write_file(data_field, data, header):
    path = data_field
    with open(path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)



def convert_to_integer(data, header):
    for head in header:
        for i, arr in enumerate(data):
            try:
                data[i][head] = int(data[i][head])
            except KeyError or ValueError:
                pass

    return data