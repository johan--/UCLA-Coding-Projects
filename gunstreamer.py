import os
import sys
import math
import time
from datetime import datetime
import simplejson as json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from geopy import geocoders
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
import tweepy
import json


#Variables that contains the user credentials to access Twitter API 
access_key = '2981595259-rNdQQ3gkigeDoKkcfNAOBOz99jQcJsh379fsSC1'
access_secret = 'sp0mR0a0UPbB04Lart0eVt8Eh57II7gCIpcFecwQH9qGo'
consumer_key = 'UcUk7YemRsZolPKpG5WX2RGZy'
consumer_secret = '4CU9UAcudTIVD405h4HAICPiLXAT2XzXKdOtdZzppKM09cfAuU'

#Runs auth to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


#This is a basic listener that will print incoming data to stdout
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


#Customizes the stream and saves text and lang to databases 
class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = pymongo.MongoClient('localhost', 27017).crime4
    
    
            
    def on_data(self, data):
        jd = json.loads(data)
        if jd['place'] is not None :
            self.db.tweets.insert( { 'text' : jd['text'], 'coordinates' : jd['coordinates'], 'lang' : jd['lang'], 'geo' : jd['geo'], 'place' : jd['place'],'location' : jd['location'], 'expanded_url' : jd['expanded_url'] } )
           
                         

    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

#Calls on StreamListerner and provides specifications of tracking
l = tweepy.streaming.Stream(auth, CustomStreamListener(api))
l.filter(track=['violence'])