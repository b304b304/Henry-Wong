# -*- coding: utf-8 -*-
import jieba
import pandas


def stopwords_list(file_path):
    # Create stopwords list
    stopwords = [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()]
    return stopwords


def data_segment(data_list):
    segmented_data_list = []
    # Load stopwords list
    stopwords = stopwords_list('./stopwords.txt')
    for data in data_list:
        segmented_data = jieba.cut(data.strip())
        stopwords_removed_data = ""
        for word in segmented_data:
            if word not in stopwords:
                if word != '\t':
                    stopwords_removed_data += (word + " ")
        segmented_data_list.append(stopwords_removed_data)
    return segmented_data_list


class EmotionDictionary:
    # The Emotion Dictionary class
    # The pointer to current word
    __cur_word = 0
    # The mapping from polarity ro polar value
    __polarity_dic = {
        0: 0,
        1: 1,
        2: -1,
        3: 0
    }

    def __init__(self, path):
        # To load the dictionary
        self.__Dictionary = pandas.read_excel(path, sheet_name=0, skiprows=[0])
        self.__word_list = self.__Dictionary.ix[:, 0].tolist()

    def query(self, word):
        # Get the emotional value of the word
        if word in self.__word_list:
            self.__cur_word = self.__word_list.index(word)
            emotional_values = self.__Dictionary.ix[self.__cur_word, :].tolist()
            polar_value = self.__polarity_dic[emotional_values[6]]
            emotional_value = emotional_values[5] * polar_value
            return emotional_value
        else:
            return 0


def emotion_calculate(segmented_data):
    # Calculate the value of emotion
    # Load the emotional dictionary Emotive Lexicon Ontology
    elo = EmotionDictionary("/home/nico/data/情感词汇/情感词汇本体.xlsx")
    segmented_data_list = segmented_data.split(" ")
    emotion_value_of_data = 0
    for word in segmented_data_list:
        emotion_value_of_data += elo.query(word)
    return emotion_value_of_data

if __name__ == "__main__":
    cleaned_data_list = []
    with open("./cleaned_data.txt") as cleaned_data:
        for cleaned_data_line in cleaned_data.readlines():
            cleaned_data_list.append(cleaned_data_line)
    segmented_cleaned_data_list = data_segment(cleaned_data_list)
    with open("calculated_data.txt", "a+") as cal_data:
        for c_data, s_c_data in zip(cleaned_data_list, segmented_cleaned_data_list):
            emotion_value = "emotion_value:" + str(emotion_calculate(s_c_data))
            cal_data.write(emotion_value + " " + c_data)
