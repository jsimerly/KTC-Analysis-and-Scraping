import requests
import json
import re
from bs4 import BeautifulSoup

class Scraper():
    def _fetch(self, url):
        resp = requests.get(url)
        return resp

    def _getSoup(self, resp):
        soup = BeautifulSoup(resp.text, 'html.parser')
        return soup

    def _getContent(self, url):
        resp = self._fetch(url)
        soup = self._getSoup(resp)
        
        pattern = re.compile(r'var playerSuperflex', re.MULTILINE | re.DOTALL)
        
        content = soup.find('script', text=pattern)
        return content
    
    def parseToJson(self, url):
        content = str(self._getContent(url))
        bottomHalf = content.split("var playerSuperflex = ",1)[1]
        fullCut = bottomHalf.split(';\n        var playerOneQB = ',1)[0]
        js = json.loads(fullCut)
        return js
    
    def getOverallValue(self, data):
        return data['overallValue']

    


if __name__ == '__main__':
    scraper = Scraper()
    data = scraper.parseToJson('https://keeptradecut.com/dynasty-rankings/players/patrick-mahomes-272')
    oData = scraper.getOverallValue(data)
    
    print(oData)

