#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tweepy
import pandas as pd
import elonthetools
from datetime import datetime, timezone, timedelta


df = elonthetools.updateCSV('elonmusk', 10)

since1 = elonthetools.timesincePost(df, 0)

since7 = elonthetools.timesincePost(df, 6)

poopPosts = elonthetools.poopingStart(10,df)

now = datetime.now(timezone.utc)

lastTime =  datetime.strptime(df.iat[0,1], '%Y-%m-%d %H:%M:%S%z')
secTime =  datetime.strptime(df.iat[1,1], '%Y-%m-%d %H:%M:%S%z')
therdTime =  datetime.strptime(df.iat[2,1], '%Y-%m-%d %H:%M:%S%z')


print('new and last: ' + str(now - lastTime))

print('last and next: ' + str(lastTime - secTime))
print('next and next: ' + str(secTime - therdTime))

print(poopPosts)
if poopPosts != 0:
    poopText = elonthetools.postSomething('Elon Musk', poopPosts,  'elonmusk', df)
