# -*- coding: utf-8 -*-
import os
import re
import pandas

data_path = {
    "blog": "/home/nico/data/2017年12月数据/2017年12月/合成数据",
    "comment": "/home/nico/data/2017年12月数据/2017年12月/评论数据"
}

column_of_data = {
    "blog": 5,
    "comment": 4
}


def get_file_path(data_type):
    # Get the filename list
    file_path_list = []
    for root, dirs, files in os.walk(data_path[data_type]):
        for file in files:
            file_path_list.append(os.path.join(root, file))
    return file_path_list


def read_data(file_path, data_type):
    # Fetches data from a sheet
    blog_data = pandas.read_excel(file_path, sheet_name=0, skiprows=[0])
    data_list = blog_data.ix[:, column_of_data[data_type]].tolist()
    return data_list


def cleaning(data_list, data_type):
    # Clean the different types of data
    if data_type == "blog":
        for i in range(len(data_list)):
            data_list[i] = re.sub("【[\w\W]*?】|#[\w\W]*?#", "", data_list[i])
    elif data_type == "comment":
        # Remove the id of users
        for i in range(len(data_list)):
            data_list[i] = "_UserId" + data_list[i]
            data_list[i] = re.sub("[_UserId\w\W]*?：|回复@[\w\W]*?:|//@[\w\W]*?:", "", data_list[i])
            data_list[i] = re.sub("【[\w\W]*?】|#[\w\W]*?#", "", data_list[i])
    data_list.append(' ')
    while '' in data_list:
        data_list.remove('')
    while ' ' in data_list:
        data_list.remove(' ')
    return data_list


def write_by_line(txt_name, data_list):
    with open(txt_name, "a+") as txt_file:
        for data in data_list:
            txt_file.write(data + "\n")

if __name__ == '__main__':
    comment_file_path_list = get_file_path("comment")
    comment_data_list = read_data(comment_file_path_list[0], "comment")[0:100]
    cleaned_comment_data_list = cleaning(comment_data_list, "comment")
    write_by_line("cleaned_data.txt", cleaned_comment_data_list)
