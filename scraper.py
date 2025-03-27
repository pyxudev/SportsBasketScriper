import urllib.request
from bs4 import BeautifulSoup

itemId = 0

def getsoup(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getdetails(soup):
    global itemId
    res = ''
    lis = soup.select('#main-list > li')
    for li in lis:
        detail_keys = li.select('.clearfix > dt')
        detail_values = li.select('.clearfix > dd')
        itemId += 1
        res += str(itemId) + '\n'
        for i in range(0, len(detail_keys)-1):
            res += detail_keys[i].text + ': ' + detail_values[i].text + '\n'
    return res

kw = input('検索キーワードを入力してください：')
url_base = 'https://www.net-menber.com/list/baske/index.html?ken='
kens = {'東京':8, '埼玉':10, '千葉':11}
text = ''
try:
    for ken, num in kens.items():
        url = url_base + str(num) + "&q=" + kw
        soup = getsoup(url)
        pager = soup.select('.pager')[0].select('li > a')
        pages = len(pager)
        if pages == 0:
            text += getdetails(soup)
        for page in range(1, pages):
            url += "&p=" + str(page+1)
            soup = getsoup(url)
            text += getdetails(soup)
    print(text)

except Exception as e:
    print(e)
