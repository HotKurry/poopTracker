import pandas as pd
#from sqlalchemy import null
import tweepy
from datetime import datetime, timezone, timedelta
import logging
import os
from os.path import exists


homeFolder= os.getcwd()
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)



def initCSV():
    file_exists = exists('Elontracker.csv')
    if file_exists != True:
        df2 = pd.DataFrame([], columns=[ 'Post ID', 'Date', 'Post Type', 'reply' ])
        df2.to_csv('Elontracker.csv')
        
#Update Database with number 'count' number of faves and posts
def updateCSV(screen_name , count):
    df = pd.read_csv('Elontracker.csv' , index_col=0)
    #Add new posts to database
    statuses = api.user_timeline(screen_name = screen_name, count = count)
    for status in statuses:
        data = pd.DataFrame([
            [status.id, status.created_at, 'post', status.in_reply_to_screen_name ]
        ],
    )
        data.to_csv('Elontracker.csv', mode='a', header=False)
    favs = api.get_favorites(screen_name = screen_name, count = count)
    #Add new faves to database
    for status in favs:
        data = pd.DataFrame([
            [ status.id, status.created_at, 'fav', status.user.screen_name  ]
        ],
    )
        data.to_csv('Elontracker.csv', mode='a', header=False)
    #drop duplicates, sort, rebuild index
    df = pd.read_csv('Elontracker.csv' , index_col=0)
    df = df.drop_duplicates()
    df = df.sort_values(by= 'Date', ascending= False)
    df=df.reset_index(drop=True)
    df.to_csv('Elontracker.csv')
    return df

#Get time since post at 'ind' 
def timesincePost(df , ind):
    now = datetime.now(timezone.utc)
    last = datetime.strptime(df.iat[ind,1], '%Y-%m-%d %H:%M:%S%z')
    sincepost = now - last
    if ind == 0:
        logging.info("Time Since last post: " + str(sincepost))
    elif ind == 1:
        logging.info("Time Since 2nd to last post: " + str(sincepost))
    elif ind == 2:
        logging.info("Time Since 3rd to last post: " + str(sincepost))
    else:
        logging.info("Time since " + str(ind+1) + "th to last post: " + str(sincepost))
    return sincepost

#post/fav combo without a >'mins' gap since now
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

#Create a post based on action density, time and number of actions. return text
def postSomething(name, poopStart, screen_name, df):
    now = datetime.now(timezone.utc)
    startTime =  datetime.strptime(df.iat[poopStart,1], '%Y-%m-%d %H:%M:%S%z')
    timePooping = now - startTime
    poopDensity = timePooping / poopStart
    myLastPost = ""
    postTest = ""
    mystatusID = type(None)
    statuses = api.user_timeline(screen_name = 'elonthetoilet', count = 1)
    for status in statuses:
        myLastPost = status.created_at
        postText = status.text
        mystatusID = status.id
    poopUpdate = ''
    halfHour = timedelta(minutes=30)    
    quiteDense = timedelta(minutes=4)
    veryDense = timedelta(minutes=2)
    densePoop = ''
    longPoop = ''
    msg = ''
    if poopDensity < veryDense:
        densePoop = ' It\'s a bad one.'
    elif poopDensity < quiteDense:
        densePoop = ' It\'s not a good one.'
    if timePooping > halfHour:
        longPoop = ' His leg is Asleep.'
    if myLastPost > startTime:
        poopUpdate = 'still '
    else:
        mystatusID = type(None)
    if poopStart == 2:
        msg = name + ' could be ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        logging.info(msg)
    elif poopStart == 3:
        msg = name + ' is probably ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        logging.info(msg)
    elif poopStart == 4:
        msg = name + ' is ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        logging.info(msg)
    elif poopStart >= 5:
        msg = name + ' is definitely ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        logging.info(msg)
    else:
        logging.info('I don\'t know what\'s happening')
    if postText != msg or msg != '':
        logging.info('posting')
        api.update_status(status = msg, in_reply_to_status_id = mystatusID, auto_populate_reply_metadata = True)
    return msg
def testSomething():
    myLastPost = ""
    postTest = ""
    mystatusID = type(None)
    print(mystatusID)
    logging.info(mystatusID)
    statuses = api.user_timeline(screen_name = 'elonthetoilet', count = 1)
    for status in statuses:
        myLastPost = status.created_at
        postText = status.text
    print(mystatusID)
    logging.info(mystatusID)
    api.update_status(status = 'This is only a test nobody is pooping.', in_reply_to_status_id = mystatusID, auto_populate_reply_metadata = True)
    