#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tweepy
import pandas as pd
import elonthetools
from datetime import datetime, timezone, timedelta
import logging

#config Variables
username = 'elonmusk'
pooper = 'Elon Musk'
updateNum = 10
postGap = 10

#logger config
logging.basicConfig(filename='app.log', level=logging.INFO, format= '[%(asctime)s] %(levelname)s - %(message)s')

#Update post database return database as Dataframe
df = elonthetools.updateCSV(username, updateNum)

#Time since last post in database
since1 = elonthetools.timesincePost(df, 0)

#find post when pooping started 
poopPosts = elonthetools.poopingStart(postGap,df)

#Poop detection algorithm
if poopPosts > 1:
    poopText = elonthetools.postSomething(pooper , poopPosts,  username, df)
elif poopPosts == 1:
    logging.info(pooper + ' could be pooping but we aren\'t sure.')
else:
    logging.info(pooper + ' is not pooping right now.')
