# -*- encoding=utf-8 -*-
import re
import pandas
import extract

data_path = "/home/nico/data/Product_Data/"


def load_k_data(path):
    k_data = pandas.read_csv(path, header=0).ix[:, "Comment"].tolist()
    return k_data


def load_jm_zs_data(path, skiprows):
    k_data = pandas.read_excel(
        path,
        sheet_name="Data_Product_Comment",
        skiprows=skiprows,
        header=0
    ).ix[:, "Comment"].tolist()
    return k_data


def extract_fs(data):
    data_fs = []
    cpp = extract.CorpusPreProcessor()

    data = list(map(cpp.sentence_segment, data))
    word_pairs_lists = []
    for sentences in data:
        word_pairs_lists.append(list(map(cpp.word_segment, sentences)))
    for sentences, word_pairs_list in zip(data, word_pairs_lists):
        for sentence, word_pairs in zip(sentences, word_pairs_list):
            f, s = extract.feature_sentiment_extract(word_pairs)
            data_fs.append([sentence, f, s])
    return data_fs


def extract_fs_auto(data):
    data_fs = []
    cpp = extract.CorpusPreProcessor()

    data = list(map(
        lambda k0: re.split(
            "(综合|养护|服务|性价比|油耗|操控|动力|配置|舒适度|空间)：",
            k0
        )[1:],
        data
    ))
    # Split the type and comment
    data = list(map(
        lambda k1: [k1[0::2], k1[1::2]],
        data
    ))
    for k in data:
        k_types = k[0]
        comments = list(map(cpp.sentence_segment, k[1]))
        print(k_types)
        word_pairs_lists = []
        for sentences in comments:
            word_pairs_lists.append(list(map(cpp.word_segment, sentences)))
        for k_type, sentences, word_pairs_list in zip(k_types, comments, word_pairs_lists):
            s_list = []
            for sentence, word_pairs in zip(sentences, word_pairs_list):
                f, s = extract.feature_sentiment_extract(word_pairs)
                data_fs.append([sentence, f, s])
                s_list.extend(s)
            data_fs.append(["类型", k_type, s_list])
    return data_fs


def save(data, path):
    data.insert(0, ["sentence", "features", "sentiments"])
    pandas.DataFrame(data).to_csv(path, header=0, index=0)


def start(pc_file, fs_file):
    wom_data = load_k_data(data_path + pc_file)
    fs = extract_fs(wom_data)
    save(fs, fs_file)


def start_auto(pc_file, fs_file):
    wom_data = load_k_data(data_path + pc_file)
    fs = extract_fs_auto(wom_data)
    save(fs, fs_file)


if __name__ == "__main__":
    # efs = extract_fs(
    #     [
    #         "这架车不错，我很喜欢",
    #         "这架车不错，我很喜欢"
    #     ]
    # )
    # efs.insert(0, ["sentence", "features", "sentiments"])
    # pandas.DataFrame(efs).to_csv("test1.csv", header=0, index=0)

    # cpp = extract.CorpusPreProcessor()
    # print(list(map(cpp.word_segment, ["这架车不错", "我很喜欢"])))

    # print(re.split("(a1|b2|c3)：", "a1：xasad b2：fasdfa"))

    # print([1, 2, 3, 4, 5, 6, 7, 8][1::2])
    # for odd, even in [1, 2, 3, 4, 5, 6, 7, 8]:main.py:103
    #     print(odd, even)

    # PCFile = "ProductCommentPCAuto.csv"
    # FSFile = "FSPCAuto.csv"
    # start_auto(PCFile, FSFile)

    # print(load_k_data(data_path + "product_data/Phone/RawData/gome_Phone.csv"))
    # start("product_data/Phone/RawData/suning_Phone.csv", "FSsuningPhone.csv")

    wom = load_jm_zs_data(data_path + "product_data/jd.xlsx", 0)
    fs = extract_fs(wom)
    save(fs, "FSjdCamera.csv")