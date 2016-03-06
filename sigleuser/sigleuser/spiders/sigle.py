#-*-coding:utf-8-*-
import scrapy
from sigleuser.items import SigleuserItem
import re
import os
import sys
import time
import requests
reload(sys)
start_time = time.time()
sys.setdefaultencoding('utf-8')

class Single_Sprider(scrapy.Spider):
      name = "single"
      start_urls=['http://i.autohome.com.cn/9667151']
      def parse(self,response):
          url = response.xpath('//*[@class="state-mes"]/@href').extract()[0]
          cookie = {"Cookie":"sessionfid=2200261338; cookieCityId=110100; __utma=1.302253700.1456885521.1457176818.1457227843.16; __utmz=1.1457176818.15.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=python%20%E8%AF%BB%E5%8F%96%E6%96%87%E4%BB%B6; sessionip=120.236.174.157; area=440199; sessionid=60422434-3149-563B-7959-E5DBCBBD5726%7C%7C2016-03-02+10%3A25%3A22.693%7C%7C0; ref=www.baidu.com%7Cpython%B6%C1%C8%A1%CE%C4%BC%FE%7C0%7C0%7C2016-03-05+19%3A20%3A19.136%7C2016-03-02+12%3A14%3A21.726; sessionuid=60422434-3149-563B-7959-E5DBCBBD5726||2016-03-02+10%3A25%3A22.693||0; mylead_25430095=11; historybbsName4=a-100006%7C%E5%B9%BF%E4%B8%9C%7C%2F2012%2F12%2F3%2F6ee52a9e-a1eb-4faa-8c44-8b2ec69045a4_s.jpg; sessionfid=3126420186; __utmb=1.0.10.1457227843; __utmc=1; sessionvid=1284D236-7E54-57C1-37C7-7A650CF77341; ASP.NET_SessionId=cdkozjjmpa525xby20rymhgv; autosessionid=7fa8c1ed-6a85-4661-8dcc-4982f9677626; pcpopclub=6BF25CE61BDD8FB5234D3568A3BF5A12EEFDE7B827DD30AA2BADB9E6D4A8E9327B1A2DA43178D02436BAFC5F004A60462F87919BC9E7A6898ADC52693335051E319B8A624C02CB5B2E29BE2F627E44E6851E84F6282B6ADE2DAD006618D1871684F3B8FCF28A0150755BDFCEC2D81A98E01CEAC768E94B1C7F82C1835C72B9A2A655511A298CBEE6665C951319B72F62C83DBA340C17DB9A1BD5C2FEB0BC5309D20E35A7A8B5A6F0594B0B3F576BE75F3D2B1C9DA613532C7BA3E3BA8251EA515E6F4BB0CC9473460E600AB076DD577D4D244670AFB59B882CEC3E44CC3167196004B8CFCC7DC1D2581F36A6B9AE289EAF1FFF34459AD30642648DDE451475B70C8829BC5507E4051B951EF1F7F110C9CCB4FD87CE5BD34EF1E60770; clubUserShow=25430095|270|6|mayh5|0|0|0||2016-03-06 09:31:13|0; autouserid=25430095; sessionuserid=25430095; sessionlogin=27480ad95c0d4cbb8796755738e862f70184084f"}
          userid = re.search('/(\d+)',response.url)
          items = []
          global start_time
          headurl='http://i.autohome.com.cn/'
          topicurlstart='http://i.service.autohome.com.cn/clubapp/OtherTopic-9667151-all-1.html'
          topicurl = re.sub('-\d+-','-'+userid.group(1)+'-',topicurlstart)
          print "topicurl: ",topicurl,'\n\n'
          validurls = []
          #if time.time() - start_time > 10:
          #     sys.exit(0)
          mypage = requests.get(response.url,cookies = cookie)
          print response.url
          with open('home','wb') as homepage:
               homepage.write(mypage.text)
          num = re.findall('<span(.*?)>(\d+)</span>',mypage.text,re.S)
          print 'following:',num[0][1],'\n'
          print 'follower:',num[1][1],'\n'
          topicpage = requests.get(topicurl,cookies=cookie)
          
          with open('topic','wb') as topage:
               topage.write(topicpage.text)
          topa = open('topic')
          topatext = topa.read()
          utopa = topatext.decode('utf-8')
          etopicnum = re.findall('>(\d+)',utopa,re.S)[2]
          topicnum = re.findall('<strong class="fcolor_6">(\d+)</strong>',utopa,re.S)[0]
          print 'myetopic',etopicnum,'\n'
          print 'mytopic',topicnum,'\n'
          topictitle = re.findall('<div.*?_blank" >(.*?)</a>',utopa,re.S)
          for each in topictitle:
              print each,'\n'
          print "userid f",userid.group(1) 
          
          followingpage = requests.get(response.url+'/following',cookies = cookie)
          following = re.findall('<li id="(\d+)">',followingpage.text,re.S)
          followerpage = requests.get(response.url+'/followers',cookies=cookie)
          followers = re.findall('<li id="(\d+)">',followerpage.text,re.S)
          for uid in following:
              validurls.append(headurl+uid)
          #for userid in followers:
          #    validurls.append(headurl+userid)
          items.extend([self.make_requests_from_url(url).replace(callback=self.parse) for url in list(set(validurls))])
          sigle = SigleuserItem()
          sigle['UserId'] = userid.group(1)
          print 'userId',userid.group(1)
          sigle['Following'] = following
          sigle['Follower'] = followers
          sigle['FollowingNum']=num[0][1]
          sigle['FollowerNum']=num[1][1]
          sigle['Topic'] = topictitle
          sigle['MTopicNum'] = topicnum
          sigle['ETopicNum'] = etopicnum
          items.append(sigle)
          return items
