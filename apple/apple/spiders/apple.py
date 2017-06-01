import scrapy
from bs4 import BeautifulSoup
from apple.items import AppleItem   # 資料元件定義來源
from scrapy.spiders import CrawlSpider, Rule  #多網頁爬蟲
from scrapy.linkextractors import LinkExtractor   #連結抓取


class AppleCrawler(CrawlSpider): #開啟一個類別因為要多網頁抓取所以變數由改成Crawlspider,單頁爬變數就用(scrapy.Spider)
    name = 'apple'  #給一個名稱
    start_urls = ['http://www.appledaily.com.tw/column/index/480/'] #抓取的起始頁
    rules = [
        Rule(LinkExtractor(allow=('/column/index/480/[1-5]$')), callback='parse_list', follow=True)
    ]
    #LinkExtractor 就是連結的抓取,allow可以將符合條件的鏈結全部抓取出來,
	
    def parse_list(self, response):  #把抓取到的內容丟到parse_list,透過parse_list去解析網頁的內容
        domain='http://www.appledaily.com.tw'
        res = BeautifulSoup(response.body)  #回應放在response.body,並用BeautifulSoup剖析網頁內容,最後把結果放在res
        for news in res.select('.aht_title'): #新聞清單都放在.aht_title 用for迴圈把新聞撈出來
            #print(news.select('a')[0].text)
            #print(domain + news.select('a')[0]['href'])#頁面連結放在a 且a只有一個元素所以[0]
            yield scrapy.Request(domain + news.select('a')[0]['href'], self.parse_detail) #透過清單連結鑽取內文,並把回應pass到parse_detail,再透過 self.parse_detail剖析內容

    def parse_detail(self,response):  #建立 parse_detail 並呼叫self  把結果放在response
        res = BeautifulSoup(response.body)
        appleitem = AppleItem()  #資料元件的順序會跟AppleItem一樣
        appleitem['title']=(res.select('#h1')[0].text)  #定義內容要跟items.py的定義一樣
        appleitem['content'] =(res.select('#bcontent')[0].text)
        appleitem['time'] = (res.select('.gggs')[0].text)
        appleitem['url'] = (response.url)

        return appleitem
        #print(res.select('#h1')[0].text)
		
			