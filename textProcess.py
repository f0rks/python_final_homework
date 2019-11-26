import pandas as pd
import re

class textProcess:
    def __init__(self):
        self.dep_dic = {}
        self.del_list = ['张译心', '张凌童', '王启东', '周哲', '张财华', '荆雷', '常唯', '王浩泽', '刘艳']
        self.add_dic = {'航测部':'', '空间三部':'', '无人飞行器':'', '希达':'', '长光智欧':'', '科宇物业':''}

    #针对title出现的特殊情况进行处理，防止生成txt时文件名不合法
    def title_process(self, title):
        if title.find('<P>') != -1:
            regex = r'</?P>'
            title = re.sub(regex, '', title, re.I)
            title = re.sub(regex, ' ', title, re.I)
        title = title.strip('</P>').strip(';')
        title = title.replace('/', '、').replace('?', '？')
        return title
    
    #部门名称规范化
    def dep_norm_process(self, department):
        department = department.replace('所办', '所长办公室')
        department = department.replace('党办', '党委办公室')
        department = department.replace('light', 'Light')
        department = department.replace('国合处', '国际合作处')
        department = department.replace('人力处', '人力资源处')
        department = department.replace('质量处', '质量管理处')
        department = department.replace('监审处', '监察审计处')
        department = department.replace('成果处', '成果转化处')
        department = department.replace('保密处', '保密管理处')
        department = department.replace('图像室', '图像部')
        department = department.replace('无人飞行器', '无人飞行器部')
        department = department.replace('孵化器公司', '孵化器')
        department = department.replace('希达', '长春希达')
        department = department.replace('科宇公司', '科宇物业')
        department = department.replace('奥普质管部', '奥普公司')
        return department

    #部门名称匹配
    def dep_process(self, news_index):
        #依据原始新闻列表的部门生成初始字典，内容为{'部门'：[人员名单]}
        for i in range(news_index.shape[0]):
            department = news_index.loc[i, 'department']
            if department.find(' ') != -1:
                department = department.replace('\\', ' ')
                department = department.strip().split()
                if len(department) == 2:
                    if department[0] in self.dep_dic.keys():
                        namelist = self.dep_dic[department[0]]
                        if department[1] not in namelist:
                            namelist.append(department[1])
                            dtemp = {department[0]:namelist}
                            self.dep_dic.update(dtemp)
                    else:
                        dtemp = {department[0].strip():[department[1].strip()]}
                        self.dep_dic.update(dtemp)
        #删除姓名在前，部门在后的字典项
        for name in self.del_list:
            del self.dep_dic[name]
        #加入未检索到的部门
        self.dep_dic.update(self.add_dic)
        #根据字典进行匹配
        for i in range(news_index.shape[0]):
            department = news_index.loc[i, 'department']
            title = self.title_process(news_index.loc[i, 'title'])
            if department.find('信息中心') != -1:
                news_index.loc[i, 'department'] = '信息中心' #信息中心单独处理
            elif department.find('朱立禄') != -1:
                news_index.loc[i, 'department'] = '所长办公室' #朱立禄单独处理
            else:
                department = department.replace('\\', ' ')
                department = department.replace('，', ' ')
                department = department.replace('：', ' ')
                department = department.split()
                for j in range(len(department)):
                    #在字典key中找到部门
                    if department[j] in self.dep_dic.keys():
                        news_index.loc[i, 'department'] = department[j] 
                        break
                    #在字典key中未找到部门
                    else: 
                        for key in self.dep_dic:
                            namelist = self.dep_dic[key]
                            if department[j].find(key) != -1: #针对部门姓名间没有空格
                                news_index.loc[i, 'department'] = key 
                                break
                            elif department[j] in namelist: #通过姓名匹配部门
                                news_index.loc[i, 'department'] = key
                                break
                            elif title.find(key) != -1: #在标题中匹配部门名称
                                news_index.loc[i, 'department'] = key
                                break
                        continue
                    break
            #匹配后进行部门名称规范化
            news_index.loc[i, 'department'] = self.dep_norm_process(news_index.loc[i, 'department'])
            print('\r第' + str(i+1) + '条已处理', end='', flush=True)
        #空项填入其他
        news_index_correct = news_index.fillna('其他')
        return news_index_correct