# -*- encoding=utf-8 -*-
import re
import jieba
import jieba.posseg
import pandas

data_path = "./dicts/"
sentiment_data_frame = pandas.read_excel(
            data_path + "dict_sentiment.xlsx",
            sheet_name=0,
            header=0
        )
sentiment_words = sentiment_data_frame.ix[:, "word"].values.tolist()


class CorpusPreProcessor:
    # To segment the sentences, words and remove the password
    # The delimiters of sentences
    __delimiters = "[，。！?;：,.!]"
    # Data path
    __sw_path = data_path + "stopwords.txt"
    # Stopwords
    __stopwords = [line.strip() for line in open(__sw_path, 'r', encoding='gbk').readlines()]

    def __init__(self):
        # Import sentiment dictionary
        # Load the dictionary
        for sentiment_word in sentiment_words:
            jieba.add_word(sentiment_word)

    def sentence_segment(self, comment_text):
        # Segments to sentences
        sentences = re.split(self.__delimiters, str(comment_text))
        sentences = list(filter(None, sentences))
        return sentences

    @classmethod
    def word_segment(cls, sentence):
        # Segments to words
        words = list(jieba.posseg.cut(sentence))
        words = list(filter(lambda word_pairs: word_pairs.word not in cls.__stopwords, words))
        return words


def feature_sentiment_extract(word_pairs):
    # To extract feature and extract
    features = []
    sentiments = []
    for pair in word_pairs:
        if pair.flag == 'n':
            features.append(pair.word)
        elif pair.word in sentiment_words:
            sentiments.append(pair.word)
    return features, sentiments


if __name__ == "__main__":
    # Just for example

    # Create a CorpusPreProcessor object
    cpp = CorpusPreProcessor()

    # To segment paragraph into sentences
    ss = cpp.sentence_segment("这架车不错，我很喜欢")
    print(ss[0])

    # To segment sentence into word pairs
    ps = cpp.word_segment(ss[0])

    # To extract features and sentiments
    a, b = feature_sentiment_extract(ps)
    print(a)
    print(b)
    pass
