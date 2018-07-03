import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parsePage(productList, html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        productName = soup.find_all(class_="p-name p-name-type-2")
        productPrice = soup.find_all(class_="p-price")
        for i in range(len(productName)):
            productName2 = productName[i].find('em').text
            productPrice2 = productPrice[i].find('i').text
            productList.append([productName2, productPrice2])
    except:
        return ""

def printProduct(productList, num):
    tplt = "{0:^5}\t{1:{3}<50}\t{2:>10}"
    print(tplt.format("序号", "产品名称", "价格", chr(12288)))
    for i in range(num):
        print(tplt.format(i + 1, productList[i][0], productList[i][1], chr(12288)))

def main():
    searchProduct = "macbookpro"
    url = "http://search.jd.com/Search?keyword=macbook&enc=utf-8&wq=" + searchProduct
    productList = []
    num = 20
    html = getHTMLText(url)
    parsePage(productList, html)
    printProduct(productList, num)

main()
