# Scrap structural data from www.brainyquote.com
#
# Creator Name:     Janib Soomro
# Creator Email:    Soomrojb@gmail.com
# Creation Date:    22nd April 2016
# Last Modified:    22nd April 2016

# Imports Section
from BeautifulSoup import BeautifulSoup
import re
import mechanize
import html2text

# Variable Section
MainURL = 'http://www.brainyquote.com/quotes/authors/a/'
UrlInit = 'http://www.brainyquote.com'

# Code Section

# Access Mechanize Browser and do setting
Bwr = mechanize.Browser()
Bwr.set_handle_robots(False)
Bwr.set_handle_equiv(False)
Bwr.addheaders = [('User-agent', 'Mozilla/5.0')]
HtmlContent = Bwr.open(MainURL).read()
Soup = BeautifulSoup(HtmlContent)

def FetchQuotes(Soup):
    # print "Fetching Quotes"
    for QuoteNum in Soup.findAll('', attrs={'class': 'bqQuoteLink'}):
        Quotation = (QuoteNum.text).encode('utf-8')
        AuthDiv = QuoteNum.findNext('div', attrs={'class':'body bq_boxyRelatedLeft bqBlackLink'})
        Tags = ','.join(re.findall(r'>(.+)</a>', str(AuthDiv)))
        csvfile = open('Quotes records.CSV', 'ab')
        csvfile.write(str(AllAuthors.text).replace(',',';;;') + ',')
        csvfile.write(str(AuthorLnk).replace(',',';;;') + ',')
        csvfile.write(str(Quotation).replace(',',';;;') + ',')
        csvfile.write(str(Tags).replace(',',';;;'))
        csvfile.write('\n')
        csvfile.close()

def GetLastPage(Soup):
    LastPg = 0
    for AllAlphas in Soup.findAll('a', href=re.compile(r'/authors/.+')):
        if AllAlphas.text == 'Next':
            PreviousLnk = AllAlphas.findPrevious('a')
            PrvLnk = re.findall(r'(\d+).html', str(PreviousLnk))
            LastPg = PrvLnk[0]
            break
    return LastPg

for AllAlphabets in re.findall(r'href=.(/authors/\w).+>([A-Z])<', HtmlContent):
    AlphaLink = AllAlphabets[0]
    AlphaText = AllAlphabets[1]
    NewLink = UrlInit + str(AlphaLink)
    NewPgSource = Bwr.open(NewLink).read()
    Soup = BeautifulSoup(NewPgSource)
    LastPg = GetLastPage(Soup)
    # print 'Total Page = %s' %LastPg
    for AllAuthors in Soup.findAll('a', href=re.compile(r'/quotes/authors/')):
        if AllAuthors.get('class') == None:
            # if AllAuthors.text == 'Jurgen Habermas':
                # print 'Inside John Hagee'
            AuthorLnk = UrlInit + str(AllAuthors.get('href'))
            AuthorPg = Bwr.open(AuthorLnk).read()
            Soup = BeautifulSoup(AuthorPg)
            LastAuthPg = GetLastPage(Soup)
            print AllAuthors.text + ' ' + UrlInit + str(AllAuthors.get('href')) + ' ' + str(LastAuthPg)
            if LastAuthPg >= 1:
                print "Quotation pages are more than 0"
                for CurPg in range(int(LastAuthPg)):
                    FetchQuotes(Soup)
                    print "checking next button"
                    for NextBtn in Soup.findAll('a'):
                        NextBtnUrl = UrlInit + str(NextBtn.get('href'))
                        if NextBtn.text == 'Next':
                            Soup = BeautifulSoup(Bwr.open(NextBtnUrl).read())
                            # break
            else:
                print "0 Quotation pages"
                QuoteDetails = FetchQuotes(Soup)
