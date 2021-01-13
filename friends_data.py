import requests
import AdvancedHTMLParser
import re
from random import *
import webbrowser

import tempfile

parser = AdvancedHTMLParser.AdvancedHTMLParser()

#try all episode 
class FriendsEpisode(object):
    
    def __init__(self, *args, **kwargs):
        self.all_episode = [[i,j] for i in range(1,11) for j in range(1,25) ] # i is season and j episode
        self.all_episode.pop(24*8 + 23)
        for k in range(7): self.all_episode.pop(-1)

    
    e = 0
    
    def get_info(self):
        self.e = randint(0,len(self.all_episode) -1 )
        r = requests.get("https://www.betaseries.com/episode/friends/s{:02d}e{:02d}".format(self.all_episode[self.e][0],self.all_episode[self.e][1]))

        #print("Episode choose : s{:02d}e{:02d}".format(self.all_episode[e][0],self.all_episode[e][1]))
        # Parse an HTML string into the document
        parser.parseStr(r.text)

        title = parser.getElementsByClassName("blockInformations__title")[0].innerText
        title = re.sub(r'  +','',title.replace("\n",'')).replace("&#039;","'")
        

        #blockInformations__metadatas
        date_prod = parser.getElementsByClassName("blockInformations__metadatas").getElementsByClassName("u-colorWhiteOpacity05")[0].innerText
        

        #blockInformations__synopsis
        synopsis = parser.getElementsByClassName("blockInformations__synopsis")[0].innerText
        synopsis = re.sub(r'  +','',synopsis.replace("\n",''))
        #sr-only
        #suite = parser.getElementsByClassName("blockInformations__synopsis")[0].parentElement.getElementsByClassName("sr-only")[0].innerText
        try:
            suite = re.sub(r'  +','',parser.getElementsByClassName("blockInformations__synopsis")[0].parentElement.getElementsByClassName("sr-only")[0].innerText.replace("\n",''))
            synopsis += suite
        except:
            pass

        synopsis = synopsis.replace("<!---->",'').replace("&#039;","'")

        #photo
        try:
            photo = requests.get(parser.getElementsByClassName("maxWidth100p heightAuto")[0].src)
            f = tempfile.NamedTemporaryFile()
            f.write(photo.content)
        except:
            f = None
            
        return {"saison_episode":self.all_episode[self.e],"title":title,"date":date_prod,"synopsis":synopsis,"file":f}
    
    def netflix(self):
        n_netflix = 70273997 + (self.all_episode[self.e][0] -1) * 24 +  self.all_episode[self.e][1]
        if self.all_episode[self.e][0] >= 9:
            n_netflix -=1
        webbrowser.open('https://www.netflix.com/watch/{}'.format(n_netflix), new=2)