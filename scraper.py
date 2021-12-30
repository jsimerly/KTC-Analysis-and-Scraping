import requests
import json
import re
import time
from bs4 import BeautifulSoup
from requests.sessions import session
from sqlalchemy.sql.functions import mode
import models
import random

print(models.session)


class Scraper():
    #Get Page Data
    def _fetch(self, url):
        resp = requests.get(url)
        return resp

    def _getSoup(self, resp):
        soup = BeautifulSoup(resp.text, 'html.parser')
        return soup
    
    def _getContent(self, url):
        resp = self._fetch(url)
        content = self._getSoup(resp)
        return content

    def parsePlayerInfoToJson(self, contents):
        playerName = contents.find('div', {'class': 'player-details-header-content dashboard-header-content dashboard-header-content-left'}).text.strip()
        try:
            position = contents.find('div', {'class':'player-details-header-subtext dashboard-header-subtext'}).findAll('a')[0].text
            measureables = contents.findAll('div', {'meas-row'})
            age = measureables[0].find('p', {'class':'row-value'}).text.strip()
            age = age.replace('y.o.', '')
            height = measureables[2].find('p', {'class':'row-value'}).text.strip().replace(' ', '')
            weight = measureables[3].find('p', {'class':'row-value'}).text.strip()
            drafted = measureables[4].find('p', {'class':'row-value'}).text.strip()
            draftClass = measureables[5].find('p', {'class':'row-value'}).text.strip()
            exp = measureables[6].find('p', {'class':'row-value'}).text.strip()

        except:
            print('--------------------------------------------------------------')
            print('None measurables for:')
            print(playerName)
            print('--------------------------------------------------------------')
            position = position = contents.find('div', {'class':'player-details-header-subtext dashboard-header-subtext'}).findAll('span')[0].text
            age = None
            height = None
            weight = None
            draftClass = None
            drafted = None
            exp = None
        
        info = {
            'name': playerName,
            'pos' : position,
            'age' : age,
            'height' : height,
            'weight' : weight,
            'drafted' : drafted,
            'draftClass': draftClass,
            'exp' : exp,
        }

        return info

    def parseUrlToId(self, url):
        return url.rsplit('-',1)[1]


    def parseSuperFlexToJson(self, contents):
        pattern = re.compile(r'var playerSuperflex', re.MULTILINE | re.DOTALL)
        
        content = contents.find('script', text=pattern)
        content = str(content)
        bottomHalf = content.split("var playerSuperflex = ",1)[1]
        fullCut = bottomHalf.split(';\n        var playerOneQB = ',1)[0]
        js = json.loads(fullCut)
        data = js['overallValue']
        return data
   

    #Move to next player
    def _getNextLink(self, contents):
        contBool = True
        try:
            adjBlock = contents.find('div', {'class':'pd-overall-adjacent-block'})
            nextPlayer = adjBlock.find('div', {'class': 'curPlayer'}).find_next_sibling('div')
            nextLink = nextPlayer.findAll('a', {'class':'adjacentPlayerLink'}, href=True)
        except:
            return('empty', False)
        
        for a in nextLink:
            link = a['href']
        return (link, contBool)


    def scrape(self, url):
        contents = self._getContent(url)
        #save playerContents

            
        jsData = self.parseSuperFlexToJson(contents)
        measurables = self.parsePlayerInfoToJson(contents)
        id = int(self.parseUrlToId(url))
        jsData = str(jsData)

        models.playerValues.addPlayer(models.playerValues,
            id,
            measurables['name'],
            measurables['pos'],
            measurables['age'],
            measurables['height'],
            measurables['weight'],
            measurables['drafted'],
            measurables['draftClass'],
            measurables['exp'],
            jsData
        )

        nextLink = self._getNextLink(contents)
        contBool = nextLink[1]
        nextLink = nextLink[0]
        print(nextLink)
    
        sleepTime = random.uniform(1,5)
        time.sleep(sleepTime)
        if contBool:
            appenedUrl = 'https://keeptradecut.com' + nextLink
            try:
                self.scrape(appenedUrl)
            except:
                newUrl = 'https://keeptradecut.com/dynasty-rankings/players/' +nextLink
                self.scrape(newUrl)

            
        else:
            models.session.commit()
           
            models.session.close()

        
        


if __name__ == '__main__':
    scraper = Scraper()

    #use the URL of the highest values player
    scraper.scrape('https://keeptradecut.com/dynasty-rankings/players/patrick-mahomes-272')
    

