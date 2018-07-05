from Microblog_analysis_system.Data_Cleaning import *
from Microblog_analysis_system.Sentiment_Analysis import *

elo = EmotionDictionary(data_path + "qx_dict.xlsx")
neg = load_dictionary(data_path + "否定词.txt")
data_paths = get_file_path("blog")
for data_path in data_paths:
    blog_data = read_data(data_path)
    print(data_path.split('/')[-1].split('.')[0])
    blog_data["发布时间"] = blog_data["发布时间"].apply(time_to_date)
    blog_data["博文"] = blog_data["博文"].apply(clean_blog_data)
    blog_data["博文"] = blog_data["博文"].apply(data_segment)
    blog_data["博文"] = blog_data["博文"].apply(lambda sentence: sentiment_calculate(sentence, elo, neg))
    grouped_data = blog_data.groupby(["博文", "发布时间"])["博主头像"]
    count_dict = statistics(get_data_line(blog_data), grouped_data)
    get_chart(count_dict, data_path.split('/')[-1].split('.')[0])
