import urllib2
from bs4 import BeautifulSoup as bs
from models.investement import Investement

def extract():
    '''
    Extract the live investments from crowdcube and return a list of investement
    models.
    '''
    url = 'https://www.crowdcube.com/investments'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'} #mocking browser headers : http://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
    req = urllib2.Request(url, headers = hdr)
    response = urllib2.urlopen(req)
    if response.getcode() != 200:
        return [] #the page scrape did not work well, should have a better handling approach
    content = response.read()
    soup = bs(content)
    pitches = soup.findAll('div', {'class':'pitch'})
    investments = []
    for pitch in pitches:
        pitch_soup = bs(str(pitch))
        title = pitch_soup.find('h2',{'class':'pitch__title'})
        investement = Investement()
        investement.title = title.a.renderContents()
        investement.external_link = title.a['href']
        investement.short_summary = pitch_soup.find('p',{'class':'pitch__description'}).a.get_text()
        investement.amount_raised = float(pitch_soup.find('span',{'class':'pitchProgress__figure'}).renderContents().decode('unicode_escape').encode('ascii','ignore').replace(',',''))
        investement.percentage_raised = float(pitch_soup.find('span',{'class':'pitchProgress__percentage'}).renderContents().replace('%',''))
        stats = pitch_soup.findAll('li',{'class':'pitch__stat'})
        for stat in stats:
            label = stat.findAll('span')[0].renderContents()
            if label.strip() == 'Days left': # not accurate as less than 5 are part of this ! But good for this problem.
                investement.days_remaining = int(stat.findAll('span')[1].renderContents()) 
        investments.append(investement)

    return investments            




