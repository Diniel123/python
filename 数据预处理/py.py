import csv
import pandas as pd  
import os  
import re
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import seaborn as sn
from pyecharts.charts import Map,Timeline
from pyecharts import options as opts  # 导入options模块
import random

myprovince_name = '江苏省'         #可以随意更改
myschool_name = '(10285)苏州大学'  #可以随意更改
# 设定文件夹路径  
folder_path = 'E:\\python\\2.1程序\\爬虫\\研招网\\数据预处理'  #需要替换为爬取的CSV文件所在的文件夹路径  
path = 'E:\\python\\2.1程序\\爬虫\\研招网\\查询招生信息.csv'   #需要替换为本人电脑的位置，注:此位置千万不要跟上一个位置一样，不然会报错
#获取文件夹下的所有csv文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]#可以得到有几个文件
#创建一个空的存储数据
all_data = pd.DataFrame()
# 循环读取每个CSV文件并追加到总数据中  
data_file = []  #文件的内容和文件的总行数
data_len = []   #每个文件的行数

province = []
num = []
school = []
department =[]
def get_file():
    #扫描文件夹
    for file in csv_files:  
        df = pd.read_csv(os.path.join(folder_path, file))
        a = f"{len(df)}"  # 打印每个文件的行数
        data_len.append(a)
        for i in range(len(df)):      
            data_file.append(df[i:i+1])
# print(data_len[1])
#print(len(data_file))#40

def get_data():
##提取数据
    data_two = []
    ######这部分为优化代码(无视物理伤害)
    for i in range(len(data_file)):
        data_one = data_file[i]
            # 将新内容追加到文件末尾  
                # 打开CSV文件并读取其内容  
        data_two.append(data_one.to_dict())   #变换
    
    sum_num = 0
    for file_num in range(len(csv_files)):
        for data_num in range(int(data_len[file_num])):        
            num_str = data_two[sum_num]['拟招生人数'][data_num]
            match = re.search(r'\d+', num_str)  #表示数字
            if match:
                num_str = match.group()
                num.append(int(num_str))      #提取出了招生人数
                # print(num) 
            province.append(str(data_two[sum_num]['省份'][data_num]))
            # print(province)
            school.append(str(data_two[sum_num]['学校'][data_num].strip()))
            # print(school)
            department.append(str(data_two[sum_num]['院系所'][data_num].strip()))
            # print(department)
            sum_num = sum_num+1


    '''
    这部分是未优化的代码
    '''
    # for i in range(len(data_file)):
    #     data_one = data_file[i]
    #         # 将新内容追加到文件末尾  
    #             # 打开CSV文件并读取其内容  
    #     data_two = data_one.to_dict()   #变换
    #     # print(data_two)
    #     if i< int(data_len[0]):
    #         num_str = data_two['拟招生人数'][i]
    #         match = re.search(r'\d+', num_str)  #表示数字
    #         if match:
    #             num_str = match.group()
    #             num.append(int(num_str))      #提取出了招生人数
    #             #print(num) 
    #         province.append(str(data_two['省份'][i]))
    #         # print(province)
    #         school.append(str(data_two['学校'][i].strip()))
    #         # print(school)
    #         department.append(str(data_two['院系所'][i].strip()))
    #         # print(department)

    #     elif i< (int(data_len[1])+int(data_len[0])) and i> int(data_len[0]):
    #         star_num = i- int(data_len[0])
    #         num_str = data_two['拟招生人数'][star_num]
    #         match = re.search(r'\d+', num_str)  #表示数字
    #         if match:
    #             num_str = match.group()
    #             num.append(int(num_str))      #提取出了招生人数
    #             # print(num) 
    #         province.append(data_two['省份'][star_num]) 
    #     #     print(data_two['省份'][star_num])
    #         school.append(data_two['学校'][star_num].strip())
    #     #     print(data_two['学校'][star_num].strip())
    #         department.append(data_two['院系所'][star_num].strip())
    #     #     print(data_two['院系所'][star_num].strip())

    #     elif i< (int(data_len[1])+int(data_len[0])+int(data_len[1])) and i> (int(data_len[1])+int(data_len[0])):
    #         star_num = i- (int(data_len[1])+int(data_len[0]))
    #         num_str = data_two['拟招生人数'][star_num]
    #         match = re.search(r'\d+', num_str)  #表示数字
    #         if match:
    #             num_str = match.group()
    #             num.append(int(num_str))      #提取出了招生人数
    #             # print(num) 
    #         province.append(data_two['省份'][star_num]) 
    #         # print(data_two['省份'][star_num])  
    #         school.append(data_two['学校'][star_num].strip())
    #         # print(data_two['学校'][star_num].strip())
    #         department.append(data_two['院系所'][star_num].strip())
    #         # print(data_two['院系所'][star_num].strip())
    # print('人数:',num)
    # print('省市:',province)
    print('学校:',school)
    # print('学院:',department)    
'''
处理后文件的保存
'''
def keep_data():
    with open(path, 'w',newline='',encoding='utf_8_sig') as file:    #newline=''出去中间的空行
        writer = csv.writer(file)
        writer.writerow(['省份','学校','院系所','招生人数'])
        # 对元组进行迭代，并将每个元素作为一个单独的行写入
        for item1,item2,item3,item4 in zip(province,school,department,num):
            # writerow需要一个列表作为参数，所以我们把元素放在一个列表中
            writer.writerow([item1,item2,item3,item4])

    '''
    计算每个省收这个专业一共多少
    这部分也可以优化
    '''
province_count = []  #有多少的省
province_name  = []  #每个省的名字
province_num = [] #每个省收多少个人

# 地图
def get_map(province,num):
        provice = list(province)
        values = list(num)
        china_map = [          #这部分是伪代码，主要目的 填补缺失值
        '安徽省', 
        '山东省',
        '广西壮族自治区',
        '海南省',
        '重庆市',
        '青海省',
        '宁夏回族自治区',
        '新疆维吾尔自治区',
        '西藏自治区',
        ]
        for i in range(len(china_map)):
            supplement = random.randint(100, 300)
            provice.append(china_map[i])
            values.append(supplement)
        map_ = Map()
        map_.add("", [list(z) for z in zip(provice, values)], maptype="china", zoom=1)
        map_.set_global_opts(

            title_opts=opts.TitleOpts(title="各省研究生招生人数",
                                    subtitle="数据来源：研招网",
                                    pos_right="center",
                                    pos_top="5%"),
                                    
            visualmap_opts=opts.VisualMapOpts(max_=500,
                                              min_=0,
             	                       range_color=["#E0ECF8", "#045FB4"]
                                            ),
            )

        # 打开html
        map_.render("E:/python/2.1程序/爬虫/研招网/数据预处理/results/render.html", width=2000, height=1200)



def data_province():

    #判断省份中相同的数据
    # 使用Counter类统计每个元素出现的次数
    counter = Counter(province)

    # 打印结果
    for item, count in counter.items():
        province_count.append(count)   
        province_name.append(item)

    '''
    优化的部分（万能小代码）
    '''
    for i in range(len(province_name)):
        province_num.append(0) 

    #循环处理  先循环有多少个省   再循环每个省有多少的数
    #定义变量
    data_row_num = 0      #数据第几行
    for i in range(len(province_name)):
        sum = 0
        for j in range(province_count[i]):
            #表格中的人数
            sum = num[data_row_num]+sum  #对sum进行求和
            province_num[i] = sum
            data_row_num = data_row_num + 1  

    #画表        province_num 里面存的所有省的数   province_name  里面是所有的省  根据这两个元组就可以画出表格  
    plt.rcParams['axes.unicode_minus'] = False  # 加入这条语句解决负号乱码问题
    plt.rcParams['font.family'] = 'FangSong'  # 加入这条语句解决中文乱码问题
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.title('每个省收的人数')
    # 绘制柱状图
    plt.bar(province_name, province_num)
    for i in range(len(province_name)):
        plt.text(province_name[i], province_num[i]+1, str(province_num[i]), ha='center')

    plt.show()

    get_map(province_name,province_num)
    '''
    未优化的部分
    '''
    #数据求和
    # 计算前三个数的和
    # province_num[0] = sum(num[:province_count[0]])
    # province_num[1] = sum(num[province_count[0]:province_count[1]+province_count[0]])
    # province_num[2] = sum(num[province_count[1]+province_count[0]:])
    # print(province_name)
    # # 创建一个直方图  
    # plt.hist(province_num, bins=10, orientation='vertical')  
    # # 设置图表标题和轴标签  
    # plt.title('省份统计')  
    # plt.xlabel('Data')  
    # plt.show()
'''
计算出来每个省中每个学校收多少人
理解部分可以参考上面的
这部分也可以优化

这部分有个bug：自动检索搜索不到
'''
school_count = []
school_name  = []
school_num = []


#检索出这个省在元组中的所有位置
def find_all_positions(char, tuple):  
    positions = []  
    for i in range(len(tuple)):  
        if tuple[i] == char:  
            positions.append(i)  
    return positions  
def data_school():
    # a = input('请输入你要查询的省份：')
    # print(a)
    # # 查找元素在列表中的位置 
    # if a in province_name:  
    #     position = province_name.index(a)  
    #     print("该省份在列表中的位置是: ", position)  
    # else:  
    #     print("未找到该省份") 
    # position = province.index(a)
    # print("该省份在列表中的位置是: ", position)
    new_school = []
    new_num = []   
    try:
        school_positions =find_all_positions(myprovince_name, province)#这个省中的学校在所有中的位置
        for i in range(len(school_positions)):
            new_school.append(school[school_positions[i]])#这个省中学校的名字  
            new_num.append(num[school_positions[i]])
        '''
        先找到这个省所有的数据
        出这个省中学校 new_school 和人数 new_num ，放在另外一个文件夹中
        在提取出来的学校中找出相同的学校
        找出重复学校的位置school_count
        过滤后学校的名字
        '''    
        #判断学校中相同的数据
        # 使用Counter类统计每个元素出现的次数     
        counter = Counter(new_school)   
        # 打印结果
        for item, count in counter.items():
            school_count.append(count)         #学校的位置
            school_name.append(item)            #过滤后学校的名字

        '''
        优化部分
        '''
        for i in range(len(school_name)):
            school_num.append(0)    
  
        
        #循环处理  先循环有多少个学校   再循环每个学校有多少的数
        #定义变量
        data_row_num = 0      #数据第几行
        for i in range(len(school_name)):
            sum = 0
            for j in range(school_count[i]):
                #表格中的人数
                sum = new_num[data_row_num]+sum  #对sum进行求和
                school_num[i] = sum
                data_row_num = data_row_num + 1    
    except:
           print('未找到该省份或者省份输入错误')
    # print(school_name)
    # print(school_num)
    #画图表  school_num 每个学校收的人数   school_name  学校的名字    根据这两个元组可以画出图形
    plt.rcParams['axes.unicode_minus'] = False  # 加入这条语句解决负号乱码问题
    plt.rcParams['font.family'] = 'FangSong'  # 加入这条语句解决中文乱码问题
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.title(myprovince_name+'每个学校收的人数')
 
    # 绘制饼状图

    plt.pie(school_num, labels=school_name, autopct='%1.1f%%')
    plt.show()
   # 绘制柱状图
    plt.title(myprovince_name+'每个学校收的人数')
    plt.bar(school_name, school_num)
    for i in range(len(school_name)):
        plt.text(school_name[i], school_num[i]+1, str(school_num[i]), ha='center')

    plt.show()



'''
未优化部分
'''
    # school_num[0] = sum(new_num[:school_count[0]])  #
    # school_num[1] = sum(new_num[school_count[0]:(school_count[0]+school_count[1])])#
    # school_num[2] = sum(new_num[(school_count[0]+school_count[1]):(school_count[0]+school_count[1]+school_count[2])])
    # print(school_num)
    # print(school_name)
    # print(school_num)
    # print(school_count)
    # counter = Counter(school)
    #      # 打印结果
    # for item, count in counter.items():
    #     school_count.append(count)
    #     school_name.append(item)
    # print(school_count)
    # print(school_name)
#对每个学校的专业进行处理
department_count = []
department_name = []
department_num = []

def data_department():
    new_department = []
    new_department_num = []
    try:
        department_positions =find_all_positions(myschool_name, school)#这个省中的学校在所有中的位置
        for i in range(len(department_positions)):
            new_department.append(department[department_positions[i]])#这个省中学校的名字  
            new_department_num.append(num[department_positions[i]])  
        # 使用Counter类统计每个元素出现的次数     
        counter = Counter(new_department)   
        
        # 打印结果
        for item, count in counter.items():
            department_count.append(count)         #学校的位置
            department_name.append(item)            #过滤后学校的名字
        for i in range(len(department_name)):
            department_num.append(0)    
  
        
        #循环处理  先循环有多少个学校   再循环每个学校有多少的数
        #定义变量
        data_row_num = 0      #数据第几行
        for i in range(len(department_name)):
            sum = 0
            for j in range(department_count[i]):
                #表格中的人数
                sum = new_department_num[data_row_num]+sum  #对sum进行求和
                department_num[i] = sum
                data_row_num = data_row_num + 1    
        print(department_name)       
        print(department_num) 
    except:
           print('未找到该学校或者学校输入错误')
     #画图   department_name 学院的名字   department_num 每个学院收多少人
     
    plt.rcParams['axes.unicode_minus'] = False  # 加入这条语句解决负号乱码问题
    plt.rcParams['font.family'] = 'FangSong'  # 加入这条语句解决中文乱码问题
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.title(myschool_name+'每个学院收的人数')
    # 绘制柱状图
    plt.bar(department_name, department_num)
    for i in range(len(department_name)):
        plt.text(department_name[i], department_num[i]+1, str(department_num[i]), ha='center')

    plt.show()



if __name__ == '__main__':
        get_file()
        get_data()
        # keep_data()
        data_province()
        data_school()
        data_department()
        #自主定义各省份的数据
        #E:/python/2.1程序/爬虫/研招网/数据预处理/results




