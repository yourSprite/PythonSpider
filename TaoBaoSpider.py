import requests
import re

def getHTMLTest(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parsePage(ilt, html):
    try:
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price,title])
    except:
        print("")

def printGoodList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "商品名称", "价格"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count,g[0], g[1]))

def main():
    goods = '芬迪小怪兽'
    depth = 2
    start_url = "https://s.taobao.com/search?q=" + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLTest(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodList(infoList)

main()
