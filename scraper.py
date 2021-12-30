import requests
import json
import re
import time
from bs4 import BeautifulSoup


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
        position = contents.find('div', {'class':'player-details-header-subtext dashboard-header-subtext'}).findAll('span')[0].text
        measureables = contents.findAll('div', {'meas-row'})
        try:
            age = measureables[0].find('p', {'class':'row-value'}).text.strip()
            age = age.replace('y.o.', '')
            height = measureables[2].find('p', {'class':'row-value'}).text.strip().replace(' ', '')
            weight = measureables[3].find('p', {'class':'row-value'}).text.strip()
            drafted = measureables[4].find('p', {'class':'row-value'}).text.strip()
            draftClass = measureables[5].find('p', {'class':'row-value'}).text.strip()
            exp = measureables[6].find('p', {'class':'row-value'}).text.strip()

        except:
            print('None measurables for:')
            print(playerName)
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
        adjBlock = contents.find('div', {'class':'pd-overall-adjacent-block'})
        nextPlayer = adjBlock.find('div', {'class': 'curPlayer'}).find_next_sibling('div')
        nextLink = nextPlayer.findAll('a', {'class':'adjacentPlayerLink'}, href=True)
        for a in nextLink:
            link = a['href']
        return link


    def scrape(self, url, model):
        contents = self._getContent(url)
        #save playerContents
        jsData = self.parseSuperFlexToJson(contents)
        measurables = self.parsePlayerInfoToJson(contents)
        id = self.parseUrlToId(url)
        nextLink = self._getNextLink(contents)
        print(nextLink)
    
        
        time.sleep(2)
        if nextLink != None:
            appenedUrl = 'https://keeptradecut.com' + nextLink
            self.scrape(appenedUrl, 'fuck')
        
        print('The End')
        


if __name__ == '__main__':
    scraper = Scraper()
    content = scraper._getContent('https://keeptradecut.com/dynasty-rankings/players/2023-mid-1st-1096')
    #print(scraper.parseUrlToId('https://keeptradecut.com/dynasty-rankings/players/jonathan-taylor-634'))
    scraper.scrape('https://keeptradecut.com/dynasty-rankings/players/wayne-gallman-172', 'fuck')

    #print(test)

