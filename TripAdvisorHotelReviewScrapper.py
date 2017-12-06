from __future__ import print_function
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests #pip install Requests
from bs4 import BeautifulSoup #pip install BeautifulSoup4
import json #import json
import time
start_time = time.time()
page = requests.get("https://www.tripadvisor.com/Hotel_Review-g295424-d1056980-Reviews-Shalimar_Park_Hotel-Dubai_Emirate_of_Dubai.html")
soup = BeautifulSoup(page.content, 'html.parser')
hotel = soup.find_all('h1', class_='heading_title')[0].get_text()

class Reviewer:

    def __init__(self, revewId, link, title):
        self.review = revewId
        self.link = link
        self.title = title

    def check(self):
        rev = requests.get(self.review)
        soups = BeautifulSoup(rev.content, 'html.parser')
       # titolo = soups.find_all('div', class_='quote')[0].get_text()

        for link_0 in soups.find(id=self.link):
            member =  link_0.find_all('div', class_='username')[0].get_text()
            avatar =  link_0.find_all('img', class_='basicImg')
            #Member Location
            location = ''
            if link_0.find_all('div', class_='location'):
                location = link_0.find_all('div', class_='location')[0].get_text()
            else:
            #location =  link_0.find_all('div', class_='location')[0].get_text()
                location = "-"
            #Review Ratings
            rating =  link_0.find_all('span', class_='ui_bubble_rating')
            date =  link_0.find_all('span', class_='ratingDate')[0].get_text()
            #Review Subject
            quote =  link_0.find_all('div', class_='quote')[0].get_text()
            #Review
            comment =  link_0.find_all('p', class_='partial_entry')[0].get_text()
            quote = quote.replace('\u2019', ' ')
            comment = comment.replace('\u2019', ' ')
            comment = comment.replace('\u201c', ' ')
            comment = comment.replace('\u201d', ' ')
            #Json Encode
            encoded = json.dumps(['review', {'user': member, 'avatar': str(avatar), 'location': str(location), 'ratings': str(rating), 'date': str(date), 'subject': str(quote), 'comment': str(comment)}])
            return encoded
retProcess = ""
for link in soup.find_all('div', class_='prw_rup prw_reviews_basic_review_hsx'):
    for link01 in link.find_all('div', class_='reviewSelector'):
        linkid = link01.get('id')
    for link0 in link.find_all('div', class_='quote'):
        for link1 in link0.find_all('a'):
            if link1.has_attr('href'):
                sublink = 'https://www.tripadvisor.com' + link1['href']
                prc = Reviewer(sublink, linkid, hotel)
                process = prc.check()
                #print ('Please Wait...')
                print(process)
                retProcess +=  process + ","
                retProcess = retProcess.rstrip(',')
f = open(hotel+'.txt', 'w')
f.write(retProcess)
f.close()


print("---processing time: %s seconds ---" % (time.time() - start_time))
