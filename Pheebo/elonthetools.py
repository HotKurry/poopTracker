import pandas as pd
import tweepy
from datetime import datetime, timezone, timedelta

tweetStr = "None"

#twitter consumer and access information goes here

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

def updateCSV(screen_name , count):
    df = pd.read_csv('Elontracker.csv' , index_col=0)
    statuses = api.user_timeline(screen_name = screen_name, count = count)
    for status in statuses:
        data = pd.DataFrame([
            [status.id, status.created_at, 'post', status.in_reply_to_screen_name ]
        ],
    )
        data.to_csv('Elontracker.csv', mode='a', header=False)
    favs = api.get_favorites(screen_name = screen_name, count = count)
    for status in favs:
        data = pd.DataFrame([
            [ status.id, status.created_at, 'fav', status.user.screen_name  ]
        ],
    )
        data.to_csv('Elontracker.csv', mode='a', header=False)
    df = pd.read_csv('Elontracker.csv' , index_col=0)
    df = df.drop_duplicates()
    df = df.sort_values(by= 'Date', ascending= False)
    df=df.reset_index(drop=True)
    print(df)
    print("-------")
    df.to_csv('Elontracker.csv')
    return df

def timesincePost(df , ind):
    now = datetime.now(timezone.utc)
    last = datetime.strptime(df.iat[ind,1], '%Y-%m-%d %H:%M:%S%z')
    sincepost = now - last
    if ind == 0:
        print("Time Since last post: " + str(sincepost))
    elif ind == 1:
        print("Time Since 2nd to last post: " + str(sincepost))
    elif ind == 2:
        print("Time Since 3rd to last post: " + str(sincepost))
    else:
        print("Time since " + str(ind+1) + "th to last post: " + str(sincepost))
    return sincepost

def poopingStart(mins, df):
    poopDelta = timedelta(minutes=mins)
    startPost = 0
    actTime =  datetime.strptime(df.iat[startPost,1], '%Y-%m-%d %H:%M:%S%z')
    now = datetime.now(timezone.utc)
    while startPost < 100:
        if now-actTime < poopDelta:    
            startPost += 1
            now = actTime
            actTime = datetime.strptime(df.iat[startPost,1], '%Y-%m-%d %H:%M:%S%z')
        else:
            break
    return startPost


def postSomething(name, poopStart, screen_name, df):
    now = datetime.now(timezone.utc)
    startTime =  datetime.strptime(df.iat[poopStart,1], '%Y-%m-%d %H:%M:%S%z')
    timePooping = now - startTime
    poopDensity = timePooping / poopStart
    myLastPost = ""
    statuses = api.user_timeline(screen_name = 'elonthetoilet', count = 1)
    for status in statuses:
        myLastPost = status.created_at
        postText = status.text
    print(myLastPost)
    print(poopDensity)
    poopUpdate = ''
    halfHour = timedelta(minutes=30)    
    quiteDense = timedelta(minutes=3)
    veryDense = timedelta(minutes=2)
    densePoop = ''
    longPoop = ''
    if poopDensity < veryDense:
        densePoop = ' It\'s a bad one.'
    elif poopDensity < quiteDense:
        densePoop = ' It\'s not a good one.'
    if timePooping > halfHour:
        longPoop = ' His leg is Asleep.'
    if myLastPost > startTime:
        poopUpdate = 'still '
    if poopStart == 2:
        msg = name + ' could be ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        print(msg)
    elif poopStart == 3:
        msg = name + ' is probably ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        print(msg)
    elif poopStart == 4:
        msg = name + ' is ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        print(msg)
    elif poopStart >= 5:
        msg = name + ' is definitely ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        print(msg)
    else:
        print('I don\'t know what\'s happening')
    if postText != msg:
        print('posting')     
    return msg