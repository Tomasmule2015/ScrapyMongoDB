import scrapy
from mongodb.items import MongodbItem
import re
import os
import time
import requests
import sys
reload(sys)
start_time = time.time()
sys.setdefaultencoding('utf-8')
class link_Sprider(scrapy.Spider):
      name = "mongo"
      
      start_urls=['http://i.autohome.com.cn/25430095']
      def parse(self,response):
          url = response.xpath('//*[@class="state-mes"]/@href').extract()[0]
          cookie = {"Cookie":"sessionfid=3126420186; cookieCityId=110100; __utma=1.302253700.1456885521.1457073017.1457146972.13; __utmz=1.1457068339.10.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; sessionip=120.236.174.157; area=440199; sessionid=60422434-3149-563B-7959-E5DBCBBD5726%7C%7C2016-03-02+10%3A25%3A22.693%7C%7C0; ref=www.baidu.com%7C%7C0%7C0%7C2016-03-03+16%3A11%3A41.946%7C2016-03-02+12%3A14%3A21.726; sessionuid=60422434-3149-563B-7959-E5DBCBBD5726||2016-03-02+10%3A25%3A22.693||0; mylead_25430095=11; historybbsName4=a-100006%7C%E5%B9%BF%E4%B8%9C%7C%2F2012%2F12%2F3%2F6ee52a9e-a1eb-4faa-8c44-8b2ec69045a4_s.jpg; sessionfid=3126420186; __utmb=1.0.10.1457146972; __utmc=1; sessionvid=50D01691-064B-BADD-E0F7-9CE2FAF36874; ASP.NET_SessionId=qyg3cetkldrr5iehld5kgh2c; autosessionid=ada39afb-e0b6-4530-8300-db59816c2b24; pcpopclub=F1237AE304C885949E53E6302872A2FFDF74E65135E4A763555E19B41E81D92B43E532A68B152FE10C80DF1C22D0069BBB06BD391A308B8BB0A6C5971AE791AB3ACCC2DCDC7E99F8DCCEE15378F14861B8E1B4D96461827BB7431ABFED0387661190ED9EFFFE11C28FA8C1D4E7B579444A930BD59A775EED71871DC923B60F6B9CB8A16ED6F5A561C0342E0A20E3F16FD8506989C5ED2CA07A96771CBF25B4C462F83C03841C168621321F2FC23435CE811E403AD0004FBA7E4166535397CAD0340D58387F68355098F5D517CA367691393CD9C50B22A7918B81B08E6116E21300DF36B59D45739FC6882D399B4F8A22299D7735DC45C126E79DB2FF7CF003F8D64C4A1008D5855BD1010FFFAF6092FD3C9F12BA79B5D0E1D4300E28D83A65C54E1932CE; clubUserShow=25430095|270|6|mayh5|0|0|0||2016-03-05 11:13:52|0; autouserid=25430095; sessionuserid=25430095; sessionlogin=b81e6a47c7f64088a544a75ada4fc4860184084f"}
          userid = re.findall('/(\d+)',response.url)
          print "ID:",userid,'\n'
          items = []
          global start_time
          fourl = 'http://i.autohome.com.cn/'          
          validurls=[]
          if time.time() - start_time > 60:
               os._exit(0)
          r = requests.get(response.url+'/following',cookies = cookie)
          
          with open('file','wb') as sa:
               sa.write(r.text)
          following = re.findall('<li id="(\d+)">',r.text,re.S)
          print '\n','yes',following,'\n'
          
	  for url in following:
             validurls.append(fourl+url)
          items.extend([self.make_requests_from_url(url).replace(callback=self.parse) for url in list(set(validurls))])
          mongo = MongodbItem()
          mongo['userId'] = userid
          mongo['userFollowing'] = following
          mongo['create_time'] = int(time.time())
          items.append(mongo)
          return items
        
         

