import urllib.request
import time
import re
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from textProcess import textProcess

#创建目录
def mkdir(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    else:
        pass

class ciompSpider:
    def __init__(self):
        self.source_url = r'http://www.ciomp.cas.cn/xwdt/zhxw/'
        self.path = r'./ciompclaw/news/'

    #获取html
    def get_html(self, url):
        headers = {
            'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        return html

    #爬取单页新闻
    def parse_mainlist(self, html):
        title = []
        date = []
        url = []       
        soup = BeautifulSoup(html, features="lxml")
        title_list = soup.select('.font06')
        date_list = soup.select('.riqi')
        #可获取链接分为6种情况，分别处理以得到正确的页面url
        for i in range(len(title_list)):
            title.append(str(title_list[i]['title']))
            if title_list[i]['href'][0] == '.':
                if title_list[i]['href'][3] != '.':
                    if title_list[i]['href'][1] == '/':
                        url.append(r'http://www.ciomp.cas.cn/xwdt/zhxw/' + title_list[i]['href'][2:])
                    else:
                        url.append(r'http://www.ciomp.cas.cn/xwdt/' + title_list[i]['href'][3:])
                else:
                    url.append(r'http://www.ciomp.cas.cn/' + title_list[i]['href'][6:])
            else:
                url.append(title_list[i]['href'])
            date.append(date_list[i].text[1:-1])
        data = {'title':pd.Series(title), 'department':np.nan, 'date':pd.Series(date), 'url':pd.Series(url)}
        return data

    #爬取新闻总表
    def get_mainlist(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, features="lxml")
        #获取总页数
        pattern = re.compile(r'var countPage = \d+', re.MULTILINE | re.DOTALL)
        pageNum = soup.find("script", attrs={'language':'JavaScript'}, text=pattern)
        num = int(str(pattern.search(pageNum.text).group(0))[-2:])
        print('总页数:', num)
        print('正在爬取第 1 页', end='', flush=True)
        data = self.parse_mainlist(html)
        news_index = pd.DataFrame(data)
        for i in range(1,num):
            print('\r正在获取第', i+1, '页', end='', flush=True)
            url_page = url + r'index_' + str(i) + r'.html'
            html = self.get_html(url_page)
            data = self.parse_mainlist(html)
            df = pd.DataFrame(data)
            news_index = pd.concat([news_index, df])
        news_index = news_index.reset_index(drop=True)
        return news_index

    #爬取新闻内容并处理部门内容
    def get_news(self, news_index):
        print('\r正在爬取新闻内容...')
        tp = textProcess()
        date = news_index.loc[0, 'date']
        path_date = self.path + date
        mkdir(path_date)
        for i in tqdm(range(news_index.shape[0])):
            datetmp = news_index.loc[i, 'date']
            url = news_index.loc[i, 'url']
            title = tp.title_process(news_index.loc[i, 'title'])
            html = self.get_html(url)
            soup = BeautifulSoup(html, features="lxml")
            department = soup.select('td[width="22%"]') #获取部门
            whole_text = soup.select('p')
            if len(department) > 0:
                news_index.loc[i, 'department'] = department[0].text
            else:
                news_index.loc[i, 'department'] = ''
            #同日期存入同一文件夹，不同日期创建新文件夹
            if datetmp == date:
                filepath = path_date + r'/' + title + r'.txt'
            else:
                date = datetmp
                path_date = self.path + datetmp
                mkdir(path_date)
                filepath = path_date + r'/' + title + r'.txt'
            #存储新闻内容
            fd = open(filepath, 'w', encoding='utf-8')
            fd.write('Title: ' + title + '\n')
            fd.write('Date: ' + date + '\n')
            fd.write('Department: ' + str(news_index.loc[i, 'department']) + '\n')
            fd.write('News:\n')
            for j in range(len(whole_text)):
                fd.write(whole_text[j].text + '\n')
            fd.close()
        #生成原始新闻总表
        news_index.to_excel(r'./ciompclaw/news/news_index_origin.xlsx', sheet_name='news_index')
        print('原始列表已生成！')
        print('正在处理混乱的department....')
        news = pd.read_excel(r'./ciompclaw/news/news_index_origin.xlsx', sheet_name='news_index')
        news = news.fillna('其他')
        news = tp.dep_process(news) #处理混乱的部门
        #生成最终新闻总表
        news.loc[:,'title':'url'].to_excel(r'./ciompclaw/news/news_index.xlsx', sheet_name='news_index')
        print('\n已完成！')
        print('爬取新闻总数：' + str(news_index.shape[0]))
    
    def process(self):
        news_index = self.get_mainlist(self.source_url)
        self.get_news(news_index)