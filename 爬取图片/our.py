import requests
from bs4 import BeautifulSoup  #解析器
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
'''
步骤:发送请求
     获取响应内容
     解析内容
     保存结果
'''

def dl_page(url):
    res = requests.get(url, headers=headers, proxies=proxies)
    res.encoding = "gbk"     #用于指定从请求中获取的文本的编码方式,防止乱码
    main_page = BeautifulSoup(res.text, "html.parser")
    print(main_page)
    main_url = main_page.find("ul", attrs={"class": "clearfix"})
    print(main_url)
    alist = main_url.find_all("a")
    url_ = "https://pic.netbian.com"     #网站整体的网址
    for a in alist:
        href = a.get("href")
        url_real = url_ + href
        resp = requests.get(url_real, headers=headers, proxies=proxies)
        resp.encoding = "gbk"
        child_page = BeautifulSoup(resp.text, "html.parser")
        img_page = child_page.find("a", attrs={"id": "img"})
        print('page:',img_page)
        img = img_page.find("img")
        print('img:',img)
        src = img.get("src")
        print('src:',src)
        src_real = url_ + src
        img_res = requests.get(src_real)
        print('src_real:',src_real)
        img_name = src.split("/")[-1]  # 拿到最后一个杠后面的内容
        print('name',img_name)
        with open("E:/python/2.1程序/爬虫/1.1图片爬取/2.1提取网站图片/img/" + img_name, mode="wb") as f:
            f.write(img_res.content)  # 括号内内容为字节，不能打印
        print("over", img_name)
        time.sleep(1)
    print("提取完毕")

'''
 "referer": "https://pic.netbian.com/4kmeinv/index.html",
  "cookie": "__yjs_duid=1_c427763b6a77b795723fe580805d86f41635746735356; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1635749214,1636550738,1636550843; zkhanecookieclassrecord=%2C54%2C; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1635746736,1636550853,1636557267,1636606416; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1636606416; yjs_js_security_passport=d0fe81024fb5a59de630df3fb7dd52134fe3a84c_1636606550_js"
'''
#
if __name__ == '__main__':

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
    }
    proxies = {
        "http": "http://113.125.156.47:8888"
    }
    url = "https://pic.netbian.com"    #https://pic.netbian.com/4kmeinv/index.html   某一部分的网址
##################################################################################

#########################################################################

    # dl_page(url)
    #     # for i in range(2,148):#此效率会极其低下
    #     #     dl_page(f"https://pic.netbian.com/4kmeinv/index_{i}.html")
    with ThreadPoolExecutor(10) as t:
        for i in range(1, 15):
            t.submit(dl_page, f"https://pic.netbian.com/4kmeinv/index_{i}.html")  #不一样 风景

    print("全部下载完毕！！！")


