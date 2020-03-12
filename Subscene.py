from bs4 import BeautifulSoup
import requests
import json
from urllib import request


class Subscene:    
    def getFilmById(filmId):
        url = "https://subscene.com/subtitles/" + filmId
        content = requests.get(url).text
        soup = BeautifulSoup(content, "html.parser")
        film = Film()
        film.id = filmId
        film.link = url
        film.subtitles = []
        for tr in soup.select("#content > div.subtitles.byFilm > div.content.clearfix > table > tbody > tr"):
            a = tr.select_one("td.a1 > a")
            if (not a):
                continue
            subtitle = Subtitle()
            subtitle.link = a["href"]
            subtitle.language = tr.select_one("td.a1 > a > span:nth-child(1)").text.strip()
            subtitle.name = tr.select_one("td.a1 > a > span:nth-child(2)").text.strip()

            film.subtitles.append(subtitle)   
        return film

    def Search(filmName):
        url='https://subscene.com/subtitles/searchbytitle'
        r = requests.post(url, json={"query":filmName}) 
        soup = BeautifulSoup(r.text, "html.parser")
        filmList=[]
        for li in soup.select('#left > div > div > ul > li'):
            film=Film()
            a=li.select_one('#left > div > div > ul > li > div.title > a')
            film.link="https://subscene.com" + a['href']
            filmList.append(film)
        return filmList
    
    def LogIn():
        s = requests.Session()
        url="https://subscene.com/account/login"
        user_agent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        loginUrlForm = s.get(url,headers=user_agent).url
        r=s.get(loginUrlForm,headers=user_agent).text
        soup = BeautifulSoup(r, "html.parser")
        selectModelJson=soup.select_one('#modelJson').text.replace('&quot;','"')
        jsonObject=json.loads(selectModelJson)
        tokenValue=jsonObject.get('antiForgery').get('value')
        r=s.post(loginUrlForm,data={"idsrv.xsrf":tokenValue,"username":"Andrewhany","password":"123456789"},headers=user_agent)
        response=s.get(r.url,headers=user_agent)
        responseText=response.text
        soup = BeautifulSoup(responseText, "html.parser")
        inputs=["id_token","access_token","token_type","expires_in","scope","state","session_state"]
        data={}
        for i in inputs:
            st='input[name=%s]'%(i)
            Selector=soup.select_one(st)
            data[i]=Selector['value']   
        url="https://subscene.com/"
        r=s.post(url,data=data,headers=user_agent).text
        soup=BeautifulSoup(r,"html.parser")
        print(soup)


class Film:
    def __init__(self):
        self.id = None
        self.title = None
        self.link = None
        self.subtitles = []   
    def __repr__(self):
        return str(self)  
    def __str__(self):  
        #return  "link is : " + str(self.link)    
        return("\nid: "+ str(self.id) +"\nSubtitles:" + str(self.subtitles) + "\nlink: " + str(self.link))
        
                   
class Subtitle:
    def __init__(self):
        self.id = None
        self.link = None
        self.name = None
        self.language=None
        self.releases = []
        self.downloadsCount = None
        self.downloadLink = None   
    def __repr__(self):
        return str(self)    
    def __str__(self):
        return "Name: %s - Language: %s - Link: %s - \n" % (self.name, self.language,self.link)

    

#print(Subscene.getFilm("inferno-1980"))
#print(Subscene.Search("inferno"))
Subscene.LogIn()


