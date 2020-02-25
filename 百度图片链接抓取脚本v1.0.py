from urllib.request import urlretrieve,quote,unquote
import requests
import time
import random
import os
from lxml import etree
from fake_useragent import UserAgent


file_name_list = [] # 存储所有文件的名称
downloader_url_list = []  # 存储所有文件的下载链接


# 请求并提取文件的下载链接
def spider_url():
    global downloader_url_list  # 设置变量为全局变量
    # 通过键盘录入要搜索的关键字，例如:汽车
    KeyWord=quote(input("请输入要搜索的关键字，例如:汽车\n"))
    print("你要搜索的关键字为：",unquote(KeyWord))
    
    #通过键盘录入需要采集的总页数,每页30条数据
    page_num=int(input("请输入需要采集的总页数："))
    print("你输入的总页数为：",page_num)

    print("开始提取文件的下载连接,请稍等......\n")

    for page in range(1,page_num+1):
        try:
            # 请求每页的url
            r = requests.get("https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord="+KeyWord+"&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word="+KeyWord+"&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&pn="+str(page*30)+"&rn=30&gsm=&"+str(int(time.time()*1000))+"=", headers={'user-agent': UserAgent().random}).json()
            downloader_url_list.extend([r["data"][i]["middleURL"] for i in range(30)])  # 提取并存储每页所有文件的下载链接
            file_name_list.extend([unquote(KeyWord) + '_' + '.'.join(url.split('/')[-1].split('.')[0:-1]) for url in downloader_url_list])   # 随机生成每个文件的名称并存入列表s
        except Exception as e:
            print("出现错误,错误如下：", e)
            continue
        time.sleep(random.uniform(0, 2))  # 设置随机休眠时间
    print("文件的下载连接提取完毕！\n", "-" * 185,downloader_url_list,"\n", "-" * 185)


# 将文件名称和链接存入指定的txt文本内。
def save_name_link():
    print("开始保存文件名称和链接,请稍等......\n")
    if os.path.exists(filePath + '文件链接.txt'):  # 如果该路径（文件）已存在，则删除该路径（文件）。
        os.remove(filePath + '文件链接.txt')
    with open(filePath + '文件链接.txt', 'a+', encoding='utf-8')as f:  # 将文件名称和链接存入指定的txt文本内。
        for i in range(len(downloader_url_list)):
            try:
                f.write("%s;%s\n" % (file_name_list[i], downloader_url_list[i]))
                print("已保存：%s" % file_name_list[i])
            except Exception as e:
                print("出现错误,错误如下：", e)
                continue
        print("全部保存完毕!")


# 显示下载进度
def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''

    totalsize_MB = totalsize / 1024 / 1024  # 目标文件大小，单位：MB。
    complete_MB = (blocknum * blocksize) / 1024 / 1024  # complete意思：完成；单位：MB。
    Surplus_MB = totalsize_MB - complete_MB  # Surplus意思：剩余；单位：MB。

    percent = 100.0 * blocknum * blocksize / totalsize
    if percent >= 100 and complete_MB >=totalsize_MB:
        percent = 100
        complete_MB = totalsize_MB
        Surplus_MB = 0
    print("| 下载进度：%.2f%% | 已下载：%.3fMB | 剩余：%.3fMB | 文件总共：%.3fMB |" % (percent, complete_MB, Surplus_MB, totalsize_MB))
    print("-" * 75)


# 从变量中读取文件名称和链接，下载文件。
def downloader():
    print("开始下载文件,请稍等......\n")
    for i in range(len(downloader_url_list)):
        try:
            Suffix_name = downloader_url_list[i].split(".")[-1]  # 从文件链接中提取文件后缀名(Suffix name)
            temporary_file_name = filePath + file_name_list[i] + '.file'  # 创建临时文件名
            Final_file_name = filePath + file_name_list[i] + '.' + Suffix_name  # 创建最终的文件名

            if os.path.exists(Final_file_name):  # 如果该路径（文件）已存在，则跳过执行下一个。
                continue
            print("正在下载文件：%s.%s" % (file_name_list[i],Suffix_name))
            urlretrieve(downloader_url_list[i], filename=temporary_file_name, reporthook=callbackfunc)  # 开始下载,将文件的后缀名临时设为".file"
            os.rename(temporary_file_name, Final_file_name)  # 每下载完成一个文件，将文件的临时后缀名重命名为文件原本的后缀名
        except Exception as e:
            print("出现错误,错误如下：", e)
            continue
        print("-" * 185)
        time.sleep(random.uniform(0, 2))  # 设置随机休眠时间
    print("全部下载完成!")


# 从指定的txt文本内读取文件名称和链接，下载文件。
def downloader_1(start_num, end_num):
    """
    @start_num:下载范围的最小值
    @end_num:下载范围的最大值
    """
    print("开始下载文件,请稍等......\n")
    with open(filePath + '文件链接.txt', 'r', encoding='utf-8')as f:  # 从指定的txt文本内读取文件名称和链接。
        row = f.readlines()  # readlines()读取整个文件所有行，保存在一个列表(list)变量中，每行作为一个元素。
    for i in range(start_num, end_num):
        try:
            file_name = row[i].strip("\n").split(";")[0]  # 提取文件名
            file_link = row[i].strip("\n").split(";")[1]  # 提取文件链接
            Suffix_name = file_link.split(".")[-1]  # 从文件链接中提取文件后缀名(Suffix name)

            temporary_file_name = filePath + file_name + '.file'  # 创建临时文件名
            Final_file_name = filePath + file_name + '.' + Suffix_name  # 创建最终的文件名
            if os.path.exists(Final_file_name):  # 如果该路径（文件）已存在，则跳过执行下一个。
                continue
            print("正在下载文件：%s.%s" % (file_name,Suffix_name))
            urlretrieve(file_link, filename=temporary_file_name, reporthook=callbackfunc)  # 开始下载,将文件的后缀名临时设为".file"
            os.rename(temporary_file_name, Final_file_name)  # 每下载完成一个文件，将文件的临时后缀名重命名为文件原本的后缀名
        except Exception as e:
            print("出现错误,错误如下：", e)
            continue
        print("-" * 185)
        time.sleep(random.uniform(0, 2))  # 设置随机休眠时间
    print("全部下载完成!")


if __name__ == "__main__":
    filePath = "F:\\百度图片\\"  # 文件存储路径

    a=time.time()       
    spider_url()     # 请求并提取文件名称和下载链接
    e=time.time()  
    print("提取链接总耗时%.2f秒"% (e-a))
    print("-"*185)  

    a=time.time()       
    save_name_link()    # 将文件名称和链接存入指定的txt文本内。
    e=time.time()  
    print("保存文件链接总耗时%.2f秒"% (e-a))
    print("-"*185)

    # a=time.time()       
    # downloader()    #从变量中读取文件名称和链接，下载全部文件。
    # e=time.time()  
    # print("下载_总耗时%.2f秒"% (e-a))
    # print("-"*185)

    a = time.time()
    downloader_1(0, 60)  # 从指定的txt文本内读取文件名称和链接，下载文件(可指定范围，范围最大数为文本内的总行数)。
    e = time.time()
    print("下载_1总耗时%.2f秒" % (e - a))
    print("-" * 185)
    # 下载完成后，自动关闭电脑
    # os.system('shutdown /s /t 10')
    