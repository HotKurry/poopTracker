import pandas as pd
#from sqlalchemy import null
import tweepy
from datetime import datetime, timezone, timedelta
import logging
import os
from os.path import exists

apiKey = 'sHTQPJsFOiQEkK0MuOTRFHeIL'
apiSecret = 'qfFb25tt5mcDM20oS89WE8pc2zvDzQsq3m9ZsnIP3cEaPwrPSx'
accessToken = '1179986678431338496-D8dAzcoZl74H9DBflq1wt3Pu4hedWS'
accessTokenSecret = 'RUzUanQH6EYn4cHeRUymn1NWIoT7TslHDTu2nuheedH76'
bearerToken = 'AAAAAAAAAAAAAAAAAAAAAE6xYwEAAAAAx6VmrZuW6yKEYYdLQG6Uh6UJNT8%3DnkWzitZtK57cJGFvpONBGmHvZvAAEF1syPlcl0VhWWvBdZC30j'

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
    days = sincepost.days
    seconds = sincepost.seconds
    hours = seconds//3600
    minutes = (seconds//60)%60
    if ind == 0:
        logging.info("Time Since last post: " +str(days) + ' days ' + str(hours) +' hours ' +  str(minutes) + ' mins')
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
            startPost -= 1
            break
    return startPost

#Create a post based on action density, time and number of actions. return text
def postSomething(name, poopStart, df):
    now = datetime.now(timezone.utc)
    startTime =  datetime.strptime(df.iat[poopStart,1], '%Y-%m-%d %H:%M:%S%z')
    timePooping = now - startTime
    poopDensity = timePooping / poopStart
    statuses = api.user_timeline(screen_name = 'elonthetoilet', count = 1)
    for status in statuses:
        myLastPost = status.created_at
        postText = status.text
        mystatusID = status.id
    poopUpdate = ''
    timeSincePoop = now - myLastPost
    halfHour = timedelta(minutes=30)    
    quiteDense = timedelta(minutes=4)
    veryDense = timedelta(minutes=2)
    densePoop = ''
    longPoop = ''
    msg = ''
    endText = ''
    days = timeSincePoop.days
    seconds = timeSincePoop.seconds
    hours = seconds//3600
    minutes = (seconds//60)%60
    #logging
    logging.info('poopstart#: ' +str(poopStart))
    logging.info('time between action during: ' +str(poopDensity))
    logging.info('duration of pooping: ' + str(timePooping))
    logging.info('Time of my last post: ' + str(hours) +' hours' +  str(minutes) + ' min(s)')
    logging.info('When Pooping started: ' + str(startTime))
    logging.info('Last post Text: ' + str(postText))
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
        #mystatusID = None
        poopdays = ''
        poophours = ''
        poopminutes = ''
        #text formatting (days)
        if days == 1:
            poopdays = '1 day '
        elif days > 1:
            poopdays = str(days) + 'days '
        #text formatting (hours)
        if hours == 1:
            poophours = '1 hour '
        elif hours > 1:
            poophours = str(hours) + 'hours '
        #text formatting (minuts)
        if minutes == 1:
            poopminutes = '1 minute '
        elif minutes > 1:
            poopminutes = str(minutes) + 'minutes '  
        endText = 'His last poop was ' + poopdays + poophours + poopminutes +  'ago.'
    if poopStart == 1:
        msg = name + ' could be ' + poopUpdate + 'pooping.' +  densePoop + longPoop + endText
        logging.info(msg)
    elif poopStart == 2:
        msg = name + ' is probably ' + poopUpdate + 'pooping.' +  densePoop + longPoop + endText
        logging.info(msg)
    elif poopStart == 3:
        msg = name + ' is ' + poopUpdate + 'pooping.' +  densePoop + longPoop + endText
        logging.info(msg)
    elif poopStart >= 4:
        msg = name + ' is definitely ' + poopUpdate + 'pooping.' +  densePoop + longPoop
        logging.info(msg)
    else:
        logging.info('I don\'t know what\'s happening')
    if (postText != msg or myLastPost > startTime) and msg != '':
        logging.info('posting')
        api.update_status(status = msg, in_reply_to_status_id = mystatusID, auto_populate_reply_metadata = True)
    return msg

""" def testSomething():
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


def testTimepooping(df):
    now = datetime.now(timezone.utc)
    startTime =  datetime.strptime(df.iat[0,1], '%Y-%m-%d %H:%M:%S%z')
    timePooping = now - startTime
    print(timePooping)
    logging.info(timePooping)
    halfHour = timedelta(minutes=30)
    print(halfHour)
    logging.info(halfHour)
    if timePooping > halfHour:
        print('greater')
    else:
        print('lessthan')


def testDoublepost():
    name = "Elon Musk"
    poopUpdate = 'still '
    msg = ""
    postText=""
    msg = name + ' is definitely ' + poopUpdate + 'pooping.'
    statuses = api.user_timeline(screen_name = 'elonthetoilet', count = 1)
    for status in statuses:
        myLastPost = status.created_at
        postText = status.text
    if postText != msg and msg != '':
        logging.info(msg)
        logging.info(postText)
        logging.info('posting')
    else:
        logging.info('notposting')
    return msg

def testingTime():
    now = datetime.now(timezone.utc)
    statuses = api.user_timeline(screen_name = 'elonthetoilet', count = 1)
    for status in statuses:
        myLastPost = status.created_at
        postText = status.text
   """ 