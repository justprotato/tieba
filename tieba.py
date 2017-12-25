import requests
import re
import time
from tool import tool
from threading import Thread

req=requests.Session()
#设置请求头
header={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
'Connection':'keep-alive',
'Cookie':'BAIDUID=D90F9C0824EBD08DCBBB3FF3BD6E89CE:FG=1; BIDUPSID=D90F9C0824EBD08DCBBB3FF3BD6E89CE; PSTM=1511269504; TIEBA_USERTYPE=aa1333212acc532f97140fc4; bdshare_firstime=1511446691824; TIEBAUID=d8f5232b2ee02049f64f66d9; __cfduid=dfc37a551af28e2d9b420134bce08cf331512482598; BDUSS=HVtfjlHd354RFJ0cmNOcnBxaFZsRExpbGlzUUplV1ptMzA5RWkyV3hYczZabEJhQVFBQUFBJCQAAAAAAAAAAAEAAAA9f5KoyMvJ-ru5utyzpDMzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADrZKFo62ShaV; STOKEN=83e41971856dcb9d5da9fbf4e76455c25d148756a856f7968f8ce48fb415a1eb; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1513410991,1513411090,1513677695,1513926774; H_PS_PSSID=1456_21102_17001_25177_20930; PSINO=7; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1513926778,1514086436,1514102077,1514197987; bottleBubble=1; 2828173117_FRSVideoUploadTip=1; wise_device=0; after_vcode=7388f56a1ff97df1a82ddc2a4afe147c411d651b60be5b11f49a426e27db7c016761a9cde0d99b2f027dfe1b1127d8948de0c3436eddd70f40a259e8a3f0297299ad8f14cf17b08fbb44a9a5312db21b0187aad2ab53b3156326f6dfe0eb99c8ebbc3100c3f9d5aeab7526a481ff28f3dececbf75fbccd766a36316cdb4735ae5b54c8d4ef638cd7dade1fe482533637c78cc5e53fe001cb6a70b236999e23423d40254ec72bd406f0e9ea9b6af0efce82a0ea97420f99395ef0c62d42155a2d8716967fb21c403569e1e84303a7660ec8b15e2ae69364dfc3ab7d42e4e9570d62645e76dcdafa24d30c8e6c8f22a134b34afb02c80d7ae3e458d47b36f08744d27ddd79f8fc3553ce2a3f5c75558bb24e129159bc18b96f9fb273f759a390cb1bae24fb34e3204f36881dd0e4452b156bbf85f1ce9541f017b301fac8a8847fb9206d238ecd9ba742e9208994ecf434; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1514205768',
'Host':'tieba.baidu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

#利用正则表达式剔除杂标签
def getContent(page):
    pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
    items = re.findall(pattern, page)
    contents = []
    for item in items:
        content = "\n" + tool.replace(item) + '\n'
        contents.append(content)
    return contents

#写入到文件
def dataToFiles(title,content):
    t="".join(re.split("\/ ",title))
    # t="".join(title.split('/'))
    try:
        with open('./data/{}.txt'.format(t),'w',) as w:
            print(content)
            w.write("".join(content))
    except FileNotFoundError:
        t="NoName"
        with open('./data/{}.txt'.format(t), 'w', ) as w:
            print(content)
            w.write("".join(content))
    return True

#获取页面
def downloadPage(url):
    page=req.get(url=url,headers=header)
    return page.text

#解析页面
def parsePage(page,pattern):
    return re.findall(pattern,page)
#生成下一页
def loadUrl():
    for n in range(173550,202550,50):
        yield "https://tieba.baidu.com/f?kw=%E6%96%97%E9%B1%BCtv&ie=utf-8&pn={}".format(n)
        #https://tieba.baidu.com/f?kw=%E6%96%97%E9%B1%BCtv&ie=utf-8&pn=172600
#获取当前页所有帖子title和帖子URL
def getTitle_Url(utres):
    ut=list()
    for i in utres:
        i=list(i)
        i[0]='https://tieba.baidu.com/p/'+i[0]
        ut.append(i)
    return ut

#当前页获取所有的数据到文件
def getAllData(ut):
    ut=getTitle_Url(ut)
    for u in ut:
        uPage=downloadPage(u[0])
        dataToFiles(u[1],getContent(uPage))
def toThread(u):
    print(u)
    page = downloadPage(u)
    print(page[:20])
    utPattern = re.compile(r'href="/p/(.*?)".*?class="j_th_tit ">(.*?)</a>', re.S)
    utResult = parsePage(page, utPattern)
    print(utResult)
    # print(utResult)
    getAllData(utResult)
    # time.sleep(1)
#爬函数
def Spider():
    threads=[]
    for u in loadUrl():
        t=Thread(target=toThread,args=[u])
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__=='__main__':
    Spider()
