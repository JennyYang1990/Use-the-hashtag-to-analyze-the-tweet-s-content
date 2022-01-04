# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 22:43:54 2020

@author: junhe
"""

import tweepy
from tweepy import OAuthHandler
import json
import time



_FILE = "tweet.json"
_QUERY = "#backtoschool"

consumer_key = 'RL07DbHVqceVKQQWPcetD8sLM'
consumer_secret = 'SMMF9QQHvomHGVnk14RXW7mX99aRSA60P1FYF072lUkGz9mqWj'
access_token = '1256377403074646016-EVE5unv5tDYJrv3LgLOBsa3AOy6bv6'
access_secret = 'waIC7tp4qp8BXj0lnptRaBQWK3fmQby1iACljxAO8tftc'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Helper function to handle twitter API rate limit

def limit_handled(cursor, list_name):
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			print("\nCurrent number of data points in list = " + str(len(list_name)))
			print('Hit Twitter API rate limit.')
			for i in range(3, 0, -1):
				print("Wait for {} mins.".format(i * 5))
				time.sleep(5 * 60)
		except tweepy.error.TweepError:
			print('\nCaught TweepError exception' )

# Helper function to get all tweets for a specified user
# NOTE:  This method only allows access to the most recent 3240 tweets
# Source: https://gist.github.com/yanofsky/5436496

def get_all_tweets(query, file_name):

	# initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	# make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.search(q=query,count=200,lang="en")

	with open(file_name,'a') as json_file:
		for tweet in new_tweets:
			json.dump(tweet._json, json_file)
			json_file.write('\n')
	
	# save most recent tweets
	alltweets.extend(new_tweets)
	
	# save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	# keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:

		print("getting tweets before %s" % (oldest))
		
		# all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.search(q=query,count=200,lang="en",max_id=oldest)

		with open(file_name,'a') as json_file:
			for tweet in new_tweets:
				json.dump(tweet._json, json_file)
				json_file.write('\n')
		
		# save most recent tweets
		alltweets.extend(new_tweets)
		
		# update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))

		if len(alltweets)>15000:
			return len(alltweets)
	
	return len(alltweets)


if __name__ == '__main__':
	#pass in the username of the account you want to download
	number = get_all_tweets(query=_QUERY, file_name=_FILE)
	print("Number of Tweets Collected: %d"%number)