from datetime import datetime

from pandas import read_excel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

df1 = read_excel(r'F:\长光所\05研一上\06Python编程基础\大作业\统计_sum.xlsx', sheet_name='sheet1')
plt.rcParams['font.sans-serif'] = ['SimSun']
df1.boxplot(column=['部门总量'],
           sym='o',  # 异常值形式
           vert=True,  # 垂直显示
           whis=1.5,  # IQR
           patch_artist=True,  # 箱子是否填充
           meanline=True,  # 均值线是否显示
           showmeans=True,
           showbox=True,  # 是否显示箱子
           showfliers=True,  # 是否显示异常值
           notch=True,  # 中位数是否有缺口
           return_type='dict'
           )
plt.show()
df2 = read_excel(r'F:\长光所\05研一上\06Python编程基础\大作业\箱型.xlsx', sheet_name='Sheet2')
df2 = df2.fillna(0)
# print(df)
plt.rcParams['font.sans-serif'] = ['SimSun']
df2.boxplot(column=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
           sym='o',  # 异常值形式
           vert=True,  # 垂直显示
           whis=1.5,  # IQR
           patch_artist=True,  # 箱子是否填充
           meanline=True,  # 均值线是否显示
           showmeans=True,
           showbox=True,  # 是否显示箱子
           showfliers=True,  # 是否显示异常值
           notch=True,  # 中位数是否有缺口
           return_type='dict'
           )
plt.show()
