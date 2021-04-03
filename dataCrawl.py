from pymongo import MongoClient
import json
import tweepy
import emoji
import time
import re

# Twitter Developer Authority:
api_key = "RaB095J4xQTED7xBCWYQ2nufy"
api_secret_key = "zPFHxgZLyZEq1af0anOWze2a6LB1nHZgzKFS130ZFGme0BcZUb"
access_token = "1374723615191621632-9h5teePVDj5I2YgvfuCa4FfjYMGp9t"
access_token_secret = "7tiW0v2g66CSarDv0oxiEjNOeqhPM3dnrCnhE7DNWUO9S"

# api_key = "iZC6veei76gDMGAJS46hQUHPg"
# api_secret_key = "kcm4oIsquusXPs30SpQr8IzvB2EANKyrU62FqnFguHqeu5avHy"
# access_token = "1202150312712253441-iXclTlTKojpWWCSVmLyXSH0fmk1i6i"
# access_token_secret = "lJuANij9ov8HkIB2rpF9isAAelg0tqZSjNyPNqMeLPhME"



auth = tweepy.OAuthHandler(api_key,api_secret_key)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Link to the database MongoDB:
dbClient = MongoClient("localhost", 27017)
dbName = "Twitter_Data"
db = dbClient[dbName]
rest_colName = "RestData"
RestData = db[rest_colName]
stream_colName = "StreamData"
StreamData = db[stream_colName]

# Remove emoji
def strip_emoji(content):
    new_cont = re.sub(emoji.get_emoji_regexp(), r"", content)
    return new_cont

def cleanList(content):
    new_cont = strip_emoji(content)
    new_cont.encode("ascii", errors="ignore").decode()
    return new_cont

def tweet_content(tweet, t):
    # Tweet object
    try:
        tweet_time = tweet['created_at']
        tweet_id = tweet['id']
        text = tweet[t]
    except Exception as e:
        print(e)
        return None

    try:
        if tweet['truncated']:
            text = tweet['extended_tweet']['full_text']
        elif text.startswith('RT'):
            retweet = True
            try:
                if tweet['retweeted_status']['truncated']:
                    text = tweet['retweeted_status']['extended_tweet']['full_text']
                else:
                    text = tweet['retweeted_status']['full_text']
            except Exception as e:
                pass
    except Exception as e:
        print(e)
    tweet_text = cleanList(text)

    quote = tweet['is_quote_status']
    retweet = tweet['retweet_count']
    source = tweet['source']


    # User object
    user = tweet['user']['screen_name']
    verified = tweet['user']['verified']
    location = tweet['user']['location']
    geo_enabled = tweet['user']['geo_enabled']
    followers = tweet['user']['followers_count']

    # Place object
    try:
        city = tweet['place']['name']
        country = tweet['place']['country']
    except Exception as e:
        city = ''
        country = ''


    # Entities object
    try:
        hashtags = tweet['entities']['hashtags'][0]['text']
    except Exception as e:
        hashtags = ''

    try:
        media_type = tweet['extended_entities']['media'][0]['type']
        if media_type == 'photo':
            media_url = tweet['extended_entities']['media'][0]['media_url']
        elif media_type == 'video':
            media_url = tweet['extended_entities']['media'][0]["video_info"]["variants"][0]["url"]
        else:
            media_url = tweet['extended_entities']['media'][0]["video_info"]["variants"][0]["url"]
    except Exception as e:
        media_type = ''
        media_url = ''

    tweet = {
            '_id': tweet_id, 'date': tweet_time, 'tweet_text': tweet_text,'quote': quote, 'retweet': retweet, 'source': source,
            'username': user, 'verified': verified, 'location': location, 'followers_count': followers, 'media_type': media_type,
             'media_url': media_url, 'city': city, 'country': country,'geo_enabled': geo_enabled, 'hashtags': hashtags,
             }
    return tweet

# Streaming API
class streamCrawl(tweepy.StreamListener):

    global geoEnabled
    global geoDisabled

    def on_connect(self):
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        print('An Error has occurred: ' + repr(status_code))
        return False

    def on_data(self, data):
        t = json.loads(data)
        tweet = tweet_content(t,'text')
        print("streaming api:", tweet)
        try:
            StreamData.insert_one(tweet)
        except Exception as e:
            print(e)


Loc_UK = [-10.392627, 49.681847, 1.055039, 61.122019]

Words_UK = ["Covid", "BBC", "vaccine", "2019-nCoV", "virus", "Scotland","Glasgow","Edinburgh","London", "England",
            "Manchester", "Sheffield", "York", "Southampton", "football","Harry", "Meghan", "NHS", "wildfire",
            "susceptible", "suspected","epidemic", "Bristol", "American"]


listener = streamCrawl(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
streamer.filter(locations=Loc_UK, languages=['en'], track=Words_UK, is_async=True)


# Rest API
Place = 'London'
Lat = '51.450798'
Long = '-0.137842'
geoTerm = Lat + ',' + Long + ',' + '1000km'

last_id = None
counter = 0
sinceID = None
results = True

while results:
    if counter < 50000:
        try:
            results = api.search(
                q="Covid" or "virus" or "independence" or "European Union" or "EU" or "Bristol" or
                  "departure" or "Scotland" or "BBC" or "economic",
                geocode=geoTerm, count=10000, max_id=last_id, lang="en", tweet_mode='extended')
            for x in results:
                resultsJson = x._json
                tweet = tweet_content(resultsJson,'full_text')
                print("REST api:", tweet)
                try:
                    RestData.insert_one(tweet)
                    # with open("./data/DataRest3.json", "a") as f:
                    #     f.writelines(json_util.dumps(tweet1))
                    #     f.write('\n')
                    #     print("Loading ini the file ...")
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            counter += 1
    else:
        time.sleep(15 * 60)
