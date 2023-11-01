import requests
'''requests可以模拟浏览器的请求'''
from bs4 import BeautifulSoup   #网页解析库，可以从 HTML 或 XML 文件中提取数据
'''
BeautifulSoup
从HTML或XML文件中提取数据的Python库.
它能够通过你喜欢的转换器实现惯用的文档导航,
查找、修改文档的方式
''' 
from pandas.core.frame import DataFrame
import re   #正则表达式
import time
import pandas as pd
import csv

# # df = pd.read_csv('E:\\python\\2.1程序\\爬虫\\研招网\\数据预处理\\查询招生信息.csv')  
path = "E:\\python\\2.1程序\\爬虫\\研招网\\数据预处理\\查询招生信息.csv"
# with open('E:\\python\\2.1程序\\爬虫\\研招网\\数据预处理\\查询招生信息.csv','w',encoding='utf_8_sig',newline='') as f :
#         columns = ['学校', '考试方式', '院系所','专业',
#                         '学习方式', '研究方向', '指导教师', '拟招生人数']
#         writer = csv.writer(f)
#         writer.writerow(columns)  #添加表头

class Graduate:
    def __init__(self, province, category, provinceName):
        self.head = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKi"
            "t/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }
        self.data = []
        self.province = province   #省份
        self.category = category   #类别
        self.provinceName = provinceName   #省份名称

    def get_list_fun(self, url, name):
        """获取提交表单代码"""
        response = requests.get(url, headers=self.head)
        resprovince = response.json()
        with open(name + ".txt", "w") as f:
            for x in resprovince:
                f.write(str(x))
                f.write("\n")

    def get_list(self):
        """
        分别获取省，学科门类，专业编号数据
        写入txt文件
        """
        self.get_list_fun("http://yz.chsi.com.cn/zsml/pages/getSs.jsp",
                          "province")
        self.get_list_fun('http://yz.chsi.com.cn/zsml/pages/getMl.jsp',
                          "category")
        self.get_list_fun('http://yz.chsi.com.cn/zsml/pages/getZy.jsp',
                          'major')

    def get_school_url(self):
        """
        输入省份，
        发送post请求，获取数据
        提取数据
        必填省份，学科门类，专业可选填
        返回学校网址
        """
        url = "https://yz.chsi.com.cn/zsml/queryAction.do"
        data = {
            "ssdm": self.province,      #请求体
            "yjxkdm": self.category,
        }
        response = requests.post(url, data=data, headers=self.head)    #发送请求.获取数据
        html = response.text 
        #print(html) 
        ''' 
        text相当于响应体内容
        #请求成功后，返回HTML代码  响应状态码、响应头和响应体等 正文数据在响应体中
        当Python访问网站成功后，我们查看它的text属性，
        我们看到的是网页的 HTML 代码.

        服务器返回响应的正文数据都在响应体中。
        响应体=网页的 HTML 代码
        调用text属性相当于人工访问网页时的查看【网页源代码】。
        '''
        reg = re.compile(r'(<tr>.*? </tr>)', re.S)  #  匹配模式 符号“.*?”非贪婪匹配：只要遇到以a为开始以b为结束就匹配
        '''
        re.S单行匹配
        使用 compile 函数将正则表达式的字符串形式编译为一个 Pattern 对象
        通过 Pattern 对象提供的一系列方法对文本进行匹配查找，获得匹配结果（一个 Match 对象）
        最后使用 Match 对象提供的属性和方法获得信息，根据需要进行其他的操作
        compile()与findall()一起使用，返回一个列表。
        '''
        #print('*************************************')
        
        content = re.findall(reg, html)
        #print(content)
        schools_url = re.findall('<a href="(.*?)" target="_blank">.*?</a>',   
                                 str(content))
        '''
        <a href="(.*?)" target="_blank">.*?</a>
        <a 到 /a>之间的所有内容  匹配content中所有链接地址
        '''
        #print(schools_url)
        return schools_url

    def get_college_data(self, url):
        """返回一个学校所有学院数据"""
        response = requests.get(url, headers=self.head)
        html = response.text
        #print(html)
        colleges_url = re.findall(
            '<td class="ch-table-center"><a href="(.*?)" target="_blank">查看</a>',
            html)
        '''
        数据都在td class="ch-table-center下，在这个之下，遍历html取出所有的数据链接 
        '''
        #print('*****************************')
        # print(colleges_url)
        return colleges_url

    def get_final_data(self, url):
        """输出一个学校一个学院一个专业的数据"""
        temp = []
        response = requests.get(url, headers=self.head)  #获取该网页下的内容
        html = response.text                             #获取数据文本
        soup = BeautifulSoup(html, features='lxml')      #利用lxml规则解析html
        #print(soup)
        summary = soup.find_all('td', {"class": "zsml-summary"})  #zsml-summary指 属性 （内容）
        for x in summary:
            temp.append(x.get_text())  #获取标签的文字内容，append() 函数可以向列表末尾添加「任意类型」的元素
        self.data.append(temp)

    def get_schools_data(self):
        """获取所有学校的数据"""
        url = "http://yz.chsi.com.cn"
        schools_url = self.get_school_url()
        amount = len(schools_url)
        i = 0
        for school_url in schools_url:
            i += 1
            url_ = url + school_url
            # 找到一个学校对应所有满足学院网址
            colleges_url = self.get_college_data(url_)
            print("已完成" + self.provinceName + "第" + str(i) + "/" +
                  str(amount) + "个高校爬取")
            #time.sleep(1)
            for college_url in colleges_url:
                _url = url + college_url
                self.get_final_data(_url)
        time.sleep(1) # 延迟时间30s  
    '''
    爬取的数据存储在self.data中
    写入文件，不覆盖原有文件
    '''      
    def get_data_frame(self):
        """将列表形数据转化为数据框格式"""


        columns = ['学校', '考试方式', '院系所', '专业', 
                        '学习方式', '研究方向', '指导教师', '拟招生人数']

        data = pd.DataFrame(self.data,columns=columns)
        data.insert(0,'省份',self.provinceName)
        # print(data)

        # #data.drop(labels='', axis=1, inplace=True)
        data.to_csv('E:\\python\\2.1程序\\爬虫\\研招网\\数据预处理\\'+self.provinceName + "查询招生信息.csv", encoding="utf_8_sig",index=False)

        # data.insert(0,'省份',self.provincName)         #添加第一行省份
        #data.drop(labels='', axis=1, inplace=True)
        ##data.to_csv("E:\\python\\2.1程序\\爬虫\\研招网\\数据预处理\\查询招生信息.csv", encoding="utf_8_sig",index=False)#utf-8-sig 需要提供BOM。带有签名的 utf-8  self.provinceName + 
        # 打开CSV文件并读取其内容  
        # with open(path, 'r',encoding='utf_8_sig') as file:  
        #     reader = csv.reader(file)  
        #     lines = list(reader)  
               
        # # 将新内容追加到文件末尾  
        # new_content = data
        # lines.append(new_content)  
        
        # # 将新内容写入CSV文件并保存  
        # with open(path, 'w', newline='',encoding='utf_8_sig') as file:  
        #     writer = csv.writer(file)  
        #     writer.writerows(lines)

if __name__ == '__main__':
    provinceList = [
        '11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33', '35',
        '36', '41', '42', '43', '44', '51', '52', '53', '61', '62'
    ] # 要抓取的省份代码
    '''
         安徽 
         山东
        '45': '广西壮族自治区',
        '46': '海南省',
        '50': '重庆市'
        '54': '西藏自治区',
        '63': '青海省',
        '64': '宁夏回族自治区',
        '65': '新疆维吾尔自治区',
        '71': '台湾省',
        '81': '香港特别行政区',
        '82': '澳门特别行政区'
    '''


    provinceNmaeDict = {
         '11': '北京市',
         '12': '天津市',
         '13': '河北省',
         '14': '山西省',
         '15': '内蒙古自治区',
         '21': '辽宁省',
         '22': '吉林省',
         '23': '黑龙江省',
         '31': '上海市',
         '32': '江苏省',
         '33': '浙江省',
         '34': '安徽省',
         '35': '福建省',
         '36': '江西省',
         '37': '山东省',
         '41': '河南省',
         '42': '湖北省',
         '43': '湖南省',
        '44': '广东省',
        '45': '广西壮族自治区',
        '46': '海南省',
        '50': '重庆市',
        '51': '四川省',
        '52': '贵州省',
        '53': '云南省',
        '54': '西藏自治区',
        '61': '陕西省',
        '62': '甘肃省',
        '63': '青海省',
        '64': '宁夏回族自治区',
        '65': '新疆维吾尔自治区',
        '71': '台湾省',
        '81': '香港特别行政区',
        '82': '澳门特别行政区'
    } #省份代码和对应的省份名称
    category = "085406" #专业代码
    for i in provinceList:
        province = i
        if province in provinceNmaeDict.keys():
            spyder = Graduate(province, category, provinceNmaeDict[province])
            spyder.get_schools_data()
            spyder.get_data_frame()
