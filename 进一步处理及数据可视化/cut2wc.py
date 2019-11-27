import jieba
import matplotlib.pyplot as plt
from os import path
from pandas import read_csv
from wordcloud import WordCloud

df = read_csv(r'D:\PycharmProjects\ciomp_spider\ciomp_spider\spiders\xbody.csv', encoding='utf-8', header=0)
# print(df.head())
# d = path.dirname(__file__)
mydic = {}


for i in range(0, len(df)):
    older = ''
    # print(x)
    # print(df.iloc[i]['time'])
    if mydic.__contains__(df.iloc[i]['date']):
        older = mydic[df.iloc[i]['date']]
    content = ' '.join(df.iloc[i]['xbody'])
    content = content.replace('\\', '').replace(' ', '').replace('\r\n', '').replace('[', '').replace(']', '').replace(
        '"', '').replace("'", '')
    newer = older + content
    mydic[df.iloc[i]['date']] = newer

for date in mydic:
    word_list = ' '.join(jieba.cut(mydic[date]))
    wordcloud = WordCloud(font_path='simhei.ttf',
                          width=800,
                          height=600,
                          background_color='white').generate(word_list)
    # plt.imshow(wordcloud)
    # plt.show()
    wordcloud.to_file(path.join(r'D:\PycharmProjects\ciomp_spider\ciomp_spider\cloudword', date + ".png"))
