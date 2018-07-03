import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parsePage(productList, html):
    try:
        product = re.findall(r'\"raw_title\"\:\".*?\"', html)
        price = re.findall(r'\"view_price\"\:\"[\d\.]*"', html)
        for i in range(len(product)):
            product1 = eval(product[i].split(':')[1])
            price1 = eval(price[i].split(':')[1])
            productList.append([product1, price1])
    except:
        return ""

def printProduct(productList, num):
    formatList = "{:^4}\t{:^8}\t{:^16}"
    print(formatList.format("序号","价格","商品名称"))
    for i in range(num):
        print(formatList.format(i + 1, productList[i][1], productList[i][0]))

def main():
    productList = []
    product = "芬迪小怪兽"
    num = 20
    url = "https://s.taobao.com/search?q=" + product
    html = getHTMLText(url)
    parsePage(productList, html)
    printProduct(productList, num)

main()
