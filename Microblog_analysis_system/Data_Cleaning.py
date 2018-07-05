# -*- coding: utf-8 -*-
import os
import re
import pandas

data_path = {
    "blog": "/home/nico/data/2017年12月数据/2017年12月/合成数据",
    "comment": "/home/nico/data/2017年12月数据/2017年12月/评论数据"
}


def get_file_path(data_type):
    # Get the filename list
    file_path_list = []
    for root, dirs, files in os.walk(data_path[data_type]):
        for file in files:
            file_path_list.append(os.path.join(root, file))
    return file_path_list


def read_data(file_path):
    # Fetches data from a sheet
    blog_data = pandas.read_excel(file_path, sheet_name=0, header=0)
    return blog_data


def clean_blog_data(data):
    if type(data) != type('string'):
        return '0000'
    data = re.sub("【[\w\W]*?】|#[\w\W]*?#", "", data)
    data = re.sub("回复@[\w\W]*?:|//@[\w\W]*?:|\|[\w\W]*?\.\.\.", "", data)
    return data


def clean_comment_data(data):
    if len(data) == 0:
        return '0000'
    # Remove the id of users
    data = "_UserId" + data
    data = re.sub("_UserId[\w\W]*?：|回复@[\w\W]*?:|//@[\w\W]*?:|\|[\w\W]*?\.\.\.", "", data)
    data = re.sub("【[\w\W]*?】|#[\w\W]*?#", "", data)
    return data


def write_by_line(txt_name, data_list):
    with open(txt_name, "a+") as txt_file:
        for data in data_list:
            txt_file.write(data + "\n")
