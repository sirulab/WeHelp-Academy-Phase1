import urllib.request as req
# pip install beautifulsoup4
import bs4
import time
import csv

def get_data(url, headers):
    request = req.Request(url, headers=headers)
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    root = bs4.BeautifulSoup(data, "html.parser")
    articles_data = []
    
    rents = root.find_all("div", class_="r-ent")
    
    for rent in rents:
        title_div = rent.find("div", class_="title")
        
        if title_div.a != None: # 如果文章被刪除
            title = title_div.a.string
            
            article_url = "https://www.ptt.cc" + title_div.a["href"]
            
            nrec_div = rent.find("div", class_="nrec") # 讚的標籤
            like = nrec_div.text # TypeError: 'NoneType' object is not callable
            
            # def get_time()
            t = get_time(article_url, headers)
            
            articles_data.append([title, like, t])

    next_link = root.find("a", string="‹ 上頁")
    next_url = "https://www.ptt.cc" + next_link["href"]
    
    return articles_data, next_url

def get_time(url, headers):
    request = req.Request(url, headers=headers)
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    root = bs4.BeautifulSoup(data, "html.parser")
    
    t = root.find_all("div", class_="article-metaline")
    for i in t:
        tag = i.find("span", class_="article-meta-tag")
        if tag.string == "時間": # type不對
            value = i.find("span", class_="article-meta-value")
            return value.string
    return ""

headers = {
    "cookie": "over18=1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

pageurl = "https://www.ptt.cc/bbs/Steam/index.html"
all_articles = []
counts = 3

for i in range(counts):
    print(f"page{i}---") # 方便檢查
    data, pageurl = get_data(pageurl, headers)
    all_articles.extend(data)

with open("articles.csv", mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["ArticleTitle", "LikeCount", "PublishTime"])

    for article in all_articles:
        writer.writerow(article) # writerows 無法使用