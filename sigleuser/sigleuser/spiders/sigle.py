#-*-coding:utf-8-*-
import scrapy
from sigleuser.items import SigleuserItem
import re
import os
import sys
import time
import requests
import string
reload(sys)
start_time = time.time()
sys.setdefaultencoding('utf-8')

class Single_Sprider(scrapy.Spider):
      name = "single"
      start_urls=['http://i.autohome.com.cn/9667151']
      def parse(self,response):
          url = response.xpath('//*[@class="state-mes"]/@href').extract()[0]
          cookie = {"Cookie":"cookieCityId=110100; __utma=1.995157461.1457319057.1457444568.1457487399.5; __utmz=1.1457319057.1.1.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=%E6%B1%BD%E8%BD%A6%E4%B9%8B%E5%AE%B6; sessionip=120.236.174.158; area=440199; sessionid=70D13D3C-93A5-F21C-1D62-A5EDEE2E8CCF%7C%7C2016-03-07+10%3A50%3A59.460%7C%7Ccn.bing.com; ref=cn.bing.com%7C0%7C0%7C8-1%7C2016-03-07+10%3A50%3A59.460%7C2016-03-07+10%3A50%3A59.460; sessionuid=70D13D3C-93A5-F21C-1D62-A5EDEE2E8CCF||2016-03-07+10%3A50%3A59.460||cn.bing.com; pcpopclub=EC5D13D82BA7188343925AC74269EF1E5DEBA55F33D10CED0D02372FDF24C066C5EAC2283636AB1C530E9EC732C5A7FD5040082A119D73B3C99052BA2D71BAC1492F10E107EEB611BD0AF1032AC5442CDC79C3791DEC7A5AED3D940260158313B82EFDD3EF41A7660F9A8720EA061DFE2AD4B6F1213F0BF74EFA535C0567240EA395F86202E86889108EF8779BB8F2B534D6E4A5008A3371DF0485BCF86ADE6C1C76F86218D13F0D18A01550F6DA3DB69C8ADDA59D277FE2F2140F43428867C3C7D8EDCCC60190745DCC1DD5D2770E7A8F8767FA0E003717C9AA1670A7BAF7C2D18CF8EEC047160EB97E1E53CE8FFCBD68C3F8EB6E97A08C232BC40B56C3760C389F50D404C8DB24C0FB57C739F7414B64A958F904C8960BC4D149FA928937A38A49F6B6; clubUserShow=25430095|270|6|mayh5|0|0|0||2016-03-07 10:58:14|0; autouserid=25430095; mylead_25430095=11; historybbsName4=c-597%7C%E5%8A%9B%E5%B8%86320%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg4%2FM0A%2F1D%2FA2%2Fuserphotos%2F2015%2F12%2F23%2F23%2FwKgH2lZ6vnWAYpDSAH370Gy_kQ4174_s.jpg%2Cc-526%7C%E5%8D%A1%E7%BD%97%E6%8B%89%7C%2F2014%2F10%2F16%2F5f68376d-c6a6-480a-804e-6ac07efee3b8_s.jpg; sessionlogin=9c893b473ee14d4aa09d36dfb36894370184084f; sessionuserid=25430095; sessionfid=621624554; __utmb=1.0.10.1457487399; __utmc=1; AccurateDirectseque=404; sessionvid=6054852E-6A64-914E-FC59-34877DB91D24; ASP.NET_SessionId=nshcur2x32xgp5nviepigkm4"}
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
          pageindex = string.atoi(num[0][1])/20
          if string.atoi(num[0][1])%20 != 0:
               pageindex += 1
          page = 0
          following = []
          while(page < pageindex ):
              followingpage = requests.get(response.url+'/following?page='+'%d'%page,cookies = cookie)
              following.extend(re.findall('<li id="(\d+)">',followingpage.text,re.S))
          #    print 'page:',page,'total',pageindex,'\n'
              page= page+1
              
         # followerpage = requests.get(response.url+'/followers',cookies=cookie)
#          followers = re.findall('<li id="(\d+)">',followerpage.text,re.S)
         # print following
          for uid in following:
              validurls.append(headurl+uid)
          #for userid in followers:
          #    validurls.append(headurl+userid)
          items.extend([self.make_requests_from_url(url).replace(callback=self.parse) for url in list(set(validurls))])
          sigle = SigleuserItem()
          sigle['UserId'] = userid.group(1)
          print 'userId',userid.group(1)
          sigle['Following'] = following
#          sigle['Follower'] = followers
          sigle['FollowingNum']=num[0][1]
          sigle['FollowerNum']=num[1][1]
          sigle['Topic'] = topictitle
          sigle['MTopicNum'] = topicnum
          sigle['ETopicNum'] = etopicnum
          items.append(sigle)
          return items
