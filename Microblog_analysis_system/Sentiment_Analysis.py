# -*- coding: utf-8 -*-
import copy
import jieba
import pandas
from matplotlib import pyplot

data_path = "/home/nico/data/情感词汇/"


def load_dictionary(file_path):
    # Create stopwords list
    stopwords = [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()]
    return stopwords


def data_segment(data):
    # Load stopwords list
    stopwords = load_dictionary('./stopwords.txt')
    segmented_data = jieba.cut(data.strip())
    stopwords_removed_data = ""
    for word in segmented_data:
        if word not in stopwords:
            if word != '\t':
                stopwords_removed_data += (word + " ")
    stopwords_removed_data.strip()
    return stopwords_removed_data


class EmotionDictionary:
    # The Emotion Dictionary class
    def __init__(self, path):
        # To load the dictionary
        sentiment_dict = pandas.read_excel(path, sheet_name=None, header=0)
        for sentiment, words in zip(sentiment_dict.keys(), sentiment_dict.values()):
            if words.empty:
                sentiment_dict.pop(sentiment)
                continue
            sentiment_dict[sentiment] = words.set_index('word')
        self.__Dictionary = sentiment_dict

    def query(self, word):
        # Get the emotional value of the word
        result = []
        sentiment_dict = self.__Dictionary
        for sentiment in sentiment_dict.keys():
            try:
                result = sentiment_dict[sentiment].ix[word, :].tolist()
                result.insert(0, sentiment)
                result.insert(0, 0)
                break
            except Exception:
                pass
        return result


def sentiment_calculate(segmented_data, emo_lo, neg_dict):
    # Calculate the value of emotion
    # Emo_lo means the Emotive Lexicon Ontology
    # Neg_dict means the negative dictionary
    # Set default sentiment none
    sentiment = "none"
    sentiment_dict = {
        # The intensity of sentiment
        "happy": 0,
        "good": 0,
        "angry": 0,
        "sorrow": 0,
        "fear": 0,
        "evil": 0,
        "shock": 0
    }
    words = segmented_data.split(" ")
    sentiment_extract_result = []
    for word in words:
        query_result = emo_lo.query(word)
        if word in neg_dict:
            sentiment_extract_result.append([1])
        elif not len(query_result) == 0:
            sentiment_extract_result.append(query_result)
    for i in range(len(sentiment_extract_result)):
        # Traveling sentiment extract result
        result = sentiment_extract_result[i]
        # If the front of the emotional word is not a negative word, add the intensity
        # to the sentiment dictionary
        if result[0] == 0:
            if i - 1 >= 0:
                if result[0] != 1:
                    sentiment_dict[result[1]] += result[3]
            if i - 1 < 0:
                sentiment_dict[result[1]] += result[3]
    max_intensity = max(sentiment_dict.items(), key=lambda x: x[1])
    if max_intensity[1] != 0:
        sentiment = max_intensity[0]
    return sentiment


def time_to_date(time):
    # Change time to date that is accurate to day
    # Such as 2018-1-1 00:00:00 -> 2018-1-1
    return time.split(' ')[0]


def get_data_line(data):
    date_line = list(set(data.ix[:, "发布时间"].tolist()))
    date_line.sort()
    for i in range(len(date_line)):
        date_line[i] = [date_line[i], 0]
    return date_line


def statistics(date_line, grouped):
    # Count sentiment of each day
    l1 = list() + date_line
    result_dict = {
        "happy": list(),
        "good": list(),
        "angry": list(),
        "sorrow": list(),
        "fear": list(),
        "evil": list(),
        "shock": list(),
        "none": list()
    }
    for key in result_dict.keys():
        result_dict[key] = copy.deepcopy(l1)
    for name, group in grouped:
        for date in result_dict[str(name[0])]:
            if date[0] == name[1]:
                date[1] += group.count()
    result_dict["happy"][0][1] += 1
    return result_dict


def get_chart(coordinate_dict, title):
    # Draw a line chart by coordinate
    pyplot.figure(figsize=(30, 10))
    pyplot.title(title)
    x = [v[0] for v in coordinate_dict["happy"]]
    for key, value in zip(coordinate_dict.keys(), coordinate_dict.values()):
        pyplot.plot(x, [v[1] for v in value], label=key)
    pyplot.legend()
    # pyplot.show()
    pyplot.savefig('figures/' + title + '.png', format='png')
    pyplot.close('all')
