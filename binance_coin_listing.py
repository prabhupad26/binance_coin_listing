# -*- coding: utf-8 -*-
"""
Author: prabhupad pradhan
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import datetime
def get_Binance_listings(last_datetime='2018-04-17T03:53:58Z'):
    last_datetime_modified = datetime.datetime.strptime(last_datetime, "%Y-%m-%dT%H:%M:%SZ") #For capturing the input timestamp in standard format for comparision
    listing_hrefs = [] # Empty list for storing the coin listing url
    new_listings = [] #empty list for storing the resultant disctionary
    host_url='https://support.binance.com' #This host url will be apended to the hrefs fetched
    #Loop to fetch all the listing hrefs from the provided website
    for x in range(1,6):#There are 5 pages containg the lisitngs
        r = requests.get('https://support.binance.com/hc/en-us/sections/115000106672-New-Listings?nonce=1525695325073&page='+str(x)+'#articles')
        soup = BeautifulSoup(r.content,'lxml')
        myLinks = soup.findAll('a',class_='article-list-link')
        print("Added anchor tag : "+str(myLinks[x]))
        #loop to append the hrefs to the array
        for index in range(len(myLinks)):
            listing_hrefs.append(myLinks[index].attrs['href'])
            print("Added hrefs from the anchor tags: "+str(listing_hrefs[index]))
    #Loop to append the host_url to the listing hrefs and update the hrefs in listing hrefs
    for url in listing_hrefs:
        listing_hrefs[listing_hrefs.index(url)]=urljoin(host_url,url)
        print(str(listing_hrefs[listing_hrefs.index(urljoin(host_url,url))]))
    #Loop to fetch the data from collected urls
    for url in listing_hrefs:
        listing_dict = {}
        r = requests.get(url,verify=False)
        soup_listing = BeautifulSoup(r.content,'lxml')
        listing_datetime = soup_listing.find('time').attrs['datetime']
        listing_datetime_modified = datetime.datetime.strptime(listing_datetime, "%Y-%m-%dT%H:%M:%SZ")
        #Comparing the datetime in the standard format 2018-04-17T03:53:58Z
        print("URL in progress: "+str(url))
        if (listing_datetime_modified>last_datetime_modified):#Start capturing only if date is greater than the last_datetime
            listing_dict['listing_datetime'] = soup_listing.find('time').attrs['datetime']#Collected the datetime
            print("Added listing time : "+str(soup_listing.find('time').attrs['datetime']))
            listing_title = soup_listing.find('h1',class_='article-title').attrs['title']#Fetched the title from the listing url, this will be further used for extracting the lisitng_coin
            if ('Lists' in listing_title):
                listing_dict['listing_coin'] = listing_title.split('Lists')[1]#Collected the listing_coin
                print("Added listing coin: "+str(listing_title.split('Lists')[1]))
                if len(soup_listing.findAll('p')[1].text) == 1:
                    listing_dict['text'] = str(soup_listing.findAll('p')[1].string)#Collected some text
                    print("Added listing text: "+str(soup_listing.findAll('p')[1].text))
                else:
                    listing_dict['text']= str(soup_listing.findAll('p')[2].string)
                    print("Added listing text: "+str(soup_listing.findAll('p')[1].text))
            new_listings.append(listing_dict)#append dictionary to the required array
    return new_listings
print (get_Binance_listings())