import scrapy
from bs4 import BeautifulSoup   
from Dcard.items import DcardItem   # 資料元件定義來源


class DcardCrawler(scrapy.Spider):
	name='dcard'  #給一個名稱
	start_urls=['https://www.dcard.tw/f/trending']	 #抓取的起始頁
	
	
	
	def parse(self, response):  #建立一個parse方法並呼叫self 把抓取的內容放在response
		domain='https://www.dcard.tw'
		res = BeautifulSoup(response.body)
		for news in res.select('.PostEntry_container_245XM'):
			# print(news.select('.PostEntry_titleUnread_ycJL0')[0].text)
			# print(domain + news.select('a')[0]['href'])
			yield scrapy.Request(domain + news.select('a')[0]['href'], self.parse_detail) #透過清單連結鑽取內文,並把回應pass到parse_detail,再透過 self.parse_detail剖析內容

			
			
			
	def parse_detail(self,response):   #建立 parse_detail 並呼叫self  把結果放在response
		res = BeautifulSoup(response.body)
		dcarditem = DcardItem()   #資料格式的順序會跟AppleItem一樣
		dcarditem['title']=(res.select('h1')[0].text)  #定義內容要跟items.py的定義一樣
		dcarditem['content'] =(res.select('div')[0].text)
		dcarditem['time'] = (res.select('.Post_published_13TGw')[0].text)
		dcarditem['url'] = (response.url)
		
		return dcarditem
		# print(res.select('h1')[0].text)
		# print(res.select('div')[0].text)
		# print(res.select('.Post_published_13TGw')[0].text)