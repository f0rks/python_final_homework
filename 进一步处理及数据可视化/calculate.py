import pandas as pd

# # 读取部门类
df = pd.read_excel('E:/1111/news_index.xlsx', usecols=[2] + [3])
df_1 = df.department.unique()
# print(len(df_1))

# 生成以周为单位的时间点
week_time = pd.date_range('20160926 00:00', periods=163, freq='7D')

n = 0
m = 0
line = 999
for i in range(162):
    a = str(week_time[i]).replace('-', '')
    a = str(a).replace('00:00:00', '').strip()
    # print(a)
    b = str(week_time[i + 1]).replace('-', '')
    b = str(b).replace('00:00:00', '').strip()#replace()
    # print(b)
    for j in range(line, 0, -1):
        # print(j)
        c = str(df.iloc[j, 1])
        c = c.replace('-', '')
        # print(c)
        n = j
        for k in range(line, 0, -1):
            d = str(df.iloc[k, 1])
            d = d.replace('-', '')
            if d >= b:
                m = k
                count = {}
                # # 遍历字符串
                for l in df.iloc[m:n, 0]:
                    # 第一次查询到，计数：1
                    if l not in count:
                        count[l] = 1
                    else:  # 再次查询到相同字符，计数+1
                        count[l] += 1
                w_data = pd.DataFrame(count, index=[0])
                if n == 999:
                    result = w_data
                else:
                    result = pd.concat([result, w_data], sort=True)
                line = m
                break
        break
result = result.reset_index(drop=True)
result = result.fillna(0)
result.to_excel(r'E:\result_dep_1.xlsx', sheet_name='Sheet1')
print('finished')

# 定义空字典
# count = {}
# # 遍历字符串
# for i in df.department[122 : 144]:
#     # 第一次查询到，计数：1
#     if i not in count:
#         count[i] = 1
#     else:  # 再次查询到相同字符，计数+1
#         count[i] += 1
# print(count)
