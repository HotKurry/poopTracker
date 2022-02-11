
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from twython import Twython
import random

tweetStr = "None"


api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

timeline = api.get_user_timeline()
lastEntry = timeline[0]
sid = str(lastEntry['id'])

def searchTwitter(sString, perP):
	return api.search(q=sString, since_id=sid, rpp=perP)

def oneGif(twitSearch, sString, gifName):
	for tweet in twitSearch['statuses']:
		user = tweet["user"]["screen_name"]
		text = tweet['text']
		id = str(tweet['id'])
		print text.encode('utf-8')
		if sString in text.lower():
			statushead = "@" + user + " "
			if "RT" not in text:
				api.create_favorite(id=id)
			photo = open('/home/pi/gifs/' + gifName, 'rb')
			response = api.upload_media(media=photo, media_type='image/gif')
			api.update_status(status=statushead, media_ids=[response['media_id']], in_reply_to_status_id=id)
			tweetStr = statushead + gifName
			return "Tweeted: " + tweetStr

def threeGif(twitSearch, sString, gifOne, gifTwo, gifThree):
	for tweet in twitSearch['statuses']:
		user = tweet["user"]["screen_name"]
		text = tweet['text']
		id = str(tweet['id'])
		print text.encode('utf-8')
		if sString in text.lower():
			statushead = "@" + user + " "
			if "RT" not in text:
				api.create_favorite(id=id)
			number = random.randrange(1,4)
			if number == 1:
				photo = open('/home/pi/gifs/' + gifOne, 'rb')
				response = api.upload_media(media=photo, media_type='image/gif')
				api.update_status(status=statushead, media_ids=[response['media_id']], in_reply_to_status_id=id)
				tweetStr = statushead + gifOne
			if number == 2:
				photo = open('/home/pi/gifs/' + gifTwo, 'rb')
				response = api.upload_media(media=photo, media_type='image/gif')
				api.update_status(status=statushead, media_ids=[response['media_id']], in_reply_to_status_id=id)
				tweetStr = statushead + gifTwo
			if number == 3:
				photo = open('/home/pi/gifs/' + gifThree, 'rb')
				response = api.upload_media(media=photo, media_type='image/gif')
				api.update_status(status=statushead, media_ids=[response['media_id']], in_reply_to_status_id=id)
				tweetStr = statushead + gifThree
			return "Tweeted: " + tweetStr

