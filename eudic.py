#!/usr/bin/python3

# Eudic词典生词本导出生成指定格式


from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import random
import time

def words(file):
    soup=BeautifulSoup(open(file),'html.parser')
    soup=soup.body.div.table.tbody.find_all('tr')
    words=[]
    for i in soup[1:]:
        words.append(i.find_all('td')[1].contents[0])
    return words

class Eudic:
    def __init__(self,word):
        #header=UserAgent(use_cache_server=False,cache=False,verify_ssl=False)
        #ua = UserAgent(verify_ssl=False)
        #eudic=requests.get("https://dict.eudic.net/dicts/en/"+word, header.firefox).text
        eudic=requests.get("https://dict.eudic.net/dicts/en/"+word).text
        self.soup=BeautifulSoup(eudic,'html.parser')

    def getPhonetic(self):
        soup=self.soup.find_all(class_='Phonitic')
        phonetic=[]
        for i in soup:
            phonetic.append(i.contents[0])
        return phonetic

    def getExp(self):
        expFCChild=self.soup.find_all(id='ExpFCChild')[0]
        condition=0 # 默认情况0

        # 共三种情况，前两种condition=0
        soup=expFCChild.find_all(class_='exp')
        if soup==[]:
            soup=[expFCChild.ol]
        if soup ==[None]:
            try:
                soup=expFCChild.contents[3:5]
                soup[0]=soup[0].contents[0]
            except:
                soup=expFCChild.contents[2:4]
                soup[0]=soup[0].contents[0]
            condition=1

        exp=[]
        if condition==0:
            for i in soup:
                expp=i.find_all('li')
                if expp !=[]:
                    for j in expp:
                        if len(j.contents) ==2:
                            j.contents[0]=j.contents[0].contents[0]
                        exp.append(j.contents)
                else:
                    exp.append(i.contents)
        if condition==1:
            exp.append(soup)
        return exp

    def getSample(self):
        expFCChild=self.soup.find_all(id='ExpLJChild')[0]
        soup=expFCChild.find_all(class_='lj_item')
        sample=[]
        for i in soup:
            s=''
            for j in range(len(i.div.p.contents)):
                try:
                    i.div.p.contents[j]=i.div.p.contents[j].contents[0]
                except:pass
                s+=str(i.div.p.contents[j])
            chinese=i.div.find_all('p')[1].contents[0]
            sample.append([s,chinese])
        return sample


class BingDict:
    def __init__(self,word):
        pass 


if __name__ == '__main__':
    f=open("words.txt","w+")
    for i in words("Print.html")[:50]:
    #for i in ['crackdown','abortion']:
        print(i)
        eudic=Eudic(i);

        # 写入单词
        f.write(i)
        try:
        #if 1==1:
            # 写入音标
            phonetic=eudic.getPhonetic()
            for j in phonetic:
                f.write(j)
            f.write("\n")

            # 写入释义
            exp=eudic.getExp()
            for j in exp:
                f.write("\t")
                for k in j:
                    f.write(str(k))
                f.write("\n")

            # 写入例句
            sample=eudic.getSample()
            sentence=random.choice(sample)
            f.write("\te.g. "+str(sentence[0])+"\n")
            f.write("\t    "+str(sentence[1]))
        except Exception as e:
            print(e)
        f.write("\n")
        time.sleep(random.randint(1,10))
    f.close()
