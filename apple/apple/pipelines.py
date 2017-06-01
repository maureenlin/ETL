# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class ApplePipeline(object):
    def open_spider(self,spider):   #啟動資料庫連線動作操作
        self.conn= sqlite3.connect('apple.sqlite')  #建立連線,要連線的資料庫名稱為apple.sqlite
        self.cur = self.conn.cursor()   #建立cur做資料的操作 
        self.cur.execute('create table if not exists apple(title varchar(100), content text, time varchar(50));')   #建立表格

    def close_spider(self,spider):  #結束資料庫連線
        self.conn.commit()                          #操作完資料庫指令後 確認指令下commit	
        self.conn.close()           #關閉資料庫

    def process_item(self, item, spider):		#把 items.py的資料塞入到資料庫
        col = ',',join(item.keys())             #column 用join把items的(title, content, time ,url)跟','隔開
        placeholders =',',join(len(item)*'?')   #知道(len(item))的長度後要設跟他一樣長度的?
        sql='insert into apple({}) values({})'  #資料庫指令 insert into table,table 的地方就是apple,({})包含就是column
                                                # 後面就是values(values的地方是要放placeholders)
        self.cur.execute(sql.format(col,placeholders), item.values())   #把抓下來的放入格式化後的sql
        								 		
        return item
